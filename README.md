# PART 1:
consists of:
- part1.py
- run_gmx2016.sh

all for single precision use

## part1.py:
Reads an .xtc-file, writes all the .gro-files and puts Link Atoms in the right
position.

files needed:
- .xtc-file
- .tpr-file
- .ndx-file with QM_region (debatable)

input:
- for 41-/43-systems: python3 part1.py 347 349 1683 1685 2139 2141 3251 22 2 27
- for 71-/73-systems: python3 part1.py 347 349 2104 2106 3235 3237 3251 22 27 2

input numbers stand for: C-alpha 1, C-beta 1, C-alpha 2, C-beta 2, C-alpha 3
C-beta 3, first solvent atom, group numbers of the relevant residues

The frames are saved as .gro-files in subdirectory 'frames'.
This script should be in the parent directory of 'frames'.
The location of the input-files is arbitrary.

Recommended input for the trjconv command (QM-Zone debatable):
cluster: 1 (Protein), center: 23 (QM-Zone), output: 0 (System)

## run_gmx2016.sh
run with 'source ./run_gmx2016.sh'

File to source the right GROMACS version to convert the modified .gro-files to a
new .xtc-file.
Converts the modified .gro-files to a new .xtc-file.


# PART 2
consists of:
- part2.sh

## part2.sh
Generates a .tpr-file for the QM rerun

files needed:
- .top-file -> changed for QM simulations
- .ndx-file -> changed for QM simulations
- new_frame0.gro
- full.xtc
- dftb_in.hsd
- .mdp-file
- single_submit.sh -> changed for rerun

input:
- ./part2.sh *.mdp *.gro *.top *.ndx

After the successfull generation of md.tpr: submit with:

qsub single_submit.sh


# Tested in:
tcb:/data/user1/HiWi_Maike/tool/test_5A_k5000_41/231213

hyd:/data/user1/MAIKE/tool/test_5A_k5000_41/231213

Test runs in tcb:/data/user1/HiWi_Maike/tool/test_5A_k5000_41/231231 without
index file
