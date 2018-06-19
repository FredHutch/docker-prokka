#!/usr/bin/env python3

import os
import sys
import uuid
import shutil
import logging
import argparse
import traceback
import subprocess


def exit_and_clean_up(temp_folder):
    """Log the error messages and delete the temporary folder."""
    # Capture the traceback
    logging.info("There was an unexpected failure")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    for line in traceback.format_tb(exc_traceback):
        logging.info(line)

    # Delete any files that were created for this sample
    logging.info("Removing temporary folder: " + temp_folder)
    shutil.rmtree(temp_folder)

    # Exit
    logging.info("Exit type: {}".format(exc_type))
    logging.info("Exit code: {}".format(exc_value))
    sys.exit(exc_value)


def run_cmds(commands, retry=0, catchExcept=False, stdout=None):
    """Run commands and write out the log, combining STDOUT & STDERR."""
    logging.info("Commands:")
    logging.info(' '.join(commands))
    if stdout is None:
        p = subprocess.Popen(commands,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
    else:
        with open(stdout, "wt") as fo:
            p = subprocess.Popen(commands,
                                 stderr=subprocess.PIPE,
                                 stdout=fo)
            stdout, stderr = p.communicate()
        stdout = False
    exitcode = p.wait()
    if stdout:
        logging.info("Standard output of subprocess:")
        for line in stdout.decode("latin-1").split('\n'):
            logging.info(line)
    if stderr:
        logging.info("Standard error of subprocess:")
        for line in stderr.decode("latin-1").split('\n'):
            logging.info(line)

    # Check the exit code
    if exitcode != 0 and retry > 0:
        msg = "Exit code {}, retrying {} more times".format(exitcode, retry)
        logging.info(msg)
        run_cmds(commands, retry=retry - 1)
    elif exitcode != 0 and catchExcept:
        msg = "Exit code was {}, but we will continue anyway"
        logging.info(msg.format(exitcode))
    else:
        assert exitcode == 0, "Exit code {}".format(exitcode)


def set_up_sra_cache_folder(temp_folder):
    """Set up the fastq-dump cache folder within the temp folder."""
    logging.info("Setting up fastq-dump cache within {}".format(temp_folder))

    # Now make a folder within the temp folder
    temp_cache = os.path.join(temp_folder, "sra")
    assert os.path.exists(temp_cache) is False
    os.mkdir(temp_cache)

    # Alter the configuration options for fastq-dump
    run_cmds([
        "vdb-config", 
        "--root", 
        "-s", 
        "/repository/user/main/public/root={}".format(temp_folder)
    ], catchExcept=True)


def get_sra(accession, temp_folder):
    """Get the FASTQ for an SRA accession."""
    logging.info("Downloading {} from SRA".format(accession))

    local_path = os.path.join(temp_folder, accession + ".fastq")
    logging.info("Local path: {}".format(local_path))

    # Download via fastq-dump
    logging.info("Downloading via fastq-dump")
    run_cmds([
        "prefetch", accession
    ])
    # Output the _1.fastq and _2.fastq files
    run_cmds([
        "fastq-dump", "--split-files",
        "--defline-seq", "@$ac.$si.$sg/$ri",
        "--defline-qual", "+",
        "--outdir", temp_folder, accession
    ])

    # Remove the cache file, if any
    cache_fp = "/root/ncbi/public/sra/{}.sra".format(accession)
    if os.path.exists(cache_fp):
        logging.info("Removing {}".format(cache_fp))
        os.unlink(cache_fp)

    # Return all of the files that were downloaded
    logging.info("Done fetching " + accession)
    
    # Combine all of the files into a single file
    local_fastq_fp = os.path.join(temp_folder, accession)
    logging.info("Concatenating all downloaded files into a single FASTQ ({})".format(
        local_fastq_fp
    ))

    run_cmds(
        [
            "cat"
        ] + [
            os.path.join(temp_folder, fp)
            for fp in os.listdir(temp_folder)
            if fp.startswith(accession) and fp.endswith(".fastq")
        ], 
        stdout=local_fastq_fp
    )

    return local_fastq_fp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Download a set of reads from SRA and sketch with finch-rs.""")

    parser.add_argument("--accession",
                        type=str,
                        required=True,
                        help="""SRA accession to download.""")
    parser.add_argument("--sketch-size",
                        type=int,
                        required=True,
                        help="""Number of minmers to use in the sketch.""")
    parser.add_argument("--output-path",
                        type=str,
                        required=True,
                        help="""S3 path (key) to upload sketch file [.sk].""")
    parser.add_argument("--temp-folder",
                        type=str,
                        default='/share',
                        help="Folder used for temporary files.")

    args = parser.parse_args()

    # Make sure that the output path ends with .fastq.gz
    assert args.output_path.endswith(".sk")

    # If the output folder is not S3, make sure it exists locally
    if args.output_path.startswith("s3://") is False:
        output_folder = "/".join(args.output_path.split("/")[:-1])
        assert os.path.exists(output_folder), "Output folder does not exist"

    # Make a temporary folder for all files to be placed in
    temp_folder = os.path.join(args.temp_folder, str(uuid.uuid4())[:8])
    assert os.path.exists(temp_folder) is False
    os.mkdir(temp_folder)

    # Set up logging
    log_fp = os.path.join(temp_folder, args.accession + ".log")
    logFormatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s [run_finch.py] %(message)s'
    )
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    # Write to file
    fileHandler = logging.FileHandler(log_fp)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    # Also write to STDOUT
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    # Set up the NCBI fastq-dump cache folder within the temp folder
    try:
        set_up_sra_cache_folder(temp_folder)
    except:
        exit_and_clean_up(temp_folder)

    # Download the SRA data
    try:
        local_fastq_fp = get_sra(args.accession, temp_folder)
    except:
        exit_and_clean_up(temp_folder)

    # Sketch with finch-rs
    sketch_fp = os.path.join(temp_folder, "output.sk")
    try:
        run_cmds([
            "finch",
            "sketch",
            "-o",
            sketch_fp,
            "-n",
            str(args.sketch_size)            
        ] + [local_fastq_fp])
        assert os.path.exists(sketch_fp)
    except:
        exit_and_clean_up(temp_folder)

    if args.output_path.startswith("s3://"):
        # Upload FASTQ to S3 folder
        try:
            run_cmds(["aws", "s3", "cp", "--sse", "AES256",
                      sketch_fp, args.output_path])
        except:
            exit_and_clean_up(temp_folder)

        # Upload logs to S3 folder
        try:
            run_cmds(["aws", "s3", "cp", "--sse",
                      "AES256", log_fp, args.output_path.replace(".sk", ".log")])
        except:
            exit_and_clean_up(temp_folder)
    else:
        # Move FASTQ to local folder
        try:
            run_cmds(["mv", sketch_fp, args.output_path])
        except:
            exit_and_clean_up(temp_folder)

        # Move logs to local folder
        try:
            run_cmds(["mv", log_fp, args.output_path.replace(".sk", ".log")])
        except:
            exit_and_clean_up(temp_folder)

    # Delete any files that were created for this sample
    logging.info("Removing temporary folder: " + temp_folder)
    shutil.rmtree(temp_folder)
