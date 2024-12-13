#!/bin/tcsh

# Strict error handling
set -e

# Configuration Management
set input_dir = "input_sequences"
set output_dir = "output_results"

# Configurable paths with environment variable fallback
set dbname = "$UNIREF_DB"     # Allow environment variable override
set ncbidir = "$BLAST_PATH"   # Allow environment variable override
set execdir = "./bin"
set datadir = "./data"

# Logging setup
set log_file = "$output_dir/psipred_batch.log"

# Validation functions
if (! -d $input_dir) then
    echo "Error: Input directory $input_dir does not exist!"
    exit 1
endif

# Create output directory if not exists
if (! -d $output_dir) mkdir -p $output_dir

# Logging function
function log_message() 
    echo "[`date +'%Y-%m-%d %H:%M:%S'`] $1" | tee -a $log_file
end

# Validate required tools
foreach tool (blastpgp makemat psipred psipass2)
    if (! -x "$ncbidir/$tool" && ! -x "$execdir/$tool") then
        log_message "Error: $tool not found in $ncbidir or $execdir"
        exit 1
    endif
end

# Main processing loop
set file_count = 0
foreach file ($input_dir/*.fasta)
    @ file_count++
    set basename = $file:r
    set rootname = $basename:t
    set tmproot = `mktemp -u psitmp.XXXXXX`

    log_message "Processing file: $file (File $file_count)"

    \cp -f $file $tmproot.fasta

    # PSI-BLAST with improved error handling and logging
    log_message "Running PSI-BLAST..."
    $ncbidir/blastpgp -b 0 -j 3 -h 0.001 -v 5000 -d $dbname -i $tmproot.fasta -C $tmproot.chk >& $tmproot.blast
    if ($status != 0) then
        log_message "Error running PSI-BLAST for $file! Skipping..."
        continue
    endif

    # Matrix generation
    log_message "Generating position-specific scoring matrix..."
    echo $tmproot.chk > $tmproot.pn
    echo $tmproot.fasta > $tmproot.sn
    $ncbidir/makemat -P $tmproot
    if ($status != 0) then
        log_message "Error running makemat for $file! Skipping..."
        continue
    endif

    # PSIPRED prediction
    log_message "Running PSIPRED prediction..."
    $execdir/psipred $tmproot.mtx $datadir/weights.dat $datadir/weights.dat2 $datadir/weights.dat3 > $output_dir/$rootname.ss
    $execdir/psipass2 $datadir/weights_p2.dat 1 1.0 1.0 $output_dir/$rootname.ss2 $output_dir/$rootname.ss > $output_dir/$rootname.horiz
    if ($status != 0) then
        log_message "Error running PSIPRED for $file! Skipping..."
        continue
    endif

    # Cleanup
    \rm -f $tmproot.*
    log_message "Completed processing $file"
end

log_message "Batch processing complete! Processed $file_count files."
log_message "Output saved in $output_dir. Check $log_file for details."
