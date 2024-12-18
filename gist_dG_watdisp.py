#!/usr/bin/env python
# coding: utf-8
# By Guangxiao Xiao
# 2024-07-23
# Copyright (C) 2024 Guangzhou Molcalx Ltd.
# Released under CC-BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
# Originally downloaded from https://www.molcalx.com.cn

"""GIST-based water displacement score.

usage: gist_watscore_dock.py [-h] <deltaG GRID file> <db file in SDF format>

For example:
gist_watscore.py dg.dx db.sdf db_out.sdf

Here dg.dx is the unhappy water deltaG grid file generated by Flare GIST.
"""


import argparse
from rdkit import Chem
import numpy as np
from gridData import Grid

parser = argparse.ArgumentParser(description="Calculate the water score for ligand database.\n")
parser.add_argument('-g',metavar='<deltaG_grid_file>',help="happy/unhappy water deltaG grid file in dx format", required=True)
parser.add_argument('-i',metavar='<input_SDF_file>',help="input file in SDF format", required=True)
parser.add_argument('-o',metavar='<output_SDF_file>',help="output file in SDF format", required=True)
args = parser.parse_args()
grid_file = args.g
ifile = args.i
ofile = args.o

# Read a dx file which is a result of Flare's GIST calculation.
grid = Grid(grid_file)

# Read a DataBase file in SDF format and keep the hydrogen
suppl = Chem.SDMolSupplier(ifile,removeHs=False)

# Get Van der Waals radii (angstrom) from RDKit's periodic table
# ptable = Chem.GetPeriodicTable()
# radii = [ptable.GetRvdw(atom.GetAtomicNum()) for atom in ligand.GetAtoms()]


# This function will collect the grid point (voxel) displace by the heavy atom:
# 1) If the distance between voxel and atom is less than atom's radius, we define that the voxel will displaced by heavy atom.
# 2) The Van der Waals radii (angstrom) can be available from RDKit's periodic table. 
#    Here is an example:
#    ptable = Chem.GetPeriodicTable()
#    radii = ptable.GetRvdw(AtomicNum)
#    Maybe we can have a dictionary to retrieve the radius.     
# 3) Discard voxels whose absolute value is below 0.5 kcal/mol.
# 4) Values exceeding +3 kcal/mol will be truncated to + 3 kcal/mol.
# 5) Return both original value and truncated value at the same time

def analyze_grid_near_atoms(ligand, grid, radii):
    conf = ligand.GetConformer()
    step_sizes = np.array(grid.delta)
    grid_origin = np.array(grid.origin)
    grid_shape = np.array(grid.grid.shape)

    # Pre-calculate atom positions for all non-hydrogen atoms
    non_h_atoms = [atom for atom in ligand.GetAtoms() if atom.GetAtomicNum() != 1]
    atom_positions = np.array([conf.GetAtomPosition(atom.GetIdx()) for atom in non_h_atoms])
    atom_indices = [atom.GetIdx() for atom in non_h_atoms]
    atom_radii = np.array([radii[atom.GetIdx()] for atom in non_h_atoms])

    # Create a meshgrid for the entire grid
    x, y, z = np.meshgrid(
        np.arange(grid_shape[0]),
        np.arange(grid_shape[1]),
        np.arange(grid_shape[2]),
        indexing='ij'
    )
    all_grid_coords = grid_origin + np.stack([x, y, z], axis=-1) * step_sizes
    all_grid_values = grid.grid
    
    # Use a set to remove duplicated voxels
    displaced_voxels = set()

    for idx, atom_pos, radius in zip(atom_indices, atom_positions, atom_radii):
        # Calculate distances from grid points to the atom
        distances = np.linalg.norm(all_grid_coords - atom_pos, axis=-1)
        
        # Apply filters
        # Use a lower threshold to ignore voxels that do not make a significant contribution.
        # Discard voxels whose absolute value is below 0.5 kcal/mol. 
        # Setting a lower threshold of 0.5 is not based on any theoretical justification but rather on personal experience.
        # Accoridng to Uehara(2016), AutoDock-GIST use the the cutoff = 1.0 kcal/mol to filter voxels.
        # Uehara(2016): https://doi.org/10.3390/molecules21111604
        # 
        mask = (distances <= radius) & ((all_grid_values <= -0.5) | (all_grid_values >= 0.5))
        # Don't use the lower threshold to remove voxels without significant contribution.
        # mask = (distances <= radius)

        filtered_coords = all_grid_coords[mask]
        filtered_values = all_grid_values[mask]
        

        # According to Balius(2017), Values exceeding +3 kcal/mol will be truncated to +3 kcal/mol.
        # Balius(2017) “Testing inhomogeneous solvation theory in structure-based ligand discovery,”
        # Proceedings of the National Academy of Sciences, 114(33), pp. E6839–E6846.
        # Available at: https://doi.org/10.1073/pnas.1703287114.
        #
        # Add unique voxels to the set to remove the duplicated voxel so that each voxel only contibute once.
        # Return a tuple which contains coordinates, value and truncated value
        for coord, value in zip(filtered_coords, filtered_values):
            # truncate the value to +3 kcal/(mol*A^3)
            truncated_value = min(value, 3.0)
            # append the coordinates, value and truncated value into set
            displaced_voxels.add((tuple(np.round(coord, 5)), value, truncated_value))
    
    return list(displaced_voxels)

# Process all molecules in the input SDF file
writer = Chem.SDWriter(ofile)
for mol in suppl:
    if mol is None:
        continue
    
    # Get Van der Waals radii for the current molecule
    ptable = Chem.GetPeriodicTable()
    radii = [ptable.GetRvdw(atom.GetAtomicNum()) for atom in mol.GetAtoms()]
    
    # Analyze the grid near the ligand's heavy atoms
    analysis_results = analyze_grid_near_atoms(mol, grid, radii)
    
    # Calculate GIST-dG-Watdisp
    # A voxel is considered to be displaced if it is contained within the van der Waals radius of an atom during
    # the docking calculation. We sum up the energies of those voxels (eq S8) and multiply the sum by the volume
    # of the voxel (volume = 0.125 Å3) to get a value in kcal/mol.
    # dG_Watdisp = sum(truncated_value) * volume   
 
    # calculate the dG_Watdisp
    gist_dg_watdisp = sum(value for _, _, value in analysis_results) * (-0.125)

    # Add GIST-dG-Watdisp as a property to the molecule
    mol.SetProp("GIST-dG-Watdisp", f"{gist_dg_watdisp:.3f}")
    
    # Write the molecule with the new property to the output file
    writer.write(mol)

writer.close()

print(f"Processing complete. Output written to {ofile}")