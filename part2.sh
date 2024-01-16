#!/bin/bash


# files needed:
# .top -> changed for qm simulations
# .ndx -> newly generated and changed for qm qimulations
# new_frame0.gro
# full.xtc
# dftb_in.hsd
# .mdp
# single_submit.sh -> changed for rerun


## input:
# ./part2.sh *.mdp *.gro *.top *.ndx


if [ "$#" -ne 4 ]; then
	echo "Usage: $0 <.mdp-file> <.gro-file> <.top-file> <.ndx-file>"
	exit 1
fi

mdp="$1"
gro="$2"
top="$3"
ndx="$4"

# generate the .tpr file
make_tpr="gmx_d grompp -f $mdp -c $gro -p $top -n $ndx -o md.tpr -maxwarn 1"
if ! $make_tpr; then
	echo "Error executing command: $make_tpr"
	exit 1
fi

echo "Successfully generated md.tpr"
