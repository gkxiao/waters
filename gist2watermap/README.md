# Tutorial: Converting GIST Results to Watermap-Style Files and Visualizing Them

This tutorial describes how to use `csv2watermap_mae.py` to convert GIST calculation results into a Schrödinger Watermap-compatible `.mae` file, then visualize it in PyMOL, and optionally use it in Maestro / Ligand Designer.

## Introduction

Watermap is an expensive commercial module in Schrödinger for predicting hydration sites and thermodynamic properties. GIST (Grid Inhomogeneous Solvation Theory) is a highly cost-effective alternative, but its raw output cannot be directly used in Maestro as Watermap results. This script converts GIST output (CSV format) into a `.mae` file that mimics the Watermap output, enabling seamless integration into a Maestro-based workflow.

## Dependencies

- Python 3
- `csv2watermap_mae.py` (this script)
- PyMOL (for visualization)
- Schrödinger Maestro (optional, for Ligand Designer)

## Usage

Run the following command in your terminal:

```bash
python csv2watermap_mae.py -o 4zlz_apo-GIST.mae --title 4zlz_apo-GIST apo_hs.csv
```

### Arguments

- `-o 4zlz_apo-GIST.mae` – output `.mae` file name.
- `--title 4zlz_apo-GIST` – structure title (e.g., protein name + system description).
- `apo_hs.csv` – input file, i.e., GIST hydration site results, containing coordinates, thermodynamic properties (e.g., ΔG), occupancy, etc.

After execution, a `4zlz_apo-GIST.mae` file will be generated in the current directory. This file is Watermap-style Maestro structure output, with Watermap-compatible properties such as `r_watermap_deltaG` and `r_watermap_occupancy` written into it.

## PyMOL Visualization

### 1. Load the `.mae` file

Start PyMOL and load the generated `.mae` file:

```pymol
load 4zlz_apo-GIST.mae
```

By default, the object name will be `4zlz_apo-GIST` (if you use a different filename, the object name will change accordingly; use `get_names()` to check).

### 2. Display hydration sites as spheres

```pymol
cmd.show("spheres", "4zlz_apo-GIST")
```

### 3. Color by ΔG value

```pymol
cmd.spectrum("properties['r_watermap_deltaG']", "green white red", "4zlz_apo-GIST", minimum=-5, maximum=5)
```

Explanation:

- `properties['r_watermap_deltaG']` – reads the ΔG property from the `.mae` file.
- Color gradient: green (favorable hydration site, more negative ΔG) → white → red (unfavorable hydration site, more positive ΔG).
- `minimum=-5, maximum=5` – defines the energy range for coloring (in kcal/mol); adjust according to your actual ΔG values.

### 4. Other useful visualizations

Color by occupancy:

```pymol
cmd.spectrum("properties['r_watermap_occupancy']", "blue white orange", "4zlz_apo-GIST", minimum=0, maximum=1)
```

Display as dots:

```pymol
cmd.show("dots", "4zlz_apo-GIST")
```

## Usage in Maestro / Ligand Designer

1. Open Schrödinger Maestro.
2. Import `4zlz_apo-GIST.mae` via `File → Import`.
3. After import, hydration sites will be displayed in the same style as Watermap results.
4. In the **Ligand Designer** panel, these sites can be treated as Watermap results for water replacement, displacement, and water network analysis in the binding site.

## Notes

- This conversion is **only a format-level adaptation**; it does not modify any scientific data from the GIST calculation.
- If the object name in PyMOL is not `4zlz_apo-GIST`, replace it with the actual object name in the commands above.
- Ensure that `apo_hs.csv` contains all required fields (coordinates, ΔG, occupancy, etc.), otherwise the resulting `.mae` file may be missing some properties.
- If you do not have Maestro, you can still perform most visualization tasks in PyMOL.

---

