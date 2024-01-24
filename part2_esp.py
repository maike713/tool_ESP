import numpy as np

#file_path = 'test.qxyz'
file_path = 'qm_dftb_qm.qxyz'

# function to detect how many frames and atoms per frame are in the input file
def find_frames(file_path):
    frames = []
    empty_lines = []
    line_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip().split()
            line_count += 1

            # ignores empty lines, otherwise out of range error
            if not line:
                empty_lines.append(line_count)
                continue

            if line[0] == 'QM':
                frames.append(line_count)

        # make sure, that in all frames are the same amount of atoms
        # and find out how many atoms there are
        for i in range(0, len(frames) - 2):
            atom_count1 = empty_lines[i+1] - frames[i] - 1
            atom_count2 = empty_lines[i+2] - frames[i+1] - 1
            assert atom_count1 == atom_count2

    frame_count = len(frames)
    empty_lines_count = len(empty_lines)


    return frames, empty_lines, atom_count1

# function to get the coordinates and charges from the input file
def read_coords_charges(file_path, frames, empty_lines):
    # create empty dictionary 
    dict_frames = {}
    # create dictionary to convert atom labels to numbers
    dict_atomtypes = {'c':1, 'h':2, 's':3}

    with open(file_path, 'r') as file:
        # read all lines as strings into list 'all_lines'
        all_lines = file.readlines()
        
        for i in range(0, len(frames)):
            # generate keys for dict_frames
            frame_label = i

            # generate values for dict_frames in the form of:
                # [[x(atom1), y(atom1), z(atom1), q(atom1)]
                #  [x(atom2), y(atom2), z(atom2), q(atom2)]
                # ...
                #  [x(atom(i)), y(atom(i)), z(atom(i)), q(atom(i))]]
            frame_value = np.empty((atom_count, 5))
            for j in range(0, atom_count):
                # split the string with index frames[i] + j in all_lines
                to_append = np.array([ all_lines[int(frames[i]) + j].split() ])
                k = to_append[:,0]
                to_append[:,0] = dict_atomtypes[k[0]]
                frame_value[j,:] = to_append

            dict_frames[i] = frame_value

    return dict_frames

# function for gamma if ESP is calculated between to atoms of the same type
def g_case_a_eq_b(hubbard1: float, x_range: np.array)->float:
    # same atoms
    alpha = 16/5 * hubbard1
    r = x_range
    g_result = 1/r - ((1/(48*r)) * (48 + 33 * alpha * r + 9 * alpha**2 * r**2 + alpha**3 * r**3 ) * np.exp(-alpha*r))
    return g_result

# function for gamma if ESP is calculated between to atoms of different types
def f_function_gamma(hubbard1: float,hubbard2: float, x_range: np.array)->float:
    alpha = 16/5 * hubbard1
    beta = 16/5 * hubbard2
    r = x_range
    a_1 = alpha * beta**4
    a_2 = 2*(alpha**2 - beta**2)**2
    a_3 = beta**6 - 3 * alpha**2 * beta**4
    a_4 = r * (alpha**2 -  beta**2)**3
    f_result = (a_1/a_2) - (a_3/a_4)
    return f_result

def f_case_a_neq_b(hubbard1: float,hubbard2: float, x_range: np.array)->float:
    alpha = 16/5 * hubbard1
    beta = 16/5 * hubbard2
    r = x_range
    f_result = 1/r - ( np.exp(-alpha*r) * f_function_gamma(hubbard1, hubbard2, r) + np.exp(-beta*r) * f_function_gamma(hubbard2, hubbard1, r))
    return f_result

# dictionary to convert numbers to atom types
dict_atomtypes_reverse = {1:'C', 2:'H', 3:'S'}

# dictionary to define hubbard units
#unit_conversion_bohr_to_nm = 1/ 0.0529177249
unit_conversion_bohr_to_nm = 1  # for a.u.
dict_hubbard = {
           "C": 0.3647*unit_conversion_bohr_to_nm,
            "H": 0.4195*unit_conversion_bohr_to_nm,
            "N": 0.4309*unit_conversion_bohr_to_nm,
            "O": 0.4954*unit_conversion_bohr_to_nm,
            "Br": 0.3277*unit_conversion_bohr_to_nm,
            "Cl": 0.3668*unit_conversion_bohr_to_nm,
            "F": 0.5584*unit_conversion_bohr_to_nm,
            "I": 0.2842*unit_conversion_bohr_to_nm,
            "P": 0.2894*unit_conversion_bohr_to_nm,
            "S": 0.3288*unit_conversion_bohr_to_nm,
            }

frames, empty_lines, atom_count = find_frames(file_path)

dict_frames = read_coords_charges(file_path, frames, empty_lines)

#empty dictionary to store ESPs per frame
dict_esp = {}
dict_esp_vgl = {}


# loop through the frames
for key in dict_frames:
    # empty list to store coordinates of a frame
    coords = []
    # empty list to store quotient = distance / charge of a frame
    quotient = []
    # empty list to store ESPs of a frame
    esp_values = []
    esp_values_vgl = []

    # loop through the atoms in a frame
    for i in range(0, atom_count):
        # save coordinates of atoms in variable coord_vector if atoms != atom i
        coord_vector_i = dict_frames[key]
        coord_vector_i = np.array([ coord_vector_i[i,1], coord_vector_i[i,2], coord_vector_i[i,3] ])
        # convert distance from Angstrom to Bohr
        coords.append(coord_vector_i * 0.5291772)

    # calculate the distance and charge between atom i and all other atoms
    for i in range(0, atom_count):
        esp_i = 0
        esp_i_vgl = 0

        for j in range(0, atom_count):
            if j != i: ### richtig oder doch andersrum?
                dist_i = np.linalg.norm(coords[i] - coords[j])
                charge_j = dict_frames[key]
                charge_j = charge_j[j,4]
                # differentiate between ESP between same or different atom types
                atom_type_i = dict_frames[key]
                atom_type_i = int(atom_type_i[i,0])
                atom_type_j = dict_frames[key]
                atom_type_j = int(atom_type_j[j,0])
                if atom_type_i == atom_type_j:
                    hubbard1  = dict_atomtypes_reverse[atom_type_i]
                    hubbard1 = dict_hubbard[hubbard1]
                    gamma_result = g_case_a_eq_b(hubbard1, dist_i)
                else:
                    hubbard1 = dict_atomtypes_reverse[atom_type_i]
                    hubbard1 = dict_hubbard[hubbard1]
                    hubbard2 = dict_atomtypes_reverse[atom_type_j]
                    hubbard2 = dict_hubbard[hubbard2]
                    gamma_result = f_case_a_neq_b(hubbard1, hubbard2, dist_i)
                # change sign of esp to be compatible with DFTB+ output
                esp_i += charge_j * gamma_result * (-1) # ESP in a.u.
                esp_i_vgl += charge_j / dist_i * (-1)
        esp_values.append(esp_i)
        esp_values_vgl.append(esp_i_vgl)
                

    # write ESPs to ESP dictionary
    dict_esp[key] = esp_values
    dict_esp_vgl[key] = esp_values_vgl            


with open('esp_output', 'w') as file:
    file.write('QM potential induced on the QM atoms (ESP) in a.u.:\n')
    for key in dict_esp:
        value = dict_esp[key]
        output_string = str(key)
        for i in range(0, len(value)):
            output_string += ' ' + str(value[i])
        file.write(f'{output_string}\n') 

with open('esp_output_wo_gamma', 'w') as file:
    file.write('QM potential induced on the QM atoms (ESP) in a.u.:\n')
    for key in dict_esp_vgl:
        value = dict_esp_vgl[key]
        output_string = str(key)
        for i in range(0, len(value)):
            output_string += ' ' + str(value[i])
        file.write(f'{output_string}\n')

print('Output with gamma function written to esp_output, with 1/r to esp_output_wo_gamma')
