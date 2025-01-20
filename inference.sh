#!/bin/bash

# 1. Set environment variables
INPUT="$1"

echo $INPUT
export HOME_DIR="/hkfs/work/workspace/scratch/fr_dm339-rfaa"
export ROSETTA_DIR="$HOME_DIR/RoseTTAFold-All-Atom"
export SCRIPT_PATH="rf2aa.run_inference"
export INPUT_DIR="$HOME_DIR/$INPUT"
export YAML_FILE="$ROSETTA_DIR/rf2aa/config/inference/$INPUT.yaml"  # Path to the concrete YAML file to override

mkdir -p LOGS

# 2. Get all unique IDs (assuming naming convention: {ID}_protein.fasta and {ID}_rna.fasta)
IDs=($(ls $INPUT_DIR | grep '_protein.fasta' | sed 's/_protein.fasta//'))

# 3. Iterate through IDs (each iteration processes one pair)
for ID in "${IDs[@]}"; do
    # Set environment variables for the current iteration
    export PROTEIN_FASTA="$INPUT_DIR/${ID}_protein.fasta"
    export RNA_FASTA="$INPUT_DIR/${ID}_rna.fasta"
    export JOB_ID="$ID"

    START_TIME=$(date +%s)

# 4. Override the YAML file
    python -c "
import yaml
with open('${YAML_FILE}', 'r') as file:
    config = yaml.safe_load(file)

# Modify the YAML structure
config['job_name'] = '${JOB_ID}'
config['protein_inputs']['A']['fasta_file'] = '${PROTEIN_FASTA}'
config['na_inputs']['B']['fasta'] = '${RNA_FASTA}'

# Write back to the same YAML file
with open('${YAML_FILE}', 'w') as file:
    yaml.dump(config, file)
    "

# 5. Run the Python script with the overridden YAML
    cd $ROSETTA_DIR
    python -m $SCRIPT_PATH --config-name $INPUT

    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    echo "Iteration for ID: ${ID} completed in ${DURATION} seconds"
done
