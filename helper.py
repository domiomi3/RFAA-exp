import os
import argparse
import shutil

import pandas as pd

from math import ceil


def csv_to_fasta(path, dir):
    col_names = ["PDBId","ProteinSequence", "RNAModified", "RNASequence"]
    df = pd.read_csv(path, sep=";", usecols=[0,1,2,3])
    
    if not os.path.exists(dir):
        os.mkdir(dir)

    for index, row in df.iterrows():
        if row['RNAModified'] == '[]':
            prot_fname = f"{row['PDBId']}_protein.fasta"
            rna_fname = f"{row['PDBId']}_rna.fasta"

            with open(os.path.join(dir, prot_fname), 'w') as pf:
                pf.write(f">{row['PDBId']}\n{row['ProteinSequence']}\n")
            
            with open(os.path.join(dir, rna_fname), 'w') as rf:
                rf.write(f">{row['PDBId']}\n{row['RNASequence']}\n")

def divide_files_into_dirs(input_dir, num_dirs=5):
    # Ensure input directory exists
    if not os.path.isdir(input_dir):
        raise ValueError(f"Input directory '{input_dir}' does not exist.")

    # Group files by ID (e.g., {ID}_protein.fasta and {ID}_rna.fasta)
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    file_groups = {}
    for file in files:
        # Extract the ID by splitting on the first underscore
        id_part = file.split('_', 1)[0]
        file_groups.setdefault(id_part, []).append(file)

    # Convert grouped files into a list of groups
    grouped_files = list(file_groups.values())

    # Calculate the number of groups per subdirectory
    num_groups = len(grouped_files)
    groups_per_dir = ceil(num_groups / num_dirs)

    # Create subdirectories and distribute groups
    input_dir_name = os.path.basename(input_dir.rstrip(os.sep))
    parent_dir = os.path.dirname(input_dir.rstrip(os.sep))

    for i in range(1, num_dirs + 1):
        sub_dir_name = f"{input_dir_name}_{i}"
        sub_dir_path = os.path.join(parent_dir, sub_dir_name)

        # Create subdirectory if it doesn't exist
        os.makedirs(sub_dir_path, exist_ok=True)

        # Get the groups for this subdirectory
        start_idx = (i - 1) * groups_per_dir
        end_idx = min(start_idx + groups_per_dir, num_groups)
        groups_to_move = grouped_files[start_idx:end_idx]

        # Move files in each group to the subdirectory
        for group in groups_to_move:
            for file in group:
                src = os.path.join(input_dir, file)
                dst = os.path.join(sub_dir_path, file)
                shutil.move(src, dst)

        print(f"Moved {sum(len(group) for group in groups_to_move)} files to {sub_dir_path}")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str)
    parser.add_argument("--dir", type=str)

    args = parser.parse_args()

    csv_to_fasta(args.path, args.dir)

    # input_dir = "check"
    # divide_files_into_dirs(input_dir)