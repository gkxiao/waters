## Enhancing Docking Scores with Flare GIST: A Case Study on 15-PGDH Inhibitors
![Enhancing Docking Score with GIST (GIST修正对接打分的示意图)](https://github.com/gkxiao/waters/blob/main/15-GPDH/enchancing-docking-score-with-GIST.png)
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
| Affinity-Corr (kcal/mol)| -9.53     | <strong>-13.93</strong>    |
| Exp ΔG (kcal/mol)       | -10.34    | -13.96    |

### Calculation Formulas
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
gist_dg_watdisplace.py -g dg.dx -i 4.sdf -o 4_watdisp.sdf
```

- 38
```
gist_dg_watdisplace.py -g dg.dx -i 38.sdf -o 38_watdisp.sdf
```




