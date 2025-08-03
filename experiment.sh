#!/bin/bash
#SBATCH --output=/home/members/morita/Sequence_Analysis_Algorithms/job%j.out  # where to store the output (%j is the JOBID)
#SBATCH --error=/home/members/morita/Sequence_Analysis_Algorithms/job%j.err  # where to store error messages
#SBATCH --mem=80G
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:0
#CommentSBATCH --exclude=habaki  # you can exclude specified nodes here; Commented out now
#SBATCH --nodelist=habaki  # you can specify nodes where the job should be run; Ditto

PROJECT_ROOT=$(git rev-parse --show-toplevel)

echo "Running on node: $(hostname)"
echo "In directory: $(pwd)"
echo "Starting on: $(date)"
echo "SLURM_JOB_ID: ${SLURM_JOB_ID}"

cd $PROJECT_ROOT/algorithms

for f in {1..5}; do
    for e in {6..11}; do
        uv run text_generate.py "$e" "$f"
        uv run fft_algorithm.py
        uv run KMP_algorithm.py
        # uv run boyer_moore_algorithm.py
    done
done 

# Send more noteworthy information to the output log
echo "Finished at: $(date)"

# End the script with exit code 0
exit 0