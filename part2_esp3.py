import numpy as np

#file_path = 'test.qxyz'
file_path = 'qm_dftb_qm.qxyz'


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


def read_coords_charges(file_path, frames, empty_lines):
    # create empty dictionary 
    dict_frames = {}
    #print(frame_value[:,0])
    # create dictionary to convert atom labels to numbers
    dict_atomtypes = {'c':1, 'h':2, 's':3}

    with open(file_path, 'r') as file:
        # read all lines as strings into list 'all_lines'
        all_lines = file.readlines()
        #print(all_lines[2].split())
        #print(all_lines[2])
        #print(type(all_lines[2]))
        #print(type(all_lines))
        
        for i in range(0, len(frames)):
            # generate keys for dict_frames
            frame_label = i
            #print(frame_label)

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
                #print(k)
                to_append[:,0] = dict_atomtypes[k[0]]
                frame_value[j,:] = to_append

            dict_frames[i] = frame_value

    return dict_frames

frames, empty_lines, atom_count = find_frames(file_path)
#print(frames)
#print(empty_lines)
#print(atom_count)

dict_frames = read_coords_charges(file_path, frames, empty_lines)
#empty dictionary to store ESPs per frame
dict_esp = {}

#print('\nDictionary:')

# loop through the frames
for key in dict_frames:
    #print(key, dict_frames[key], '\n')
    # empty list to store coordinates of a frame
    coords = []
    # empty list to store quotient = distance / charge of a frame
    quotient = []
    # empty list to store ESPs of a frame
    esp_values = []

    # loop through the atoms in a frame
    for i in range(0, atom_count):
        # save coordinates of atoms in variable coord_vector if atoms != atom i
        coord_vector_i = dict_frames[key]
        coord_vector_i = np.array([ coord_vector_i[i,1], coord_vector_i[i,2], coord_vector_i[i,3] ])
        coords.append(coord_vector_i)

    # calculate the distance and charge between atom i and all other atoms
    for i in range(0, len(coords)):
        esp_i = 0
        for j in range(0, len(coords)):
            if j != i: ### richtig oder doch andersrum?
                dist_i = np.linalg.norm(coords[i] - coords[j])
                charge_i = dict_frames[key]
                charge_i = charge_i[i,4]
                # calculate the esp on atom i
                esp_i += charge_i / dist_i
        esp_values.append(esp_i)

    # write ESPs to ESP dictionary
    dict_esp[key] = esp_values
                

#print('ESP Dictionary:\n')
#for key in dict_esp:
#    print(key, dict_esp[key], '\n')

with open('esp_output3', 'w') as file:
    for key in dict_esp:
        value = dict_esp[key]
        output_string = str(key)
        for i in range(0, len(value)):
            output_string += ' ' + str(value[i])
        file.write(f'{output_string}\n') 
