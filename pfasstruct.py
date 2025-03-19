from argparse import ArgumentParser
from contextlib import closing
from indigo import Indigo, IndigoException
from mysql.connector import connect
from numpy import array, sum
from pandas import read_sql_query
from warnings import filterwarnings

# Parse CLA
parser = ArgumentParser(description='desc: a command-line utility that identifies structures from DSSTOX matching a fraction-fluorine and/or substructure-based definition of PFAS')
parser.add_argument('-f', '--fracf', type=float, help='minimum fraction of fluorine atoms for PFAS definition')
parser.add_argument('-s', '--subs', nargs='*', help='SMARTS or SMILES substructure query strings for PFAS definition')
parser.add_argument('-u', '--user', help='DSSTOX database username', required=True)
parser.add_argument('-p', '--pwd', help='DSSTOX database password', required=True)
parser.add_argument('-l', '--loc', help='DSSTOX database location/hostname', required=True)
parser.add_argument('-t', '--tofile', help='XLSX filename to write output', required=True)
args = parser.parse_args()

# Configure database connection with CLA
config = {
    'host': args.loc,
    'database': 'prod_dsstox',
    'user': args.user,
    'password': args.pwd,
    'charset': 'utf8',
    'collation': 'utf8_general_ci',
    'use_unicode': True
}

# Define initial filtering SQL query for PFAS candidate compounds
query = ('SELECT gs.dsstox_substance_id AS DTXSID, c.dsstox_compound_id AS DTXCID, gs.casrn AS CASRN, gs.preferred_name AS PREF_NAME, c.smiles AS SMILES '
         'FROM compounds c JOIN generic_substance_compounds gsc ON gsc.fk_compound_id = c.id '
         'JOIN generic_substances gs ON gs.id = gsc.fk_generic_substance_id '
         'WHERE c.mol_formula REGEXP BINARY \'F[^a-z]\' ' # Has fluorine
         'AND c.mol_formula REGEXP BINARY \'C[^a-z]\' ' # Has carbon
         'AND (c.smiles REGEXP BINARY \'F[)]?C\' OR c.smiles REGEXP BINARY \'C[(]?F\') ' # Has C-F single bond
         'AND NOT c.mol_file LIKE \'%RAD%\'') # Has no radicals

# Ignore MySQL/pandas warnings
filterwarnings('ignore', category=UserWarning)
# Open the connection and execute the query with pandas
with closing(connect(**config)) as conn:
    cmpds = read_sql_query(query, conn)

# Initialize Indigo instance
indigo = Indigo()

# Compute fraction fluorine atoms (# F / # !H) from an Indigo molecule
def fracf(mol):
    el = array([a.atomicNumber() for a in mol.iterateAtoms()])
    return sum(el == 9) / sum(el > 1)

# Convert input substructure strings to Indigo query molecules
qmols = [indigo.loadQueryMolecule(s) for s in args.subs]

# Match a molecule against all input query molecule substructures
def subs(mol):
    matcher = indigo.substructureMatcher(mol)
    return [str(i + 1) for i, q in enumerate(qmols) if matcher.match(q)]

# Test a SMILES string against both components of the PFAS definition
def test(smi):
    results = []
    try:
        mol = indigo.loadMolecule(smi)
        try:
            if fracf(mol) >= args.fracf:
                results.append('F')
        except IndigoException:
            pass

        try:
            results.extend(subs(mol))
        except IndigoException:
            pass
    except IndigoException:
        pass

    return '.'.join(results)

cmpds['PFAS_MATCHES'] = cmpds['SMILES'].apply(test)
pfas = cmpds[cmpds['PFAS_MATCHES'] != '']
print(f'Identified {len(pfas)} PFAS compounds')
pfas.to_excel(args.tofile, index=False)
print(f'Saved to file {args.tofile}')