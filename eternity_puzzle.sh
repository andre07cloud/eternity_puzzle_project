#!/bin/bash

# Tableau des noms des instances
instances=("eternity_A.txt" "eternity_B.txt" "eternity_C.txt" "eternity_D.txt" "eternity_E.txt" "eternity_complet.txt")

# Parcourir chaque instance
for instance in "${instances[@]}"
do
    # Nom du fichier de sortie correspondant à l'instance
    output_file="output_${instance}.txt"
    
    # Lancer le script avec chaque instance et rediriger la sortie vers le fichier de sortie
    python3 main.py --agent=advanced --infile="instances/${instance}" > "$output_file"
done
