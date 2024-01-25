# PART 1:
consists of:
- part1.py
- part1_mod.py
- run_gmx2016.sh

all for single precision use

## part1.py:
Reads an .xtc-file, writes all the .gro-files and puts Link Atoms in the right
position.

files needed:
- .xtc-file
- .tpr-file

input:
- for 41-/43-systems: python3 part1.py 347 349 1683 1685 2139 2141 3251 22 2 27
- for 71-/73-systems: python3 part1.py 347 349 2104 2106 3235 3237 3251 22 27 2

input numbers stand for: C-alpha 1, C-beta 1, C-alpha 2, C-beta 2, C-alpha 3
C-beta 3, first solvent atom, group numbers of the relevant residues

ATTENTION: the input numbers are the LINE NUMBERS and not the atom numbers!!
As python starts counting at 0, a line number of 348 results in an input number
of 347

The frames are saved as .gro-files in subdirectory 'frames'.
The new frames with the added Link Atoms are in the subdirectory 'new_frames'.
This script should be in the parent directory of 'frames'.
The location of the input-files is arbitrary.

Output:
- full.gro

Recommended input for the trjconv commands:
output: 0 (System)

## part1_mod.py
This script can be used if the frames from the original .xtc-file were successfully
generated but something's wrong with adding the Link Atoms.

This script uses the frames and adds the Link Atoms.

It's for example useful if the centering didn't work with one frame. Then
part1.py generates a trajectory until this frame. The frames after the broken
one can be copied to a new directory as well as this script. It can then
generate the trajectory from the frame after the broken one.

Another use is for testing with QM/MM simulations. Generate frames from the
.xtc-file with part1.py, delete the Link Atoms with "sed -i '/XXX/d' frame*.gro"
and generate with part1_mod.py the new_frame*.gro files. ATTENTION: for this
case, the checksum at the beginning of the new_frame.gro-files needs to be three
atoms lower ("sed -i 's/149890/149887/g' full.gro").

## run_gmx2016.sh
run with 'source ./run_gmx2016.sh'

File to source the right GROMACS version to convert the modified .gro-files to a
new .xtc-file.
Converts the modified .gro-files to a new .xtc-file.

Output:
- full.xtc

# PART 2
consists of:
- part2.sh
- part2_esp.py
- plot_esp.py

## part2.sh
Generates a .tpr-file for the QM rerun

ATTENTION: generate .ndx-file with new_frame0.gro and add the QM region.
Otherwise there will be 3 atoms missing in the .ndx-file.

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


## part2_esp.py
Calculates the ESP from the QM on itself. Reads the input file
'qm_dftb_qm.qxyz' and writes the ESPs to the output file 'esp_output' where the
gamma function was used and to 'esp_output_wo_gama' if Coulomb (1/r) was used.


## plot_esp.py
Example for plotting the results for ESP given by GROMACS and the correction
from part2_esp.py. Includes the conversion factor from a.u. to SI units.


# TO DO
- change code of part1 so that the number of link atoms can be chosen
- change part1_mod so that the distance between the Ca and Cb are used for the
  ERROR file

# Tested in:
tcb:/data/user1/HiWi_Maike/tool/test_5A_k5000_41/231213

hyd:/data/user1/MAIKE/tool/test_5A_k5000_41/231213

Test runs in tcb:/data/user1/HiWi_Maike/tool/test_5A_k5000_41/231231 without
index file
