import pandas as pd
import re
from pathlib import Path

pd.set_option('display.max_columns', None)

def parsingDisgenetDiseases():
    #source file
    disgenetColumns = ['entrezGeneIds','useless1','useless2','useless3','diseaseId','diseaseName','diseaseType']
    numColumns = [0,4,5,6]
    p = Path('Datasets/disease/disgenetDiseases.tsv')
    disgenet = pd.read_csv(p, sep='\t', header=0, names=disgenetColumns, usecols=numColumns, index_col=False,
                          dtype={'entrezGeneIds': str} )

    # deleting useless rows
    for index, row in disgenet.iterrows():
        # disease type
        if (row['diseaseType'] != 'disease'):
            disgenet.drop(index, inplace=True)

    #standardizing columns
    for index, row in disgenet.iterrows():
        #entrez gene ids
        id = re.search("[^0-9]*([0-9]*)",row['entrezGeneIds'])
        row['entrezGeneIds'] = id.group(1)

        # disease name
        elem1 = row['diseaseName'].replace(",", " -")
        elem2 = elem1.replace(";", " -")
        elem = str(elem2).lower()
        row['diseaseName'] = elem

    # grouping tuples
    disgenet['entrezGeneIds'] = disgenet.groupby(['diseaseId'])['entrezGeneIds'].transform(
        lambda x: '|'.join(x))
    disgenet = disgenet.drop_duplicates()

    # output
    p = Path('DatasetsFormatted/disease/disgenetDiseases.csv')
    disgenet.to_csv(p, index=False, columns=['diseaseId','diseaseName','entrezGeneIds'])