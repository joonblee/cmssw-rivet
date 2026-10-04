import sys
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing ('standard')
options.register('runOnly', '', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "Run only specified analysis")
options.register('yodafile', 'output.yoda', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "Name of yoda output file")
options.setDefault('maxEvents', 100)
if(hasattr(sys, "argv")):
    options.parseArguments()
print(options)

process = cms.Process("runRivetAnalysis")

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

# MiniAOD does not have HepMC nor genParticles. It is thus necessary to produce "mergedGenParticles using prunedGenParticles + packedGenParticles" and then trasfer "mergedGenParticles -> HepMC"
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())
process.mergedGenParticles = cms.EDProducer("MergedGenParticleProducer",
    inputPruned = cms.InputTag("prunedGenParticles"),
    inputPacked = cms.InputTag("packedGenParticles"),
)
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.generator = cms.EDProducer("GenParticles2HepMCConverter",
    genParticles = cms.InputTag("mergedGenParticles"),
    #genEventInfo = cms.InputTag("generator", "", "SIM"), # MiniAODv1, v3
    #genEventInfo = cms.InputTag("generator", "", "GEN"), # MiniAODv2
    genEventInfo = cms.InputTag("generator"), # test
    signalParticlePdgIds = cms.vint32()
)

# run rivet
process.load("GeneratorInterface.RivetInterface.rivetAnalyzer_cfi")

if options.runOnly:
    process.rivetAnalyzer.AnalysisNames = cms.vstring(options.runOnly)
else:
    process.rivetAnalyzer.AnalysisNames = cms.vstring(
        #'MC_GENERIC', # MC generic analysis
        'MC_XS', # MC xs analysis
        #"CMS_2022_I2079374",
        "RivetNonIsoPheno",
        "HiggsTemplateCrossSections"
    )

#process.rivetAnalyzer.UserAnalysisPaths = cms.vstring("/afs/cern.ch/work/j/joon/private/mg/paper/CMSSW_14_2_0/src")
process.rivetAnalyzer.OutputFile      = options.yodafile
#process.rivetAnalyzer.CrossSection    = 831.76 # NNLO (arXiv:1303.6254)

process.rivetAnalyzer.HepMCCollection = cms.InputTag("generator:unsmeared")
process.p = cms.Path(process.mergedGenParticles*process.generator*process.rivetAnalyzer)

process.source.fileNames = [
'file:./DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos.root',
]
