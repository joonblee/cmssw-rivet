#!/bin/bash
echo ""
echo "[SYSTEM] Print setup"
echo "Host name: $(hostname)"
echo "PWD: $(pwd)"
echo ""

#source /cvmfs/cms.cern.ch/cmsset_default.sh
#cd $CMSSW_BASE/src
#eval `scram runtime -sh`

export RIVET_ANALYSIS_PATH="${RIVET_ANALYSIS_PATH:+$RIVET_ANALYSIS_PATH:}$PWD"
#source $CMSSW_BASE/src/Rivet/rivetSetup.sh
#rivet-build RivetNonIsoPheno.so RivetNonIsoPheno.cc

echo ""
echo "[SYSTEM] Print setup"
echo "RIVET_INFO_PATH = $RIVET_INFO_PATH"
echo "RIVET_ANALYSIS_PATH = $RIVET_ANALYSIS_PATH"
which rivet
which yodamerge
echo ""

echo ""
echo "[SYSTEM] Start running..."
# cmsRun rivet_NonIsoPheno_cfg.py maxEvents=100 yodafile=output.yoda
cmsRun -j FrameworkJobReport.xml PSet.py
echo "[SYSTEM] Done"
echo ""
