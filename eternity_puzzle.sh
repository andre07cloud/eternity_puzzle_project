#!/bin/bash

# Tableau des noms des instances
instances=("eternity_A.txt" "eternity_B.txt" "eternity_C.txt" "eternity_D.txt" "eternity_E.txt" "eternity_complet.txt")

# Parcourir chaque instance
for instance in "${instances[@]}"
do
    # Lancer le script avec chaque instance
    python3 main.py --agent=advanced --infile="instances/${instance}"
done

