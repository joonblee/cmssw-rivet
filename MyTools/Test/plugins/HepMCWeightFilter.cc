#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include <memory>
#include <cmath>

#include "SimDataFormats/GeneratorProducts/interface/HepMC3Product.h"
#include "HepMC3/GenEvent.h"

class HepMCWeightFilter : public edm::stream::EDFilter<> {
public:
  explicit HepMCWeightFilter(const edm::ParameterSet& cfg)
    : src_(cfg.getParameter<edm::InputTag>("src")),
      maxWeight_(cfg.getParameter<double>("maxWeight"))
  {
    token_ = consumes<edm::HepMC3Product>(src_);
  }

  bool filter(edm::Event& evt, const edm::EventSetup&) override {
    edm::Handle<edm::HepMC3Product> h;
    evt.getByToken(token_, h);

    const auto* ev = h->GetEvent();
    double w = ev->weights.empty() ? 1.0 : ev->weights[0];

    return (std::abs(w) < maxWeight_);
  }

private:
  edm::InputTag src_;
  edm::EDGetTokenT<edm::HepMC3Product> token_;
  double maxWeight_;
};

DEFINE_FWK_MODULE(HepMCWeightFilter);

