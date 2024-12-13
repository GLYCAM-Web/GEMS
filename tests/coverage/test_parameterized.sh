#!/bin/bash

cd $GEMSHOME

userdata_dir=${1:-"/website/userdata/complex/gm"}
PREP_JSON=${2:-"gemsModules/complex/glycomimetics/tests/inputs/explicit_build.test.json"}
TEST_JSON=${3:-"gemsModules/complex/glycomimetics/tests/inputs/explicit_status-parameterized.json"}

# project_dir=$(./bin/delegate $PREP_JSON | python tests/utilities/json_ripper.py project.project_dir)
# pUUID=$(basename $project_dir)
# sleep 1
pUUID="f86dc7e1-281a-445f-9944-c52927001e6a"
echo "Project UUID: $pUUID"
echo

# gemsModules/complex/glycomimetics/tests/inputs/explicit_status-parameterized.json
# replace ${pUUID} with the pUUID 
status_request=$(sed "s/\${pUUID}/$pUUID/g" $TEST_JSON)
echo $status_request
echo 

# run the test
echo $status_request | ./bin/delegate
