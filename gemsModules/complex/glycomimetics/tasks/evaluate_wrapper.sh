#!/bin/bash
# We must use a bash wrapper so that change directory works as intended.

# Enable error handling
set -o pipefail

PROJECT_DIR=$1
PDB_FILE=$2

# Default webtool path is valid on harper
EVALUATE_EXE="${GEMS_GLYCOMIMETICS_WEBTOOL_PATH:=/programs/glycomimeticsWebtool}/internal/glycomimetics/validation/main.exe"

if [ ! -f $EVALUATE_EXE ]; then
    exit 2
fi

# Set core file size to 0 to prevent core dumps
ulimit -c 0

# Run with timeout to prevent infinite hangs
timeout 600 $EVALUATE_EXE $PDB_FILE $PROJECT_DIR/available_atoms.txt > $PROJECT_DIR/evaluation.log 2> $PROJECT_DIR/evaluate.err
EXIT_CODE=$?

# Check for different failure scenarios
case $EXIT_CODE in
    0)  # Success
        exit 0
        ;;
    124) # timeout occurred
        echo "Process timed out after 600 seconds" >> $PROJECT_DIR/evaluate.err
        exit 1
        ;;
    139) # Segmentation fault (SIGSEGV)
        echo "Segmentation fault occurred" >> $PROJECT_DIR/evaluate.err
        exit 1
        ;;
    134) # SIGABRT
        echo "Process aborted" >> $PROJECT_DIR/evaluate.err
        exit 1
        ;;
    *)  # Other error
        echo "Process failed with exit code $EXIT_CODE" >> $PROJECT_DIR/evaluate.err
        exit 1
        ;;
esac