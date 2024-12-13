# PSIPRED Batch Processing Script

## Overview

This script automates the process of predicting protein secondary structure using PSIPRED (Position-Specific Iterated BLAST) for multiple FASTA sequence files. It combines PSI-BLAST and PSIPRED tools to generate detailed secondary structure predictions.

## Prerequisites

### Software Requirements
- tcsh shell
- BLAST+ toolkit
- PSIPRED package
- Sequence database (recommended: UniRef90)

### Recommended System Configuration
- Linux/Unix environment
- Sufficient disk space (5-10 GB for databases)
- Multi-core processor
- Minimum 16 GB RAM

## Installation Steps

1. **Install Dependencies**
   ```bash
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install tcsh blast-legacy psipred
   ```

2. **Download Sequence Database**
   - Download UniRef90 from [UniProt](https://www.uniprot.org/uniref)
   - Ensure database is formatted for BLAST: 
     ```bash
     makeblastdb -in uniref90.fasta -dbtype prot
     ```

3. **Prepare Directory Structure**
   ```
   project_root/
   ├── bin/                 # PSIPRED executables
   ├── data/                # PSIPRED weight files
   ├── input_sequences/     # Input FASTA files
   ├── output_results/      # Prediction output
   └── run_psipred.tcsh     # Processing script
   ```

## Configuration

Edit `run_psipred.tcsh` and update the following variables:

- `dbname`: Full path to UniRef90 database
- `ncbidir`: Path to BLAST executable directory
- `execdir`: Path to PSIPRED executable directory
- `datadir`: Path to PSIPRED weight files

## Usage

### Single File Processing
```bash
tcsh run_psipred.tcsh input_sequences/example.fasta
```

### Batch Processing
```bash
tcsh run_psipred.tcsh
```

## Output Files

For each input FASTA file, the script generates:
- `*.ss2`: Detailed secondary structure prediction
- `*.ss`: Initial secondary structure prediction
- `*.horiz`: Human-readable prediction summary
- `*.blast`: PSI-BLAST log file

## Output Interpretation

### .ss2 File Format
```
Residue  AA  Observed  Predicted  Confidence
1        M   -         C          9
2        A   -         C          8
...
```
- **AA**: Amino Acid
- **Observed**: Experimental structure (if available)
- **Predicted**: Predicted structure (H: Helix, E: Sheet, C: Coil)
- **Confidence**: Prediction confidence (0-9 scale)

## Troubleshooting

1. **Permission Issues**
   ```bash
   chmod +x run_psipred.tcsh
   ```

2. **Database Path Errors**
   - Verify full, absolute paths
   - Ensure database is properly formatted

3. **Executable Permissions**
   ```bash
   chmod +x bin/psipred
   chmod +x bin/psipass2
   ```

## Performance Optimization

- Use job scheduling systems like SLURM for large datasets
- Increase PSI-BLAST iterations for more sensitive predictions
- Utilize multi-core processing

## Limitations

- Accuracy depends on sequence similarity in the database
- Most effective for proteins with homologous sequences
- May struggle with novel or highly divergent proteins

## Citations

If you use this in research, please cite:
- PSIPRED: Jones, D.T. (1999). Protein Secondary Structure Prediction Based on Position-Specific Scoring Matrices. J. Mol. Biol.
- UniRef: Suzek et al. (2015). UniRef clusters: a comprehensive and scalable alternative for improving sequence similarity searches.

## License

MIT License

## Contributing

Contributions, issues, and feature requests are welcome!

---
