# MG paper: generator comparisons
### python3 crab.py      # to submit multiple commands at once, rather use crab submit

import os
from CRABClient.UserUtilities import config
config = config()

RunDate    = '251217_1157'
config.General.requestName = ''
config.General.workArea    = 'crablog' + RunDate
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = './rivet_GEN-25-002_DY_cfg.py'

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
  config.JobType.outputFiles = ['output.yoda', 'output.weights.json']

  #   ### 2016
  # 
  #   config.General.requestName = 'DY01234jets_13TeV-sherpa'
  #   config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   config.Data.inputDataset   = '/DY01234jets_13TeV-sherpa/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
  #   config.Data.splitting = 'FileBased'
  #   crabCommand('submit', config = config)
  # 
  #   ## DYjetsto*_01234jets_Pt-0ToInf_13TeV-sherpa samples are in Rucio # cannot be used!!!
  # 
  #   # config.General.requestName = 'DYjetstoee_01234jets_Pt-0ToInf_13TeV-sherpa'
  #   # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   # config.Data.inputDataset   = '/DYjetstoee_01234jets_Pt-0ToInf_13TeV-sherpa/RunIISummer16MiniAODv3-PUMoriond17_QCDEWNLO_correct_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
  #   # config.Data.splitting = 'FileBased'
  #   # crabCommand('submit', config = config)
  # 
  #   # config.General.requestName = 'DYjetstomumu_01234jets_Pt-0ToInf_13TeV-sherpa'
  #   # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   # config.Data.inputDataset   = '/DYjetstomumu_01234jets_Pt-0ToInf_13TeV-sherpa/RunIISummer16MiniAODv3-PUMoriond17_QCDEWNLO_correct_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
  #   # config.Data.splitting = 'FileBased'
  #   # crabCommand('submit', config = config)
  # 
  #   # config.General.requestName = 'DYjetstotautau_01234jets_Pt-0ToInf_13TeV-sherpa'
  #   # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   # config.Data.inputDataset   = '/DYjetstotautau_01234jets_Pt-0ToInf_13TeV-sherpa/RunIISummer16MiniAODv3-PUMoriond17_QCDEWNLO_correct_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
  #   # config.Data.splitting = 'FileBased'
  #   # crabCommand('submit', config = config)
  # 
  #   ## Warning:			CRAB refuses to proceed in getting the details of the dataset /DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL16MiniAOD-106X_mcRun2_asymptotic_v13-v2/MINIAODSIM from DBSbecause the dataset is not 'VALID' but 'INVALID'. To allow CRAB to consider a dataset that is not 'VALID', set Data.allowNonValidInputDataset = True in the CRAB configuration. Notice that this will not force CRAB to run over all files in the dataset; CRAB will still check if there are any valid files in the dataset and run only over those files.
  # 
  #   # config.General.requestName = 'DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8'
  #   # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   # config.Data.inputDataset   = '/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL16MiniAOD-106X_mcRun2_asymptotic_v13-v2/MINIAODSIM'
  #   # config.Data.splitting = 'FileBased'
  #   # crabCommand('submit', config = config)
  # 
  #   ## No DYToMuMu*powheg-pythia8 sample
  # 
  #   config.General.requestName = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8'
  #   config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   config.Data.inputDataset   = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM'
  #   config.Data.splitting = 'FileBased'
  #   crabCommand('submit', config = config)
  # 
  #   config.General.requestName = 'DYJetsToLL_M-50_TuneCH3_13TeV-madgraphMLM-herwig7'
  #   config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   config.Data.inputDataset   = '/DYJetsToLL_M-50_TuneCH3_13TeV-madgraphMLM-herwig7/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM'
  #   config.Data.splitting = 'FileBased'
  #   crabCommand('submit', config = config)
  # 
  #   config.General.requestName = 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8'
  #   config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   config.Data.inputDataset   = '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM'
  #   config.Data.splitting = 'FileBased'
  #   crabCommand('submit', config = config)
  # 
  #   config.General.requestName = 'DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  #   config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   config.Data.inputDataset   = '/DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM'
  #   config.Data.splitting = 'FileBased'
  #   crabCommand('submit', config = config)
  # 
  #   ## Uncomment the following lines if you want to make DYJetsToMuMu MiNNLO plots
  # 
  #   # config.General.requestName = 'DYJetsToMuMu_M-50_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  #   # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   # config.Data.inputDataset   = '/DYJetsToMuMu_M-50_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM'
  #   # config.Data.splitting = 'FileBased'
  #   # crabCommand('submit', config = config)
  # 
  #   #  #########################################################################
  #   #  ### 2016APV
  #   #
  #   #  #config.General.requestName = 'DYJetsToLL_M-50_TuneCH3_13TeV-madgraphMLM-herwig7_2016APV'
  #   #  #config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   #  #config.Data.inputDataset   = '/DYJetsToLL_M-50_TuneCH3_13TeV-madgraphMLM-herwig7/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM'
  #   #  #config.Data.splitting = 'FileBased'
  #   #  #crabCommand('submit', config = config)
  #   #
  #   #  # /DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL16MiniAODAPV-106X_mcRun2_asymptotic_preVFP_v8-v1/MINIAODSIM
  #   #  # /DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
  #   #  # /DYJetsToMuMu_M-50_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM
  #   #
  #   #
  #   #  ### 2017
  #   #
  #   #  # config.General.requestName = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8'
  #   #  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   #  # config.Data.inputDataset   = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9_ext1-v1/MINIAODSIM'
  #   #  # config.Data.splitting = 'FileBased'
  #   #  # crabCommand('submit', config = config)
  #   #
  #   #  # config.General.requestName = 'DYJetsToLL_M-50_TuneCH3_13TeV-madgraphMLM-herwig7_UL17'
  #   #  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   #  # config.Data.inputDataset   = '/DYJetsToLL_M-50_TuneCH3_13TeV-madgraphMLM-herwig7/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
  #   #  # config.Data.splitting = 'FileBased'
  #   #  # crabCommand('submit', config = config)
  #   #
  #   #  # config.General.requestName = 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8'
  #   #  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   #  # config.Data.inputDataset   = '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
  #   #  # config.Data.splitting = 'FileBased'
  #   #  # crabCommand('submit', config = config)
  #   #
  #   #  # No sherpa sample for 17
  #   #  # config.General.requestName = 'DY01234jets_13TeV-sherpa'
  #   #  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   #  # config.Data.inputDataset   = '/DY01234jets_13TeV-sherpa/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
  #   #  # config.Data.splitting = 'FileBased'
  #   #  # crabCommand('submit', config = config)
  #   #
  #   #  # config.General.requestName = 'DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8'
  #   #  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   #  # config.Data.inputDataset   = '/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
  #   #  # config.Data.splitting = 'FileBased'
  #   #  # crabCommand('submit', config = config)
  #   #
  #   #  # config.General.requestName = 'DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  #   #  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   #  # config.Data.inputDataset   = '/DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
  #   #  # config.Data.splitting = 'FileBased'
  #   #  # crabCommand('submit', config = config)
  #   #
  #   #  # config.General.requestName = 'DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos'
  #   #  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   #  # config.Data.inputDataset   = '/DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
  #   #  # config.Data.splitting = 'FileBased'
  #   #  # crabCommand('submit', config = config)
  #   #
  #   #  ### 2018
  #   #
  #   #  # config.General.requestName = 'DYJetsToLL_M-50_TuneCH3_13TeV-madgraphMLM-herwig7_UL18'
  #   #  # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   #  # config.Data.inputDataset   = '/DYJetsToLL_M-50_TuneCH3_13TeV-madgraphMLM-herwig7/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM'
  #   #  # config.Data.splitting = 'FileBased'
  #   #  # crabCommand('submit', config = config)
  # 
  #   # /DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM is the only VALID powheg-pythia8 sample
  #   config.General.requestName = 'DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8'
  #   config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   config.Data.inputDataset   = '/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-NoPUEcalAging2023_102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
  #   config.Data.splitting = 'FileBased'
  #   crabCommand('submit', config = config)
  #   #
  #   #  # No sherpa sample for 18
  # 
  #   # herwig matchbox sample only exists for 2018
  #   config.General.requestName = 'DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7'
  #   config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  #   config.Data.inputDataset   = '/DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/MINIAODSIM'
  #   config.Data.splitting = 'FileBased'
  #   crabCommand('submit', config = config)



  ## ## PYTHIA8 samples 

  ## config.General.requestName = 'DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8-RunIIFall15MiniAODv1'
  ## config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## config.Data.inputDataset   = '/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv1-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
  ## config.Data.splitting = 'FileBased'
  ## crabCommand('submit', config = config)

  ## config.General.requestName = 'DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8-RunIIFall15MiniAODv2'
  ## config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## config.Data.inputDataset   = '/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
  ## config.Data.splitting = 'FileBased'
  ## crabCommand('submit', config = config)

  ## config.General.requestName = 'DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8-RunIISummer17MiniAOD'
  ## config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## config.Data.inputDataset   = '/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/MINIAODSIM'
  ## config.Data.splitting = 'FileBased'
  ## crabCommand('submit', config = config)

  ## # /DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-FlatPU8to42RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM # DELETED
  ## # /DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-FlatPU8to37HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM # DELETED


  ### Run-3

  ## config.General.requestName = 'Run3-DYto2L-4Jets_MLL-50_TuneCP5_13p6TeV_madgraphMLM-pythia8'
  ## config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## config.Data.inputDataset   = '/DYto2L-4Jets_MLL-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v3/MINIAODSIM'
  ## config.Data.splitting = 'FileBased'
  ## crabCommand('submit', config = config)

  ## config.General.requestName = 'Run3-DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8'
  ## config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## config.Data.inputDataset   = '/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v5/MINIAODSIM'
  ## config.Data.splitting = 'FileBased'
  ## crabCommand('submit', config = config)

  ## config.General.requestName = 'Run3-DYto2E_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8'
  ## config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## config.Data.inputDataset   = '/DYto2E_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8/Run3Summer22EEMiniAODv3-124X_mcRun3_2022_realistic_postEE_v1-v3/MINIAODSIM'
  ## config.Data.splitting = 'FileBased'
  ## crabCommand('submit', config = config)


  ## ###
  ## ## No Events
  ## # config.General.requestName = 'Run3-DYto2Mu-5Jets-2NLO3LO_MLL-40_TuneSherpaDef_13p6TeV_sherpaMEPS'
  ## # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## # config.Data.inputDataset   = '/DYto2Mu-5Jets-2NLO3LO_MLL-40_TuneSherpaDef_13p6TeV_sherpaMEPS/Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2/MINIAODSIM'
  ## # config.Data.splitting = 'FileBased'
  ## # crabCommand('submit', config = config)
  ## ##

  config.General.requestName = 'Run3-DYto2E-5Jets-2NLO3LO_MLL-40_TuneSherpaDef_13p6TeV_sherpaMEPS_2022postEE'
  config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  config.Data.inputDataset   = '/DYto2E-5Jets-2NLO3LO_MLL-40_TuneSherpaDef_13p6TeV_sherpaMEPS/Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2/MINIAODSIM'
  config.Data.splitting = 'FileBased'
  crabCommand('submit', config = config)

  config.General.requestName = 'Run3-DYto2E-5Jets-2NLO3LO_MLL-40_TuneSherpaDef_13p6TeV_sherpaMEPS_2023'
  config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  config.Data.inputDataset   = '/DYto2E-5Jets-2NLO3LO_MLL-40_TuneSherpaDef_13p6TeV_sherpaMEPS/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v15-v2/MINIAODSIM'
  config.Data.splitting = 'FileBased'
  crabCommand('submit', config = config)

  # ## NoEvents
  # # config.General.requestName = 'Run3-DYJetsToMuMu_TuneCP5_13p6TeV_powhegMiNNLO-pythia8-photos'
  # # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  # # config.Data.inputDataset   = '/DYJetsToMuMu_TuneCP5_13p6TeV_powhegMiNNLO-pythia8-photos/Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2/MINIAODSIM'
  # # config.Data.splitting = 'FileBased'
  # # crabCommand('submit', config = config)
  # ##

  config.General.requestName = 'Run3-DYJetsToMuMu_H2ErratumFix_TuneCP5_13p6TeV_powhegMiNNLO-pythia8-photos_PUAVE1'
  config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  config.Data.inputDataset   = '/DYJetsToMuMu_H2ErratumFix_TuneCP5_13p6TeV-powhegMiNNLO-pythia8-photos/Run3Summer23MiniAODv4-PUAVE1_130X_mcRun3_2023_realistic_v15-v2/MINIAODSIM'
  config.Data.splitting = 'FileBased'
  crabCommand('submit', config = config)

  config.General.requestName = 'Run3-DYJetsToMuMu_H2ErratumFix_TuneCP5_13p6TeV_powhegMiNNLO-pythia8-photos_PUAVE10'
  config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  config.Data.inputDataset   = '/DYJetsToMuMu_H2ErratumFix_TuneCP5_13p6TeV-powhegMiNNLO-pythia8-photos/Run3Summer23MiniAODv4-PUAVE10_130X_mcRun3_2023_realistic_v15-v2/MINIAODSIM'
  config.Data.splitting = 'FileBased'
  crabCommand('submit', config = config)

  ## ## Status: Production
  ## # config.General.requestName = 'Run3-DYto2L-2Jets-EWK_MLL-50_TuneCP5_13p6TeV_madgraph-pythia8'
  ## # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## # config.Data.inputDataset   = '/DYto2L-2Jets-EWK_MLL-50_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2/MINIAODSIM'
  ## # config.Data.splitting = 'FileBased'
  ## # crabCommand('submit', config = config)
  ## ##
  ## ###


  ## # config.General.requestName = 'Run3-DYToLL_M-50_TuneCP5_13p6TeV-pythia8'
  ## # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## # config.Data.inputDataset   = '/DYToLL_M-50_TuneCP5_13p6TeV-pythia8/Run3Summer22EEMiniAODv3-Poisson70KeepRAW_124X_mcRun3_2022_realistic_postEE_v1-v1/MINIAODSIM'
  ## # config.Data.splitting = 'FileBased'
  ## # crabCommand('submit', config = config)

  ## config.General.requestName = 'Run3-DYTo2L_MLL-50_TuneCP5_13p6TeV_pythia8-Run3Summer22MiniAODv3'
  ## config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## config.Data.inputDataset   = '/DYTo2L_MLL-50_TuneCP5_13p6TeV_pythia8/Run3Summer22MiniAODv3-124X_mcRun3_2022_realistic_v12-v2/MINIAODSIM'
  ## config.Data.splitting = 'FileBased'
  ## crabCommand('submit', config = config)

  ## config.General.requestName = 'Run3-DYTo2L_MLL-50_TuneCP5_13p6TeV_pythia8-Run3Summer22MiniAODv4'
  ## config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## config.Data.inputDataset   = '/DYTo2L_MLL-50_TuneCP5_13p6TeV_pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v1/MINIAODSIM'
  ## config.Data.splitting = 'FileBased'
  ## crabCommand('submit', config = config)

  ## # config.General.requestName = 'Run3-DYto2L_M-50_TuneCP5_13p6TeV_pythia8'
  ## # config.Data.outputDatasetTag = config.General.workArea + '___' + config.General.requestName + '___' + RunDate
  ## # config.Data.inputDataset   = '/DYto2L_M-50_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-KeepSi_130X_mcRun3_2023_realistic_postBPix_v2-v3/MINIAODSIM'
  ## # config.Data.splitting = 'FileBased'
  ## # crabCommand('submit', config = config)








