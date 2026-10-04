# generator comparisons

import sys
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing ('standard')
options.register('runOnly', '', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "Run only specified analysis")
options.register('yodafile', 'output.yoda', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "Name of yoda output file")
#options.setDefault('maxEvents', 100)
if(hasattr(sys, "argv")):
    options.parseArguments()
print(options)

process = cms.Process("runRivetAnalysis")

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)
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
        'ATLAS_2017_I1495243',
        'ATLAS_2017_I1614149',
        'ATLAS_2018_I1646686',
        'ATLAS_2019_I1750330',
        'ATLAS_2019_I1759875',
        'ATLAS_2022_I2037744',
        'ATLAS_2022_I2077575',
        'ATLAS_2022_I2152933',
        'ATLAS_2023_I2648096',
        'CMS_2016_I1491950',
        'CMS_2018_I1620050',
        'CMS_2018_I1662081',
        'CMS_2018_I1663958',
        'CMS_2018_I1703993',
        'CMS_2021_I1901295'
    )
process.rivetAnalyzer.OutputFile      = options.yodafile
#process.rivetAnalyzer.CrossSection    = 831.76 # NNLO (arXiv:1303.6254)

# 1. simplest case
process.rivetAnalyzer.HepMCCollection = cms.InputTag("generator:unsmeared")
process.p = cms.Path(process.mergedGenParticles*process.generator*process.rivetAnalyzer)

# 2. weight unity
# process.weightUnity = cms.EDProducer("HepMCWeightUnityProducer",
#     src = cms.InputTag("generator","unsmeared")
# )
# process.rivetAnalyzer.HepMCCollection = cms.InputTag("weightUnity")
# process.p = cms.Path(process.mergedGenParticles*process.generator*process.weightUnity*process.rivetAnalyzer)

# 3. reject high weight event
# process.weightFilter = cms.EDFilter("HepMCWeightFilter",
#     src       = cms.InputTag("generator","","GEN"),
#     maxWeight = cms.double(100.0)
# )
# process.rivetAnalyzer.HepMCCollection = cms.InputTag("generator:unsmeared")
# process.p = cms.Path(process.mergedGenParticles*process.generator*process.weightFilter*process.rivetAnalyzer)



process.source.fileNames = [
#'file:./DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos.root',
]
