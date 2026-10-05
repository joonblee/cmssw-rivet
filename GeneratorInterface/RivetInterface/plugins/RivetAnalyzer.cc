#include "GeneratorInterface/RivetInterface/interface/RivetAnalyzer.h"
#include "GeneratorInterface/RivetInterface/interface/WeightUtils.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Run.h"

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "Rivet/Run.hh"
#include "Rivet/AnalysisHandler.hh"
#include "Rivet/Analysis.hh"

#include <regex>
#include <fstream>
#include <map>
#include <set>
#include "FWCore/Utilities/interface/Exception.h"

using namespace Rivet;
using namespace edm;

RivetAnalyzer::RivetAnalyzer(const edm::ParameterSet& pset)
    : _isFirstEvent(true),
      _outFileName(pset.getParameter<std::string>("OutputFile")),
      _analysisNames(pset.getParameter<std::vector<std::string> >("AnalysisNames")),
      //decide whether to finalize the plots or not.
      //deciding not to finalize them can be useful for further harvesting of many jobs
      _doFinalize(pset.getParameter<bool>("DoFinalize")),
      _lheLabel(pset.getParameter<edm::InputTag>("LHECollection")),
      _xsection(-1.) {
  usesResource("Rivet");

  _hepmcCollection = consumes<HepMC3Product>(pset.getParameter<edm::InputTag>("HepMCCollection"));
  _genLumiInfoToken = consumes<GenLumiInfoHeader, edm::InLumi>(pset.getParameter<edm::InputTag>("genLumiInfo"));

  _useLHEweights = pset.getParameter<bool>("useLHEweights");
  _weightMetadataFile = pset.getParameter<std::string>("WeightMetadataFile");
  _allowMissingLHEWeights = pset.getParameter<bool>("allowMissingLHEWeights");
  _preserveVariationRate = pset.getParameter<bool>("preserveVariationRate");
  if (_useLHEweights) {
    _lheLabels.push_back(_lheLabel);
    for (const auto& tag : pset.getParameter<std::vector<edm::InputTag>>("LHEFallbackCollections"))
      if (tag != _lheLabel) _lheLabels.push_back(tag);
    for (const auto& tag : _lheLabels) {
      _lheRunTokens.push_back(consumes<LHERunInfoProduct, edm::InRun>(tag));
      _lheEventTokens.push_back(consumes<LHEEventProduct>(tag));
    }
  }

  _weightCap = pset.getParameter<double>("weightCap");
  _NLOSmearing = pset.getParameter<double>("NLOSmearing");
  _setIgnoreBeams = pset.getParameter<bool>("setIgnoreBeams");
  _skipMultiWeights = pset.getParameter<bool>("skipMultiWeights");
  _selectMultiWeights = pset.getParameter<std::string>("selectMultiWeights");
  _deselectMultiWeights = pset.getParameter<std::string>("deselectMultiWeights");
  _setNominalWeightName = pset.getParameter<std::string>("setNominalWeightName");

  //set user cross section if needed
  _xsection = pset.getParameter<double>("CrossSection");
}

RivetAnalyzer::~RivetAnalyzer() {}

void RivetAnalyzer::beginJob() {
  //set the environment, very ugly but rivet is monolithic when it comes to paths
  char* cmsswbase = std::getenv("CMSSW_BASE");
  char* cmsswrelease = std::getenv("CMSSW_RELEASE_BASE");
  if (!std::getenv("RIVET_REF_PATH")) {
    const std::string rivetref = string(cmsswbase) +
                                 "/src/GeneratorInterface/RivetInterface/data:" + string(cmsswrelease) +
                                 "/src/GeneratorInterface/RivetInterface/data:.";
    char* rivetrefCstr = strdup(rivetref.c_str());
    setenv("RIVET_REF_PATH", rivetrefCstr, 1);
    free(rivetrefCstr);
  }
  if (!std::getenv("RIVET_INFO_PATH")) {
    const std::string rivetinfo = string(cmsswbase) +
                                  "/src/GeneratorInterface/RivetInterface/data:" + string(cmsswrelease) +
                                  "/src/GeneratorInterface/RivetInterface/data:.";
    char* rivetinfoCstr = strdup(rivetinfo.c_str());
    setenv("RIVET_INFO_PATH", rivetinfoCstr, 1);
    free(rivetinfoCstr);
  }
}

void RivetAnalyzer::beginRun(const edm::Run& iRun, const edm::EventSetup& iSetup) {
  _runHeaders.clear();
  for (const auto& token : _lheRunTokens) {
    std::vector<std::pair<std::string, std::string>> headers;
    auto handle = iRun.getHandle(token);
    if (handle.isValid()) {
      for (auto it = handle->headers_begin(); it != handle->headers_end(); ++it) {
        std::string text;
        for (const auto& line : it->lines()) text += line + "\n";
        // Other headers can be very large; only reweighting definitions are needed.
        if (text.find("<weight") != std::string::npos) headers.emplace_back(it->tag(), text);
      }
    }
    _runHeaders.push_back(headers);
  }
}

void RivetAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<HepMC3Product> evt;
  iEvent.getByToken(_hepmcCollection, evt);
  auto genEvent = std::make_unique<HepMC3::GenEvent>();
  genEvent->read_data(*evt->GetEvent());
  if (genEvent->weights().empty()) throw cms::Exception("RivetWeights") << "Empty generator weight vector";

  edm::Handle<LHEEventProduct> lhe;
  size_t lheSource = 0;
  for (; lheSource < _lheEventTokens.size(); ++lheSource) {
    lhe = iEvent.getHandle(_lheEventTokens[lheSource]);
    if (lhe.isValid()) break;
  }
  const bool hasLHE = lhe.isValid() && !lhe->weights().empty();
  if (_useLHEweights && !hasLHE && !_allowMissingLHEWeights)
    throw cms::Exception("RivetWeights") << "No LHE variation weights found in configured products";

  std::vector<std::string> originalNames;
  auto genLumiInfo = iEvent.getLuminosityBlock().getHandle(_genLumiInfoToken);
  if (genLumiInfo.isValid()) originalNames = genLumiInfo->weightNames();
  if (!originalNames.empty() && originalNames.size() != genEvent->weights().size())
    throw cms::Exception("RivetWeights") << "Generator weight names and values have different sizes";
  if (originalNames.empty()) originalNames.resize(genEvent->weights().size());

  if (_isFirstEvent) {
    _generatorOriginalNames = originalNames;
    for (size_t i = 0; i < originalNames.size(); ++i) {
      // Indexed names avoid collisions after sanitising PS descriptions.
      std::string name = i == 0 ? "" : "GEN_" + std::to_string(i) + "_" + rivetweights::cleanName(originalNames[i]);
      _generatorWeightNames.push_back(name);
    }
    _hasLHEWeights = hasLHE;
    if (hasLHE) {
      _selectedLHELabel = _lheLabels[lheSource].encode();
      _metadataHeaders = _runHeaders[lheSource];
      for (const auto& weight : lhe->weights()) {
        _lheWeightIds.push_back(weight.id);
        _lheWeightNames.push_back("LHE_" + rivetweights::cleanName(weight.id));
      }
    }
    _cleanedWeightNames = _generatorWeightNames;
    _cleanedWeightNames.insert(_cleanedWeightNames.end(), _lheWeightNames.begin(), _lheWeightNames.end());
    std::set<std::string> names(_cleanedWeightNames.begin(), _cleanedWeightNames.end());
    if (names.size() != _cleanedWeightNames.size())
      throw cms::Exception("RivetWeights") << "Duplicate or colliding weight IDs";
    runinfo = std::make_shared<HepMC3::GenRunInfo>();
    runinfo->set_weight_names(_cleanedWeightNames);
  } else {
    if (originalNames != _generatorOriginalNames || hasLHE != _hasLHEWeights)
      throw cms::Exception("RivetWeights") << "Weight layout changed between events; split incompatible inputs";
    if (hasLHE && (_metadataHeaders != _runHeaders[lheSource] ||
                   _selectedLHELabel != _lheLabels[lheSource].encode()))
      throw cms::Exception("RivetWeights") << "LHE definitions changed between runs; split incompatible inputs";
  }

  std::vector<double> mergedWeights = genEvent->weights();
  for (double weight : mergedWeights)
    if (!std::isfinite(weight)) throw cms::Exception("RivetWeights") << "Non-finite generator weight";
  if (hasLHE) {
    std::vector<std::pair<std::string, double>> input;
    for (const auto& weight : lhe->weights()) input.emplace_back(weight.id, weight.wgt);
    auto weights = rivetweights::orderedLHEWeights(mergedWeights[0], lhe->originalXWGTUP(), _lheWeightIds, input);
    mergedWeights.insert(mergedWeights.end(), weights.begin(), weights.end());
  }

  double xsection = _xsection > 0 ? _xsection : genEvent->cross_section()->xsecs()[0];
  _nominalXsection = xsection;
  HepMC3::GenCrossSectionPtr xsec = make_shared<HepMC3::GenCrossSection>();
  xsec->set_cross_section(std::vector<double>(mergedWeights.size(), xsection),
                          std::vector<double>(mergedWeights.size(), 0.));
  genEvent->set_cross_section(xsec);
  genEvent->set_run_info(runinfo);
  genEvent->weights() = mergedWeights;

  //apply the beams initialization on the first event
  if (_isFirstEvent) {
    _analysisHandler = std::make_unique<Rivet::AnalysisHandler>();
    _analysisHandler->addAnalyses(_analysisNames);

    /// Set analysis handler weight options
    _analysisHandler->setCheckBeams(!_setIgnoreBeams);
    _analysisHandler->skipMultiWeights(_skipMultiWeights);
    _analysisHandler->matchWeightNames(_selectMultiWeights);
    _analysisHandler->unmatchWeightNames(_deselectMultiWeights);
    _analysisHandler->setNominalWeightName(_setNominalWeightName);
    _analysisHandler->setWeightCap(_weightCap);
    _analysisHandler->setNLOSmearing(_NLOSmearing);

    _analysisHandler->init(*genEvent);

    _isFirstEvent = false;
  }

  //run the analysis
  _analysisHandler->analyze(const_cast<GenEvent&>(*genEvent));
}

void RivetAnalyzer::endRun(const edm::Run& iRun, const edm::EventSetup& iSetup) {
  // A CRAB input file can contain several runs: finalise only once in endJob.
}

void RivetAnalyzer::endJob() {
  if (_isFirstEvent) return;
  // Equal per-weight cross sections cancel rate variations in sigma/sumW.
  // The scalar API derives sigma_i = sigma_nom * sumW_i / sumW_nom.
  if (_preserveVariationRate)
    _analysisHandler->setCrossSection(std::make_pair(_nominalXsection, 0.), true);
  if (_doFinalize) _analysisHandler->finalize();
  _analysisHandler->writeData(_outFileName);

  if (!_weightMetadataFile.empty()) {
    std::ofstream out(_weightMetadataFile);
    if (!out) throw cms::Exception("RivetWeights") << "Cannot write " << _weightMetadataFile;
    out << "{\n  \"schema_version\": 1,\n  \"use_lhe_weights\": " << (_useLHEweights ? "true" : "false")
        << ",\n  \"has_lhe_weights\": " << (_hasLHEWeights ? "true" : "false")
        << ",\n  \"preserve_variation_rate\": " << (_preserveVariationRate ? "true" : "false")
        << ",\n  \"lhe_collection\": " << rivetweights::jsonString(_selectedLHELabel)
        << ",\n  \"generator_weights\": [";
    for (size_t i = 0; i < _generatorWeightNames.size(); ++i) {
      if (i) out << ',';
      out << "\n    {\"name\": " << rivetweights::jsonString(_generatorWeightNames[i])
          << ", \"description\": " << rivetweights::jsonString(_generatorOriginalNames[i]) << '}';
    }
    out << "\n  ],\n  \"lhe_weights\": [";
    for (size_t i = 0; i < _lheWeightIds.size(); ++i) {
      if (i) out << ',';
      out << "\n    {\"id\": " << rivetweights::jsonString(_lheWeightIds[i])
          << ", \"name\": " << rivetweights::jsonString(_lheWeightNames[i]) << '}';
    }
    out << "\n  ],\n  \"lhe_headers\": [";
    for (size_t i = 0; i < _metadataHeaders.size(); ++i) {
      if (i) out << ',';
      out << "\n    {\"tag\": " << rivetweights::jsonString(_metadataHeaders[i].first)
          << ", \"text\": " << rivetweights::jsonString(_metadataHeaders[i].second) << '}';
    }
    out << "\n  ]\n}\n";
    if (!out) throw cms::Exception("RivetWeights") << "Failed writing " << _weightMetadataFile;
  }
}

DEFINE_FWK_MODULE(RivetAnalyzer);
