# MG paper: generator comparisons
### python3 crab.py      # to submit multiple commands at once, rather use crab submit

import os
from CRABClient.UserUtilities import config
config = config()

RunDate    = '260331_1026'
config.General.requestName = ''
config.General.workArea    = 'crablog' + RunDate
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = './rivet_GEN-25-002_W_cfg.py'

config.Data.inputDataset = ''
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publication = False
config.Data.outputDatasetTag = ''

config.Site.storageSite = 'T3_KR_KNU'


if __name__ == '__main__':
  from CRABAPI.RawCommand import crabCommand

  ### MC ###
  config.Data.splitting = 'FileBased'
  config.Data.unitsPerJob = 1
  config.JobType.pyCfgParams = ['yodafile=output.yoda', 'maxEvents=-1']
  config.JobType.outputFiles = ['output.yoda']

  # mg+py
  config.General.requestName = 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_mcRun2'
  config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  config.Data.inputDataset   = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAOD-106X_mcRun2_asymptotic_v13-v2/MINIAODSIM'
  config.Data.splitting = 'FileBased'
  crabCommand('submit', config = config)

  config.General.requestName = 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_upgrade2018'
  config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  config.Data.inputDataset   = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM'
  config.Data.splitting = 'FileBased'
  crabCommand('submit', config = config)


  # config.General.requestName = 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_mcRun2'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer19UL16MiniAOD-106X_mcRun2_asymptotic_v13-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_mc2017'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_upgrade2018'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # # sherpa
  # config.General.requestName = 'WJetsToLNu_012JetsNLO_34JetsLO_EWNLOcorr_13TeV-sherpa'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WJetsToLNu_012JetsNLO_34JetsLO_EWNLOcorr_13TeV-sherpa/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v4/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WJetsToLNu_012JetsNLO_34JetsLO_EWNLOcorr_13TeV-sherpa_ext1'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WJetsToLNu_012JetsNLO_34JetsLO_EWNLOcorr_13TeV-sherpa/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9_ext1-v3/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # # aMC@NLO
  # config.General.requestName = 'WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8_mcRun2'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8_upgrade2018'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # # MiNNLO
  # config.General.requestName = 'WminusJetsToMuNu_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WminusJetsToMuNu_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL16MiniAOD-106X_mcRun2_asymptotic_v13-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WplusJetsToMuNu_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WplusJetsToMuNu_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL16MiniAOD-106X_mcRun2_asymptotic_v13-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WplusJetsToTauNu_TauToMu_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WplusJetsToTauNu_TauToMu_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL16MiniAOD-106X_mcRun2_asymptotic_v13-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WminusJetsToTauNu_TauToMu_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WminusJetsToTauNu_TauToMu_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL16MiniAOD-106X_mcRun2_asymptotic_v13-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WplusJetsToMuNu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WplusJetsToMuNu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIIFall17MiniAODv2-fixECALGT_LowPU_94X_mc2017_realistic_v10For2017H_v2-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WplusJetsToTauNu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WplusJetsToTauNu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIIFall17MiniAODv2-fixECALGT_LowPU_94X_mc2017_realistic_v10For2017H_v2-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WplusJetsToENu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WplusJetsToENu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIIFall17MiniAODv2-fixECALGT_LowPU_94X_mc2017_realistic_v10For2017H_v2-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WminusJetsToENu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WminusJetsToENu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIIFall17MiniAODv2-fixECALGT_LowPU_94X_mc2017_realistic_v10For2017H_v2-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WminusJetsToTauNu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WminusJetsToTauNu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIIFall17MiniAODv2-fixECALGT_LowPU_94X_mc2017_realistic_v10For2017H_v2-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'WminusJetsToMuNu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/WminusJetsToMuNu_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIIFall17MiniAODv2-fixECALGT_LowPU_94X_mc2017_realistic_v10For2017H_v2-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)




