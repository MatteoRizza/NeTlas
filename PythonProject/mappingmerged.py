import pandas as pd
from pathlib import Path

# This script was used only once to join two tables of associations between gene identifiers
# and obtain the table uniprot-entrez-ensembl-hgnc.xlsx

#join
p = Path('Datasets/mapping/uniprot-entrez-ensembl.xlsx')
mapping1 = pd.read_excel(p, dtype={'entrezgeneid':str})
p = Path('Datasets/mapping/entrez-hgnc-ensembl.xlsx')
mapping2 = pd.read_excel(p, dtype={'entrezgeneid':str})
result = pd.merge(mapping1,mapping2,on='entrezgeneid',how='outer')

#aggregate ensemble column
for index, row in result.iterrows():
    if(pd.isnull(row['ensemblid_x'])):
        row['ensemblid_x'] = row['ensemblid_y']
result.drop('ensemblid_y', axis=1, inplace=True)
result.rename(columns={'ensemblid_x': 'ensemblid'}, inplace=True)

#delete duplicates
result = result.drop_duplicates()

#output
p = Path('Datasets/mapping/uniprot-entrez-ensembl-hgnc.xlsx')
result.to_excel(p, columns=['uniprotid','entrezgeneid','ensemblid','hgncsymbol'])