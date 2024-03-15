#!/bin/bash

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
