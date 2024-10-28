#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/6e4d1b06-18c9-4f3e-95d2-e9fc098aeac8/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-6e4d1b06-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/6e4d1b06-18c9-4f3e-95d2-e9fc098aeac8/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22/Minimize.bash
