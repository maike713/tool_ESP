import numpy as np

#file_path = 'test.qxyz'
file_path = 'qm_dftb_qm.qxyz'

def read_qxyz(file_path):
    # create empty dictionary for the atom coordinates
    atom_coordinates = {}
    # create empty dictionary for atom charges
    atom_charges = {}
    
    with open(file_path, 'r') as file:
    
        current_atom_count = 0
        current_step = np.array([])
        
        for line in file:
            line = line.strip().split()
    
            # if empty line, don't write in line
            if not line:    # recognizes empty line
               continue    # returns to the beginning of the for loop
            
            # find beginning of step
            if line[0] == 'QM':
               #current_atom_count = 0
                current_step = np.append(current_step, int(line[-1]))
                #print(line)
                #print('current step: ', current_step)
                continue
            
            # enumerate atoms
            atom_label = f'atom_{current_atom_count}'
            current_atom_count += 1
    
            # get coordinates
            atom_coordinates[atom_label] = np.array([float(line[1]), float(line[2]), float(line[3])])
            
            # get charges
            atom_charges[atom_label] = float(line[4])

    return atom_coordinates, atom_charges, current_step



atom_coordinates, atom_charges, current_step = read_qxyz(file_path)

#print('\nCoordinates:')
#for key in atom_coordinates:
#    print(key, atom_coordinates[key])
#
#print('\nCharges:')
#for key in atom_charges:
#    print(key, atom_charges[key])

start_range = 0
end_range = len(atom_coordinates)
step = 15

#### output file
with open('esp_output2', 'a') as file:
    file.write('ESP QM region on QM region\n')
    file.write('Step, Atom1, Atom2, etc\n')


     #### ESP
    for start in range(start_range, end_range, step):
        end = min(start + step, end_range)

        # |r - ri| distances
        distances = {}
        for atom in list(atom_coordinates)[start:end]:
            distances[atom] = sum(np.linalg.norm(atom_coordinates[atom] - atom_coordinates[other_atom]) for other_atom in atom_coordinates if other_atom != atom)
        
        #print('\nDistances:')
        #for key in distances:
        #    print(key, distances[key])
        
        # sum of charges
        sum_charges = {}
        for atom in list(atom_charges)[start:end]:
            sum_charges[atom] = sum(charge for other_atom, charge in atom_charges.items() if other_atom != atom)
        
        #print('\nCharges:')
        #for key in sum_charges:
        #    print(key, sum_charges[key])
        
        # ESP
        esp = {}
        for atom in distances:
            esp[atom] = sum(sum_charges[other_atom] / distances[other_atom] for other_atom in distances if other_atom != atom)
        
        print('\nESP:')
        for key in esp:
            print(key, esp[key])
        
        for i in range(0,len(current_step)):
            output_array = np.array([current_step[i]])
            for key in esp:
                output_array = np.append(output_array, esp[key])
            #file.write(f'{output_array}\n')
            np.savetxt(file, output_array, fmt = '%.6f', delimiter = ' ', newline = ' ')
            file.write('\n')

print('ESP written to file esp_output2')
