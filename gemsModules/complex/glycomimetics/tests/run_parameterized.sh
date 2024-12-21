#!/bin/bash

# i.e. /programs/gems/gemsModules/complex/glycomimetics/tests/pdbs/1_3ubn_clean_with_H.pdb
pdb_file=$1
TEST_JSON=${2:-"/programs/gems/gemsModules/complex/glycomimetics/tests/inputs/explicit_evaluate-parameterized.json"}
eval_request=$(cat $TEST_JSON | sed "s|\${PDB_FILE}|$pdb_file|g" | sed "s|\${EXPECTED_OUTPUT}|$expected_output|g")
echo $eval_request | ./bin/delegate