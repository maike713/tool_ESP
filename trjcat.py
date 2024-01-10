import subprocess

# make an .xtc-file out of the full.gro file
try:
    subprocess.run('gmx trjcat -f full.gro -o full.xtc', shell = True, check = True)
except subprocess.CalledProcessError as e:
    print(f'Error executing command: {e}')
