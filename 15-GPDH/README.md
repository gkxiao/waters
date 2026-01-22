## 🔬Why Docking Missed a 400× Binder — Revealing Hidden Water Contributions with GIST

![Compound 4 and 38](https://github.com/gkxiao/waters/blob/main/15-GPDH/Compound-4-38-and-their-activity.png)

In the discovery of 15-PGDH inhibitors, a classic medicinal chemistry insight paid off: displacing high-energy waters led to a >400-fold affinity gain, from compound 4 to 38 (Dodda, L. S., et al. J. Med. Chem. https://lnkd.in/gPgeMVni).

Yet, standard molecular docking struggled here.
While GNINA predicted the affinity of compound 4 reasonably well, it failed to rank the much stronger binder 38 above it.

This makes the system a great test case for explicit solvation analysis.

Revisiting the problem with Flare GIST shows why:

✅ GIST hydration sites align well with crystallographic waters

✅ The GIST-derived desolvation free energy captures the energetic benefit of displacing high-energy waters

✅ Adding this term as a correction layer to docking scores reproduces the correct relative binding free energies

Importantly, GIST is not a replacement for docking or FEP.
It acts as a physics-based solvation layer, making otherwise invisible water-driven effects explicit — particularly in cases where water displacement dominates the binding gain.

Read the full case study📚, please refer to the blog post: https://lnkd.in/g_zp2ew8
### Visualization of Results
You can request a free Flare Visualizer (https://cresset-group.com/software/download-flare-visualizer/) to visualize and analyze my calculation results (15-PGDH-apo-gist.flr), or apply for a free Flare demo license (https://cresset-group.com/about/contact-us/) to reproduce my calculations.

## Apo-GIST Analysis Identifies Opportunities for Lead Compound Optimization
![Unhappy water in the pocket](http://blog.molcalx.com.cn/wp-content/uploads/2026/01/Compound-4-38-water-displacement-and-binding-mode.png)

As shown in the figure, apo-GIST analysis identifies two high-energy hydration sites (#4 and #19) within the binding pocket, which spatially coincide with the crystallographic waters HOH483 and HOH485, respectively. The positive hydration free energies of these sites indicate thermodynamically unfavorable water molecules, suggesting that their displacement by ligand atoms is expected to provide a favorable contribution to binding free energy upon ligand optimization.

## Correct the docking score using ΔG<sub>watdisp</sub> calculated by Flare GIST


| Metric                  | 4         | 38        |
|-------------------------|-----------|-----------|
| gauss_1                 | 122.46680 | 149.03520 |
| gauss_2                 | 1420.47168| 1643.15222|
| repulsion               | 5.23956   | 6.98573   |
| hydrophobic             | 94.15118  | 101.49037 |
| non_dir_h_bond          | 1.99749   | 2.97978   |
| Affinity (kcal/mol)     | -9.53     | -10.23    |
| CNNaffinity             | 6.77      | 7.39      |
| ΔG<sub>watdisp</sub> (kcal/mol) | -18.144 | -21.846 |
| Affinity-Corr (kcal/mol)| <strong>-9.53</strong>     | <strong>-13.93</strong>    |
| Exp ΔG (kcal/mol)       | -10.34    | -13.96    |

As shown in the table, GNINA’s scoring terms indicate that Compound 38 forms stronger non-directional hydrogen-bond interactions and more favorable hydrophobic contacts than Compound 4. However, these improvements translate into only a small difference in predicted binding affinity (ΔΔG ≈ 0.7 kcal/mol), far below the experimental value of 3.62 kcal/mol.

This discrepancy suggests that interaction-based scoring alone is insufficient to capture the dominant energetic contribution in this optimization step. In contrast, when the GIST-derived water displacement free energy (ΔG_watdisp) is incorporated as an explicit correction term, the corrected binding free energies show quantitative agreement with experiment.


As shown in the table, GNINA’s scoring breakdown indicates that Compound 38 forms stronger non-directional hydrogen-bond interactions and more favorable hydrophobic contacts than Compound 4, as reflected by the larger non_dir_h_bond and hydrophobic terms. However, these improvements are only marginally reflected in the predicted binding affinities, yielding a ΔΔG of approximately 0.7 kcal/mol between Compounds 4 and 38, substantially smaller than the experimental value of 3.62 kcal/mol. This discrepancy suggests that interaction-based scoring alone is insufficient to capture the dominant contribution in this optimization step. In contrast, when the GIST-derived water displacement free energy ΔG<sub>watdisp</sub> is incorporated as an explicit correction term, the resulting corrected affinities (Affinity-Corr) show quantitative agreement with the experimental binding free energies. The calculation formula is as follows:

$$
\begin{aligned}
\Delta G_{\text{bind}}^{\text{docking-GIST-corr}} = \Delta G_{\text{bind}}^{\text{docking}} + \Delta G_{\text{watdisp}} \cdots(1)
\end{aligned}
$$


$$
\begin{align}
\Delta \Delta G_{\text{bind}}^{\text{docking-GIST-corr}} &= \Delta \Delta G_{\text{bind}}^{\text{docking}} + \Delta \Delta G_{\text{watdisp}} \\
&= -0.7 + (-3.70) \\
&= -4.40 \ \text{kcal/mol} \cdots(2)
\end{align}
$$

$$
\Delta \Delta G_{\text{watdisp}} = -21.846 - (-18.144) = -3.70 \ \text{kcal/mol} \cdots(3)
$$

$$
\Delta \Delta G_{\text{bind}}^{\text{Exp}} = -3.62 \ \text{kcal/mol} \cdots(4)
$$

## Gnina score of Compound 4 and 38

- Compound 4

```
gnina -r 9pfl_dry.pdb -l 4.sdf -o 4_gnina_score.sdf --score_only
              _
             (_)
   __ _ _ __  _ _ __   __ _
  / _` | '_ \| | '_ \ / _` |
 | (_| | | | | | | | | (_| |
  \__, |_| |_|_|_| |_|\__,_|
   __/ |
  |___/

gnina v1.3 master:97fa6bc+   Built Oct  3 2024.
gnina is based on smina and AutoDock Vina.
Please cite appropriately.

Commandline: gnina -r 9pfl_dry.pdb -l 4.sdf -o 4_gnina_score.sdf --score_only

## Name gauss(o=0,_w=0.5,_c=8) gauss(o=3,_w=2,_c=8) repulsion(o=0,_c=8) hydrophobic(g=0.5,_b=1.5,_c=8) non_dir_h_bond(g=-0.7,_b=0,_c=8) num_tors_div
Affinity: -9.52626 (kcal/mol)
CNNscore: 0.70952
CNNaffinity: 6.76675
CNNvariance: 0.03029
Intramolecular energy: -0.42520
Term values, before weighting:
## 4 122.46680 1420.47168 5.23956 94.15118 1.99749 0.00000
```

- Compound 38
```
nina -r 9pfl_dry.pdb -l 38.sdf -o 38_gnina_score.sdf --score_only
              _
             (_)
   __ _ _ __  _ _ __   __ _
  / _` | '_ \| | '_ \ / _` |
 | (_| | | | | | | | | (_| |
  \__, |_| |_|_|_| |_|\__,_|
   __/ |
  |___/

gnina v1.3 master:97fa6bc+   Built Oct  3 2024.
gnina is based on smina and AutoDock Vina.
Please cite appropriately.

Commandline: gnina -r 9pfl_dry.pdb -l 38.sdf -o 38_gnina_score.sdf --score_only

## Name gauss(o=0,_w=0.5,_c=8) gauss(o=3,_w=2,_c=8) repulsion(o=0,_c=8) hydrophobic(g=0.5,_b=1.5,_c=8) non_dir_h_bond(g=-0.7,_b=0,_c=8) num_tors_div
Affinity: -10.22557 (kcal/mol)
CNNscore: 0.86695
CNNaffinity: 7.38772
CNNvariance: 0.09617
Intramolecular energy: -0.51773
Term values, before weighting:
## 38 149.03520 1643.15222 6.98573 101.49037 2.97978 0.00000
```

## Computation of ΔG<sub>watdisp</sub> for Compounds 4 and 38
- 4
```
gist_dG_watdisplace.py -g dG.dx -i 4.sdf -o 4_watdisp.sdf
```

- 38
```
gist_dG_watdisplace.py -g dG.dx -i 38.sdf -o 38_watdisp.sdf
```

Where, ***dG.dx*** can be exported from the Flare Project file **15-PGDH-apo-gist.flr**.



