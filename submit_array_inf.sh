#!/bin/bash
#SBATCH --partition=accelerated-h100
#SBATCH --job-name=rfaa_missing
#SBATCH --output=LOGS/%x_%A_%a.out
#SBATCH --error=LOGS/%x_%A_%a.err
#SBATCH --time=2:00:00
#SBATCH --gres=gpu:1
#SBATCH --array=0-4

source /home/hk-project-p0021863/fr_dm339/mambaforge/etc/profile.d/conda.sh

conda activate RFAA 

# List of input directories
INPUT_DIRS=(
    "input_1"
    "input_2"
    "input_3"
    "input_4"
    "input_5"
)

# Get the input directory for this array task
INPUT_DIR="${INPUT_DIRS[$SLURM_ARRAY_TASK_ID]}"

echo "Running inference for INPUT_DIR: $INPUT_DIR"

# Your inference script or logic here
bash inference.sh "$INPUT_DIR"
