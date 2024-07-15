# Introduction

This tool extends the functionality of GROMACS/DFTB+ by calculating
electrostatic potentials (ESPs) directly from the atoms within the quantum
mechanics (QM) region. Unlike GROMACS/DFTB+, which provides ESP values solely
from the molecular mechanics (MM) on the QM region, this tool offers
corrections to compute ESP values directly from the QM atoms themselves.
Additionally, it facilitates the preparation of classical MM simulations for
QM/MM reruns and thus ESP values for MM simulations can be generated.

# Part 1: Link Atom Placement Tool ('LAPLACE')

Part 1 of the tool consists of two essential components:
- `laplace.py`
- `run_gmx2016.sh`
And one additional component:
- `laplace_mod.py`

## Description:

The purpose of this part is to read an .xtc-file, generate .gro-files and insert
Link Atoms at appropriate positions (`laplace.py`). Then, an older GROMACS version
needs to be sourced that is able to convert the resulting .gro-file to a
trajectory file (`run_gmx2016.sh`).

## Requirements:

- .xtc-file of a classical MM simulation
- .tpr-file of the same system

## Usage:

- `python3 laplace.py *C-alpha1 C-beta1 C-alpha2 C-beta2 C-alpha3 C-beta3 first_sol
gr_nr1 gr_nr2 gr_nr3*`

Where the input numbers represent the line numbers of the C-alpha and C-beta
atoms, of the first solvent atom and of the group numbers of the relevant
residues.

- `source ./run_gmx2016.sh`

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

- For 41-/43-systems: `python3 laplace.py 347 349 1683 1685 2139 2141 3251 22 2
  27`
- For 71-/73-systems: `python3 laplace.py 347 349 2104 2106 3235 3237 3251 22 27
  2`
- Recommended input for the `trjconv` commands: `output: 0 (System)`

## laplace\_mod.py

This script serves as a fallback option if there were issues with adding the
Link Atoms to the frames generated from the original .xtc-file.

### Usage Scenarios:

1. Fixing Frame Generation Issues:
This script can come in handy if the frames were successfully generated from the
original .xtc-file but encountered problems with adding Link Atoms. For
instance, if centering failed for one frame, laplace.py can generate a trajectory
until that frame. Subsequently, the frames after the problematic one can be
copied to a new directory along with this script. Then, this script can add the
Link Atoms starting from the frame following the problematic one.

2. Testing with QM/MM Simulations:
Another use-case is for testing the tool with actual QM/MM simulations, for
example if the code was modified. First, generate frames from the .xtc-file
using laplace.py. Then, delete the Link Atoms using "sed -i '/XXX/d'
frame\*.gro". Next, use laplace\_mod.py to generate new\_frame\*.gro files. Note: For
this scenario, ensure that the checksum at the beginning of the new\_frame.gro
files is three atoms lower by using "sed -i 's/149890/149887/g' full.gro".


# Part 2: QM Rerun and ESP Calculation ('QMREC')

Part 2 of the tool consists of the following components:
- `make_tpr.sh`
- `qmrec.py`
- `conv_full_esp.py`
- `plot_esp.py`

## Description

This part focuses on performing a QM rerun and calculating the ESP within the QM
region. This is added to the ESP of the MM region on the QM region by DFTB+ to
get the full ESP. During this step, the atomic units are converted to SI units
(Volt). Finally, a script to visualize the full ESP is provided.

## Requirements

- topology file (`.top`) -> changed for QM/MM simulations
- index file (`.ndx`) -> changed for QM/MM simulations
- `dftb_in.hsd`
- `.mdp` file with instructions for a QM/MM simulation (the provided file should
  be fine for most cases)
- `single_submit_rerun.sh` -> changed for a QM/MM rerun
- `new_frame0.gro`
- `full.xtc`

## Usage

1. Create a new index file with `new_frame0.gro` (input in GROMACS: `gmx_d
   make_ndx -f new_frame0.gro`, select '0' for the whole system and quit with
   'q'). Add the section '[QM\_region]' at the bottom of the index file with the
   number of the atoms in the QM region.

2. `./make_tpr.sh *.mdp *.gro *.top *.ndx`
    This generates the `md.tpr` file that is needed as input for the QM rerun.
    Change the submission script `single_submit_rerun.sh` according to your needs.
The provided default should work but if the original simulation was a classical
MM simulation, the files should be exported more often (`export GMX_DFTB_ESP=1`,
`export GMX_DFTB_CHARGES=1` and `export GMX_DFTB_QM_COORD=1`). The name of the rerun
can be changed in the second line (the default name is 'rerun').
Submit the rerun with `qsub single_submit_rerun.sh`.

3. `python3 qmrec.py`
    This script calculates the ESP from the QM atoms onto themselves. It reads
the input file `qm_dftb_qm.qxyz` generated by the QM rerun and writes the ESPs
to `esp_output`. 

4. `python3 conv_full_esp.py`
    The ESP from `esp_output` is added to the ESP from the MM on the QM region
(`qm_dftb_esp.xvg`) to get the full ESP. It creates a Numpy binary file
(`esp_full.npy`) and a txt file (`esp_full.txt`). The script also converts the
atomic units (electronic charge / Hartree) to SI units. It also changes the sign
of the partial ESP, as DFTB+ gives negative charges a positive sign. Please note
that the sign of the output file `qm_dftb_charges.xvg` is correct, so the ESP
within the QM region in the file `esp_output` is already has the right sign and
only needs to be converted to SI units.

5. `python3 plot_esp.py`
    Facilitates visualization by plotting the full ESP.

## Output

- `md.tpr`
- `qm_dftb_qm.qxyz`
- `esp_output`


# Supplementary Info
- `LA_position.svg` shows the position where the Link Atom is placed.
- `flowchart.svg` and `flowchart.png` illustrate the work flow of the tool.


# Planned Improvements
- change code of `laplace.py` so that the number of Link Atoms can be chosen
- change `laplace_mod.py` so that the distance between the Ca and Cb are used for the
  ERROR file
- rewrite the function `coord` in `laplace.py` and `laplace_mod.py` so that it does not
  use a global variable

# Notes

- The ESP from `qm_dftb_esp.xvg` is given in Volts
- The ESP from `esp_output` is given in atomic units and is converted to Volts
  in `conv_full_esp.py`
