###################
# for GROMACS with single precision

# input 41: python3 part1.py 347 349 1683 1685 2139 2141 3251 22 2 27
# input 73: python3 part1.py 347 349 2104 2106 3235 3237 3251 22 27 2
# explanation:               ca1 cb1 ca2  cb2  ca3  cb3  sol  group-numbers

###### FILES NEEDED:
# .xtc-file
# .tpr-file
# .ndx-file

## frames are saved as .gro-files in subdirectory 'frames'
# this script should be in the parent directory of 'frames'
# the input files (xtc, tpr, ndx) can be anywhere

## input for the trjconv command:
# output: 0 (System)

####################

import subprocess
import sys
import numpy as np
import os
import glob
from sklearn.metrics.pairwise import euclidean_distances

# parameter to change the accuracy of the centering test
p = 1.0

# input
xtc = str(input('Enter the name of the .xtc-file:\n'))
tpr = str(input('Enter the name of the .tpr-file:\n'))
ndx = str(input('Enter the name of the .ndx-file:\n'))

# make a directory to store the frames
try:
    subprocess.run('mkdir frames', shell = True, check = True)
except subprocess.CalledProcessError as e:
    print(f'Error executing command: {e}')

# make a directory 'new_frames' to store the new files
try:
    subprocess.run('mkdir new_frames', shell = True, check = True)
except subprocess.CalledProcessError as e:
    print(f'Error executing command: {e}')

command1 = f'gmx trjconv -f {xtc} -s {tpr} -n {ndx} -pbc whole -o whole.xtc'
# execute the command in the frames subdirectory
# one directory back because the command is executed in a subdirectory
command2 = f'gmx trjconv -f ../whole.xtc -s ../{tpr} -n ../{ndx} -pbc mol -sep -o frame.gro'
try:
    subprocess.run(command1, shell = True, check = True, cwd = '.')
except subprocess.CalledProcessError as e:
    print(f'Error executing command: {e}')
try:
    subprocess.run(command2, shell = True, check = True, cwd = './frames')
except subprocess.CalledProcessError as e:
    print(f'Error executing command: {e}')

a1 = int(sys.argv[1])
b1 = int(sys.argv[2])
a2 = int(sys.argv[3])
b2 = int(sys.argv[4])
a3 = int(sys.argv[5])
b3 = int(sys.argv[6])
sol = int(sys.argv[7])

# format to be 5 characters long
group_1 = '{:>5}'.format(sys.argv[8])
group_2 = '{:>5}'.format(sys.argv[9])
group_3 = '{:>5}'.format(sys.argv[10])

print(type(group_1))

file_list = os.listdir('frames')

# function to get the coordinates as a vector
## global variable 'lines' in function -> meh
def coord(num_line):
    lines_string = str(lines[num_line])
    vec = np.array([float(lines_string.split()[3]),float(lines_string.split()[4]), float(lines_string.split()[5])])
    return vec

# loop through all files in directory 'frames'
for file_name in file_list:
    input_file_path = os.path.join('frames', file_name)

    with open(input_file_path, 'r') as file:
        # read all the lines in list 'lines'
        lines = file.readlines()

        # add three atoms to the total number of atoms
        total_atoms = int(lines[1]) + 3

        # get the coordinates of Ca and Cb atoms
        vec_ca1 = coord(a1)
        vec_cb1 = coord(b1)
        vec_ca2 = coord(a2)
        vec_cb2 = coord(b2)
        vec_ca3 = coord(a3)
        vec_cb3 = coord(b3)

        # calculate the vectors to the link atoms and round to three decimals
        vec_la1 = np.round(0.72 * (vec_ca1 - vec_cb1) + vec_cb1, decimals = 3)
        vec_la1 = ['{:>8.3f}'.format(num) for num in vec_la1]     # add zeroes if necessary
        vec_la2 = np.round(0.72 * (vec_ca2 - vec_cb2) + vec_cb2, decimals = 3)
        vec_la2 = ['{:>8.3f}'.format(num) for num in vec_la2]     # add zeroes if necessary
        vec_la3 = np.round(0.72 * (vec_ca3 - vec_cb3) + vec_cb3, decimals = 3)
        vec_la3 = ['{:>8.3f}'.format(num) for num in vec_la3]     # add zeroes if necessary

    # control mechanism: should detect broken QM-zone

    # create 2D-arrays that sklearn can work with
    vec_ca1_2d = np.array(vec_ca1, dtype = float).reshape(1,-1)
    vec_ca2_2d = np.array(vec_ca2, dtype = float).reshape(1,-1)
    vec_ca3_2d = np.array(vec_ca3, dtype = float).reshape(1,-1)

    vec_cb1_2d = np.array(vec_cb1, dtype = float).reshape(1,-1)
    vec_cb2_2d = np.array(vec_cb2, dtype = float).reshape(1,-1)
    vec_cb3_2d = np.array(vec_cb3, dtype = float).reshape(1,-1)

    # calculate the distances between Calpha and Cbeta
    dist_ca1_cb1 = euclidean_distances(vec_ca1_2d, vec_cb1_2d)
    dist_ca2_cb2 = euclidean_distances(vec_ca2_2d, vec_cb2_2d)
    dist_ca3_cb3 = euclidean_distances(vec_ca3_2d, vec_cb3_2d)

    if dist_ca1_cb1 > p or dist_ca2_cb2 > p or dist_ca3_cb3 > p:
        print('BROKEN MOLECULE')
        with open('ERROR.txt', 'a') as error_file:
            error_file.write(f'\nERROR probably broken molecule file {file_name}\n')
            error_file.write(f'{dist_ca1_cb1}, {dist_ca2_cb2}, {dist_ca3_cb3}\n')


    output_file_path = os.path.join('new_frames', f'new_{file_name}')

    # write a new file
    with open(output_file_path, 'w') as new_file:
        # write the first line
        new_file.write(lines[0])

        # write the new total amount of atoms
        new_file.write(f'{total_atoms}\n')

        # write all lines just before SOL
        for i in range(2, sol):
            new_file.write(lines[i])

        # write the Link Atoms
        new_file.write(f'{group_1}XXX     LA {sol - 1}{vec_la1[0]}{vec_la1[1]}{vec_la1[2]}\n')
        new_file.write(f'{group_2}XXX     LA {sol}{vec_la2[0]}{vec_la2[1]}{vec_la2[2]}\n')
        new_file.write(f'{group_3}XXX     LA {sol + 1}{vec_la3[0]}{vec_la3[1]}{vec_la3[2]}\n')

        # write the SOL atoms
        for i in range(sol, len(lines)):
            new_file.write(lines[i])


## generate the new xtc-file

# get a list of files with ending .gro and sort them
file_pattern = os.path.join('new_frames', 'new_frame*.gro')
file_list = sorted(glob.glob(file_pattern), key = lambda x: int(os.path.basename(x).split('frame')[1].split('.gro')[0]))
print(file_list)

# loop through all gro-files in current directory
for file_name in file_list:
    input_file_path = os.path.join('.', file_name)
    output_file_path = os.path.join('.', 'full.gro')
    
    # read all the .gro files
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # write to full.gro
    with open(output_file_path, 'a') as full_file:
        for i in range(0, len(lines)):
            full_file.write(lines[i])
