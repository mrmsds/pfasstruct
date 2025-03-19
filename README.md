# PFASSTRUCT
Command-line utility to generate iterations of the PFASSTRUCT lists based on a fraction-fluorine and/or substructure-based definition

## HELP
```
usage: pfasstruct.py [-h] [-f FRACF] [-s [SUBS ...]] -u USER -p PWD -l LOC -t TOFILE

desc: a command-line utility that identifies structures from DSSTOX matching a fraction-fluorine and/or substructure-based definition of PFAS

options:
  -h, --help            show this help message and exit
  -f, --fracf FRACF     minimum fraction of fluorine atoms for PFAS definition
  -s, --subs [SUBS ...]
                        SMARTS or SMILES substructure query strings for PFAS definition
  -u, --user USER       DSSTOX database username
  -p, --pwd PWD         DSSTOX database password
  -l, --loc LOC         DSSTOX database location/hostname
  -t, --tofile TOFILE   XLSX filename to write output
```

## EXAMPLE
```
py pfasstruct.py -u YOUR_DSSTOX_USER -p YOUR_DSSTOX_PASS -l mysql-ip-m.epa.gov -f 0.3 -s C(F)(F)(C(F))F FC(F)(F)(C~C(F)(F)) C(F)(F)(C(F)(F)) C(F)(F)[B,O,N,P,S,Si]C(F)(F) -t pfasstruct_test.xlsx
```