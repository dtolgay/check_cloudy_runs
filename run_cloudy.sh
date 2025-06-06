#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=40
#SBATCH --time=23:00:00
#SBATCH --job-name=run_cloudy
#SBATCH --output=run_cloudy.out
#SBATCH --error=run_cloudy.err

# Limit threading in Python, R, etc.
export OMP_NUM_THREADS=1


# Load necessary modules
module purge 
module load NiaEnv/2019b gnu-parallel


### Specify the file containing the list of directories and set the parallel job count
# Change to the working directory
cd /scratch/m/murray/dtolgay/cloudy_runs/z_0/cr_1_CO87_CII_H_O3/cr_1_CO87_CII_H_O3_metallicity_above_minus_2 || exit 1
running_directories_file_name=abundance_emissivity_files_not_found.txt
number_of_parallel_jobs=100

# # Use GNU Parallel to process each directory
# parallel --jobs "$number_of_parallel_jobs" --joblog "slurm-$SLURM_JOBID.log" '
#     cd /scratch/m/murray/dtolgay/cloudy_runs/z_0/cr_1_CO87_CII_H_O3/cr_1_CO87_CII_H_O3_metallicity_above_minus_2 || exit 1
#     cd {} || exit 1
#     if [[ ! -f "started12.txt" ]]; then
#         touch "started12.txt"
#         cloudy *.in && touch "success.txt"
#     fi
# ' :::: "$running_directories_file_name"


# Use GNU Parallel to process each directory
parallel --jobs "$number_of_parallel_jobs" --joblog "slurm-$SLURM_JOBID.log" '
    cd /scratch/m/murray/dtolgay/cloudy_runs/z_0/cr_1_CO87_CII_H_O3/cr_1_CO87_CII_H_O3_metallicity_above_minus_2 || exit 1
    cd {} || exit 1
    if [[ ! -f "started12.txt" ]]; then
        touch "started12.txt"
        
        # Start cloudy in the background
        cloudy *.in &
        PID=$!
        
        # Monitor memory usage
        while kill -0 $PID 2>/dev/null; do
            if [[ -f /proc/$PID/status ]]; then
                mem_usage=$(awk "/VmRSS/ {print \$2}" /proc/$PID/status)  # Memory usage in KB
                
                if [[ "$mem_usage" -gt 10485760 ]]; then  # Exceeds 10 GB (10 * 1024 * 1024 KB)
                    echo "Killing $PID due to excessive memory usage: $mem_usage KB" >> memory_exceeded.log
                    kill -9 $PID
                    exit 1  # Exit the parallel process for this directory
                fi
            fi
            sleep 5  # Check every 5 seconds
        done

        wait $PID && touch "success.txt"
    fi
' :::: "$running_directories_file_name"

