#!/bin/bash

for atom in $(find ../atoms/ -type f -name "*py" ! -name "handler.py")
do
    atom_path=$(dirname ${atom})
    mv ${atom} "${atom_path}/handler.py"
    echo "Atom name updated: ${atom}"
done
