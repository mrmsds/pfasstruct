# PFASSTRUCT
Command-line utility to generate iterations of the PFASSTRUCT lists matching a fraction-fluorine and/or substructure-based definition

## HELP
```
usage: pfasstruct [-h] [-f FRACF] [-s [SUBS ...]] -u USER -p PWD -l LOC -t TOFILE

desc: a command-line utility that identifies structures from DSSTOX matching a fraction-fluorine and/or substructure-based definition of PFAS

options:
  -h, --help            show this help message and exit
  -f, --fracf FRACF     minimum fraction of fluorine atoms for PFAS definition
  -s, --subs [SUBS ...]
                        SMARTS substructure query strings for PFAS definition
  -u, --user USER       DSSTOX database username
  -p, --pwd PWD         DSSTOX database password
  -l, --loc LOC         DSSTOX database location/hostname
  -t, --tofile TOFILE   XLSX filename to write output
```

## POWERSHELL
```
.\pfasstruct -u YOUR_DSSTOX_USERNAME -p YOUR_DSSTOX_PASSWORD -l mysql-ip-m.epa.gov -f 0.3 -s "C(F)(F)(C(F))F" "C(F)(F)(C(F)(F))" "FC(F)(F)(C~C(F)(F))" "C(F)(F)[B,O,N,P,S,Si]C(F)(F)" -t pfasstruct.xlsx
```

## CMD
```
pfasstruct -u YOUR_DSSTOX_USERNAME -p YOUR_DSSTOX_PASSWORD -l mysql-ip-m.epa.gov -f 0.3 -s C(F)(F)(C(F))F C(F)(F)(C(F)(F)) FC(F)(F)(C~C(F)(F)) C(F)(F)[B,O,N,P,S,Si]C(F)(F) -t pfasstruct.xlsx
```

## PYTHON
```
py pfasstruct.py -u YOUR_DSSTOX_USERNAME -p YOUR_DSSTOX_PASSWORD -l mysql-ip-m.epa.gov -f 0.3 -s C(F)(F)(C(F))F C(F)(F)(C(F)(F)) FC(F)(F)(C~C(F)(F)) C(F)(F)[B,O,N,P,S,Si]C(F)(F) -t pfasstruct.xlsx
```