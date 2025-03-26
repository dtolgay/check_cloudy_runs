#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --time=23:00:00
#SBATCH --job-name=check_status_of_cloudy_jobs
#SBATCH --output=check_status_of_cloudy_jobs.out
#SBATCH --error=check_status_of_cloudy_jobs.err

# Change to the directory where the job was submitted
cd $SLURM_SUBMIT_DIR

# Load necessary modules
module purge
ml python/3.11.5

# Write the output real time to a file
python -u check_status_cloudy_jobs.py > output.log 2>&1
# python -u rsync_files.py > rsync_output.log 2>&1