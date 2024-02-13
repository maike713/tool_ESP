# Introduction

This tool extends the functionality of GROMACS/DFTB3 by calculating
electrostatic potentials (ESPs) directly from the atoms within the quantum
mechanics (QM) region. Unlike GROMACS/DFTB3, which provides ESP values solely
from the molecular mechanics (MM) on the QM region, this tool offers
corrections to compute ESP values directly from the QM atoms themselves.
Additionally, it facilitates the preparation of classical MM simulations for
QM/MM reruns and thus ESP values for MM simulations can be generated.

# Part 1: Link Atom Placement Tool

Part 1 of the tool consists of two essential components:
- `part1.py`
- `run\_gmx2016.sh`
And one additional component:
- `part1\_mod.py`

## Description:

The purpose of this part is to read an .xtc-file, generate .gro-files and insert
Link Atoms at appropriate positions (`part1.py`). Then, an older GROMACS version
needs to be sourced that is able to convert the resulting .gro-file to a
trajectory file (`run\_gmx2016.sh`).

## Requirements:

- .xtc-file of a classical MM simulation
- .tpr-file of the same system

## Usage:

- `python3 part1.py *C-alpha1 C-beta1 C-alpha2 C-beta2 C-alpha3 C-beta3 first\_sol
gr_nr1 gr_nr2 gr_nr3*`

Where the input numbers represent the line numbers of the C-alpha and C-beta
atoms, of the first solvent atom and of the group numbers of the relevant
residues.

- `source ./run\_gmx2016.sh`

## Note:

- Input numbers correspond to line numbers, not atom numbers.
- Python uses zero-based indexing, so a line number of 348 results in an input
  of 347.
- Frames are saved in the 'frames' subdirectory, while frame with added Link
  Atoms are stored in 'new\_frames'.
- The script should reside in the parent directory of 'frames'.
- If the bond between C-alpha and C-beta atoms is broken due to periodic
  boundary conditions, the tool cannot provide the correct coordinates. This is
  prevented by the ´trjconv -pbc whole´ option. If this fails and the distance
  between two C-alpha anc C-beta atoms is longer than 1 nm, the tool provides an
  `ERROR.txt` file with the frame of the probably broken molecule.

## Output:

- `full.gro`
- `ERROR.txt` (hopefully not)
- `full.xtc`

## Recommended Usage for Specific Systems:

- For 41-/43-systems: `python3 part1.py 347 349 1683 1685 2139 2141 3251 22 2
  27`
- For 71-/73-systems: `python3 part1.py 347 349 2104 2106 3235 3237 3251 22 27
  2`
- Recommended input for the `trjconv` commands: `output: 0 (System)`

## part1\_mod.py

This script serves as a fallback option if there were issues with adding the
Link Atoms to the frames generated from the original .xtc-file.

### Usage Scenarios:

1. Fixing Frame Generation Issues:
This script can come in handy if the frames were successfully generated from the
original .xtc-file but encountered problems with adding Link Atoms. For
instance, if centering failed for one frame, part1.py can generate a trajectory
until that frame. Subsequently, the frames after the problematic one can be
copied to a new directory along with this script. Then, this script can add the
Link Atoms starting from the frame following the problematic one.

2. Testing with QM/MM Simulations:
Another use-case is for testing the tool with actual QM/MM simulations, for
example if the code was modified. First, generate frames from the .xtc-file
using part1.py. Then, delete the Link Atoms using "sed -i '/XXX/d'
frame\*.gro". Next, use part1\_mod.py to generate new\_frame\*.gro files. Note: For
this scenario, ensure that the checksum at the beginning of the new\_frame.gro
files is three atoms lower by using "sed -i 's/149890/149887/g' full.gro".


# PART 2
consists of:
- part2.sh
- part2\_esp.py
- plot\_esp.py

## part2.sh
Generates a .tpr-file for the QM rerun

ATTENTION: generate .ndx-file with new\_frame0.gro and add the QM region.
Otherwise there will be 3 atoms missing in the .ndx-file.

files needed:
- .top-file -> changed for QM simulations
- .ndx-file -> changed for QM simulations
- new\_frame0.gro
- full.xtc
- dftb\_in.hsd
- .mdp-file
- single\_submit.sh -> changed for rerun

input:
- ./part2.sh \*.mdp \*.gro \*.top \*.ndx

After the successfull generation of md.tpr: submit with:

qsub single\_submit.sh


## part2\_esp.py
Calculates the ESP from the QM on itself. Reads the input file
`qm\_dftb\_qm.qxyz` and writes the ESPs to the output file `esp\_output` where the
gamma function was used and to `esp\_output\_wo\_gama` if Coulomb (1/r) was used.


## plot\_esp.py
Example for plotting the results for ESP given by GROMACS and the correction
from part2\_esp.py. Includes the conversion factor from a.u. to SI units.


# TO DO
- change code of part1 so that the number of link atoms can be chosen
- change part1\_mod so that the distance between the Ca and Cb are used for the
  ERROR file

# Tested in:
tcb:/data/user1/HiWi_Maike/tool/test_5A_k5000_41/231213

hyd:/data/user1/MAIKE/tool/test_5A_k5000_41/231213

Test runs in tcb:/data/user1/HiWi_Maike/tool/test_5A_k5000_41/231231 without
index file
