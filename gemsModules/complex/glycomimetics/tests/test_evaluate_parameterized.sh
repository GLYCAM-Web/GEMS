#!/bin/bash

cd $GEMSHOME

userdata_dir=${1:-"/website/userdata/complex/gm"}
TEST_JSON=${3:-"gemsModules/complex/glycomimetics/tests/inputs/explicit_evaluate-parameterized.json"}

PDB_DIR=gemsModules/complex/glycomimetics/tests/pdbs
EXPECTED_OUTPUTS=gemsModules/complex/glycomimetics/tests/expected_outputs
FAILED_OUTPUTS=gemsModules/complex/glycomimetics/tests/failed_outputs-git-ignore-me
if [ ! -d $FAILED_OUTPUTS ]; then
    mkdir $FAILED_OUTPUTS
fi

# Get PDB files
PDBS=($(find $PDB_DIR -type f -name "*.pdb"))

# Try to match each PDB with its output, warn if missing
PAIRS=()
ignored=()
for pdb in "${PDBS[@]}"; do
    base=$(basename "$pdb" .pdb)
    expected="${EXPECTED_OUTPUTS}/${base}.json"
    
    if [[ ! -f "$expected" ]]; then
        echo "Warning: No matching output found for $pdb"
        ignored+=($pdb)
    else
        PAIRS+=("$pdb:$expected")
    fi
done

# replace ${PDB_FILE} with the pdb file
failures=()
for pair in "${PAIRS[@]}"; do
    IFS=':' read -r -a pair <<< "$pair"
    pdb_file=${pair[0]}
    echo "Running test for $(basename $pdb_file)"

    expected_output=${pair[1]}
    eval_request=$(cat $TEST_JSON | sed "s|\${PDB_FILE}|$pdb_file|g" | sed "s|\${EXPECTED_OUTPUT}|$expected_output|g")
    eval_response=$(echo $eval_request | ./bin/delegate)
    if [ $? -ne 0 ]; then
        echo "Error: Failed to run test for $pdb_file"
        failures+=($pdb_file)
    fi

    echo "See this test's project directory at: $(echo ${eval_response} | python tests/utilities/json_ripper.py project.project_dir)"

    # check if the output is as expected
    output=$(echo $eval_response | python tests/utilities/json_ripper.py entity.responses.evaluation_of_pdb)
    diff <(echo $output) <(cat $expected_output)
    if [ $? -ne 0 ]; then
        echo "Error: Output for this test does not match expected output"
        failures+=($pdb_file)
        # dump failed response
        echo $eval_response > $FAILED_OUTPUTS/git-ignore-me-$(basename $expected_output)
    else
        echo "Test passed."
    fi
done

if [ ${#ignored[@]} -ne 0 ]; then
    echo "Ignored tests for:"
    for ignore in "${ignored[@]}"; do
        echo $ignore
    done
fi

if [ ${#failures[@]} -ne 0 ]; then
    echo "Failed tests for:"
    for failure in "${failures[@]}"; do
        echo $failure
    done
    exit 1
else
    # if no pairs we didn't run any tests
    if [ ${#PAIRS[@]} -eq 0 ]; then
        echo "No tests to run"
    else
        echo "All tests passed"
    fi
fi

