#!/bin/bash 
#$ -cwd -pe nproc 1 -N rerun

#export PATH=$PATH/home/jboeser/miniconda3
#source /home/jboeser/miniconda3/etc/profile.d/conda.sh
#conda activate python3


source /usr/local/run/gromacs-dftbplus-machine-learning/bin/GMXRC

export OMP_NUM_THREADS=1
export GMX_QMMM_VARIANT=1 # defines type of electrostatics 0= ewald , 1= ewald mesh 2-4= different cut-offs
export GMX_DFTB_ESP=1
export GMX_DFTB_CHARGES=1
export GMX_DFTB_QM_COORD=1


current=$PWD
# add gll topol to cwd
workdir=/scratch/$USER/GMX_$JOB_ID

mkdir -vp $workdir
cp dftb_in.hsd md.tpr full.xtc $workdir
cd $workdir

gmx_d mdrun -s md.tpr -rerun full.xtc
#gmx_d mdrun -ntomp 1 -deffnm md -plumed plumed.dat 
#gmx_d mdrun -ntomp 1 -deffnm md 
#gmx_d mdrun -ntomp 1 -deffnm metad_$i -cpi metad_$i.cpt -plumed plumed_$i.dat -noappend &>/dev/null & 

wait

cd $current

rsync -avruz $workdir/ .
