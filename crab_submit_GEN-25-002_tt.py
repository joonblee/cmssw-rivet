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
config.JobType.psetName = './rivet_GEN-25-002_tt_cfg.py'

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
  config.Data.unitsPerJob = 2
  config.JobType.pyCfgParams = ['yodafile=output.yoda', 'maxEvents=-1']
  config.JobType.outputFiles = ['output.yoda']

  # config.General.requestName = 'TT_TuneCH3_13TeV-powheg-herwig7'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate 
  # config.Data.inputDataset   = '/TT_TuneCH3_13TeV-powheg-herwig7/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  #config.General.requestName = 'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_v2'
  #config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #config.Data.inputDataset   = '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM'
  #config.Data.splitting = 'FileBased'
  #crabCommand('submit', config = config)

  # # Toponium paper
  # # (831.76 x 0.1049)
  # config.General.requestName = 'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)
  # ---> Not working

  # # (831.76)
  # # (/TT_TuneEE5C_13TeV-powheg-herwigpp/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM)
  # config.General.requestName = 'TT_TuneEE5C_13TeV-powheg-herwigpp'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TT_TuneEE5C_13TeV-powheg-herwigpp/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'TT_TuneEE5C_13TeV-powheg-herwigpp_ext3'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TT_TuneEE5C_13TeV-powheg-herwigpp/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext3-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)
 
  # # powheg+py (CUETP8M2T4)
  # config.General.requestName = 'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_backup'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)
 
  # # powheg+py (New material for the top mass review paper)
  # config.General.requestName = 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  config.General.requestName = 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8'
  config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  config.Data.inputDataset   = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM'
  config.Data.splitting = 'FileBased'
  crabCommand('submit', config = config)

  # config.General.requestName = 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)
 
  # # mg+py
  # config.General.requestName = 'TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'TTJets_TuneCP5_13TeV-madgraphMLM-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)
  # 
 
  # config.General.requestName = 'TTToDileptonic_TuneCP5_13TeV-madgraph-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTToDileptonic_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

  # config.General.requestName = 'TTToSemileptonic_TuneCP5_13TeV-madgraph-pythia8'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTToSemileptonic_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)
 
  # # sherpa
  # config.General.requestName = 'TTtoLminusNuQ-4Jets-1NLO3LO_13TeV_sherpa'
  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # config.Data.inputDataset   = '/TTtoLminusNuQ-4Jets-1NLO3LO_13TeV_sherpa/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM'
  # config.Data.splitting = 'FileBased'
  # crabCommand('submit', config = config)

