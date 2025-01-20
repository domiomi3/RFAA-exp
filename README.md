Please follow the instructions from RoseTTAFold-All-Atom/README.md to install all necessary modules.

To convert .csv file containing RNA-protein pairs into individual FASTA files of the sequences run the following command
```
python helper.py --path path/to/csv --dir output/dir/inside/RoseTTAFold/folder
```

To run a single job refer to inference.sh.

To run an array, refer to submit_array_inf.sh.