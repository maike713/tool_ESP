#!/bin/bash

# source GROMACS 2016.4
source /usr/local/run/gromacs-2016.4-plumed-2.3.4-sse41/bin/GMXRC

# command to get an .xtc-file
gmx trjcat -f full.gro -o full.xtc
