#!/bin/bash

# source GROMACS 2016.4
source_gmx="source /usr/local/run/gromacs-2016.4-plumed-2.3.4-sse41/bin/GMXRC"
if ! $source_gmx; then
    echo "Error executing command: $source_gmx"
    exit 1
fi

echo "Successfully sourced GROMACS v2016.4"

# command to get an .xtc-file
make_xtc="gmx trjcat -f full.gro -o full.xtc"
if ! $make_xtc; then
    echo "Error executing command: $make_xtc"
    exit 1
fi

echo "Successfully generated full.xtc"
