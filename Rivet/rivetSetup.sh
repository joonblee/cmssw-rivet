#!/bin/bash
for group in SMP TOP; do
  export RIVET_REF_PATH="$CMSSW_BASE/src/Rivet/$group/data${RIVET_REF_PATH:+:$RIVET_REF_PATH}"
  export RIVET_INFO_PATH="$CMSSW_BASE/src/Rivet/$group/data${RIVET_INFO_PATH:+:$RIVET_INFO_PATH}"
done
