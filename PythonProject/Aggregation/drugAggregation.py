import pandas as pd
import re
from tqdm import tqdm
from pathlib import Path

def drugAggregation():
    #sources
    numColumns = [0, 1, 2]
    p = Path('DatasetsFormatted/drug/biogridDrugs.csv')
    biogrid = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIds':str, 'pubmedId': str})
    p = Path('DatasetsFormatted/drug/dgiDrugs.csv')
    dgi = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIds':str, 'pubmedId': str})

    #join
    result = pd.merge(biogrid, dgi, on=['drugName'], how='outer')

    #merging other data
    result['pubmedId'] = 'AAA'
    result['entrezGeneIds'] = 'AAA'
    for index, row in tqdm(result.iterrows(), total=result.shape[0]):

        # pubmed id
        if(pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = ''
        elif (not pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_x']
        elif (pd.isnull(row['pubmedId_x']) and not pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_y']
        else:
            row['pubmedId'] = row['pubmedId_x'] + "|" + row['pubmedId_y']
        det = re.split("\|", row['pubmedId'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['pubmedId'] = detect

        # entrez gene ids
        if (pd.isnull(row['entrezGeneIds_x']) and pd.isnull(row['entrezGeneIds_y'])):
            row['entrezGeneIds'] = ''
        elif (pd.isnull(row['entrezGeneIds_x']) and not pd.isnull(row['entrezGeneIds_y'])):
            row['entrezGeneIds'] = row['entrezGeneIds_y']
        elif (not pd.isnull(row['entrezGeneIds_x']) and pd.isnull(row['entrezGeneIds_y'])):
            row['entrezGeneIds'] = row['entrezGeneIds_x']
        else:
            row['entrezGeneIds'] = row['entrezGeneIds_x'] + "|" + row['entrezGeneIds_y']
        det = re.split("\|", row['entrezGeneIds'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['entrezGeneIds'] = detect

    # output
    p = Path('DatasetsFormatted/drug/drugs.csv')
    result.to_csv(p, index=False, columns=['drugName', 'entrezGeneIds', 'pubmedId'])