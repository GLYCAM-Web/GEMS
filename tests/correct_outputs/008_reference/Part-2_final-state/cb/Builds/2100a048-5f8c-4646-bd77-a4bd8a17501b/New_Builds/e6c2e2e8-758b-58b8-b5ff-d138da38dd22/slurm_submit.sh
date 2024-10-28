#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/2100a048-5f8c-4646-bd77-a4bd8a17501b/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-2100a048-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/2100a048-5f8c-4646-bd77-a4bd8a17501b/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22/Minimize.bash
