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



