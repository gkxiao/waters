# coding: utf-8
# By Gaokeng Xiao
# 2024-07-23
# Copyright (C) 2024 Guangzhou Molcalx Ltd.
# Released under CC-BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
# Originally downloaded from https://github.com/gkxiao/waters
# Welcome to Flare Python Interpreter.
# Documentation can be found at Python > Documentation.
# This default python script can be edited at:
# '/home/gkxiao/.com.cresset-bmd/Flare/python/default-scripts/InterpreterDefaultScript.py'
from cresset import flare
import numpy as np

"""Show the GIST solvation free energy
Usage:
Please select the protein interested and the pick the atom interested.
The script will show the deltaG at the coordinate of atom picked by using the selected protein's GIST grid.
"""
#
# Don't modify the codes starting from here !
#
# Access the current Flare project
p = flare.main_window().project

# use the selected protein and its deltaG surface 
prot = flare.main_window().selected_proteins[0]
# Get the associated grid, which is a GIST deltaG
# find the surface including dG，detlaG or ΔG
def starts_with_dG_prefix(s):
    # List of prefixes to check
    prefixes = ["dG", "deltaG", "dg", "ΔG", "ΔG+", "ΔG-"]
    
    # Check if the string starts with any of the prefixes
    for prefix in prefixes:
        if s.startswith(prefix):
            return True
surface_idx = 0
for idx in range(len(prot.surfaces)):
    if starts_with_dG_prefix(prot.surfaces[idx].name):
        surface_idx = surface_idx
        break
    else:
        print("Cannot find the GIST ΔG grid for this protein")
        print("Exit program")
        exit()
grid = prot.surfaces[surface_idx].grid()

# set protein & its deltaG grid
prot = p.proteins[protein_index]
grid = prot.surfaces[surface_index].grid()

# Get the picked atom
picked_atom = flare.main_window().picked_atoms[0]
picked_coord = picked_atom.pos

# Define the radius for the calculation
radius = 1.4

# Define the step sizes for the grid
step_sizes = np.array([0.5, 0.5, 0.5])

# Get the shape of the grid
grid_shape = np.array([grid.x_size, grid.y_size, grid.z_size])

# Get the origin of the grid
grid_origin = np.array(grid.origin)

# Create a meshgrid of indices for each dimension
x_indices, y_indices, z_indices = np.meshgrid(
    np.arange(grid_shape[0]),
    np.arange(grid_shape[1]),
    np.arange(grid_shape[2]),
    indexing='ij'
)

# Calculate all grid coordinates based on the origin and step sizes
all_grid_coords = grid_origin + np.stack([x_indices, y_indices, z_indices], axis=-1) * step_sizes

# Get all grid values
all_grid_values = grid.data

# Convert the picked coordinate to a numpy array
input_coord = np.array(picked_coord)

# Calculate the distances between all grid points and the input coordinate
distances = np.linalg.norm(all_grid_coords - input_coord, axis=-1)

# Create a mask to filter out points outside the radius and with zero grid values
mask = (distances <= radius) & (abs(all_grid_values) > 0)

# Filter the coordinates and values based on the mask
filtered_coords = all_grid_coords[mask]
filtered_values = all_grid_values[mask]

# Initialize a list to store the results
results = []

# Iterate over the filtered coordinates and values
for coord, value in zip(filtered_coords, filtered_values):
    # Truncate the value if it is greater than 3.0
    truncated_value = min(value, 3.0)
    results.append((tuple(np.round(coord, 5)), value, truncated_value))

# Print information about the picked atom and the input coordinate
print(f'Atom: {picked_atom} {picked_atom.index},{picked_atom.residue}')
print(f'The input coordinate: {picked_coord[0]:.3f},{picked_coord[1]:.3f},{picked_coord[2]:.3f}')
print(f'Radius: {radius} A')
print(f"Total unique voxels: {len(results)}")
print(f'Method: truncated the value greater than 3.0 kcal/mol*A^3')

# Calculate and print the sum of values and truncated values, multiplied by 0.125
sum_values = sum(value for _, value, _ in results)*0.125
sum_truncated_values = sum(truncated_value for _, _, truncated_value in results)*0.125
# set the atom rf as dG
picked_atom.tf = sum_truncated_values

# access atom style
atom_style = picked_atom.style

# set the annotation to display the tf value
# By cresset robotchat, great job!
atom_style.annotation = f"dG = {picked_atom.tf:.3f}"
atom_style.annotation_label_visible = True

# print results
print(f"dG : {sum_values:.3f} kcal/mol")
print(f"dG_truncated: {sum_truncated_values:.3f} kcal/mol")
