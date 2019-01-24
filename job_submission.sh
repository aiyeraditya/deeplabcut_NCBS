#!/bin/bash -l
#$ -S /bin/bash
#$ -cwd
#$ -V

## Change the name below (after -N) to suite your requirement
#$ -N DeepabCut_Training

# Change the number of cores demanded (after orte) to suite your code-run requirement
#$ -pe mpirun 32

## set the queue depending on Job run time.
#$ -q all.q

#$ -l h_vmem=10G

## Email address to send email to
#$ -M aiyer.aditya@gmail.com

## To send email when job ends or aborts
#$ -m ea

echo "Starting MPI job at: " `date`
echo "Starting MPI job on: " `hostname`
echo "Total cores demanded: " $NSLOTS
echo "Job name given: " $JOB_NAME
echo "Job ID: " $JOB_ID
echo "Starting MPI job..."

## Change the executable to match your path and executable

/home/sane/adityaiyer/script.sh

exit 0
