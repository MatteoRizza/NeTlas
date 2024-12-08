import pandas as pd
import re
from pathlib import Path

pd.set_option('display.max_columns', None)

def parsingBiosnapDiseases():
    #source file
    biosnapColumns = ['diseaseId','diseaseName','entrezGeneIds']
    numColumns = [0,1,2]
    p = Path('Datasets/disease/biosnapDiseases.tsv')
    biosnap = pd.read_csv(p, sep='\t', header=0, names=biosnapColumns, usecols=numColumns, index_col=False,
                          dtype={'entrezGeneIds': str} )

    # standardizing columns
    for index, row in biosnap.iterrows():

        # disease name
        elem1 = row['diseaseName'].replace(",", " -")
        elem2 = elem1.replace(";", " -")
        elem = str(elem2).lower()
        row['diseaseName'] = elem

    # grouping tuples
    biosnap['entrezGeneIds'] = biosnap.groupby(['diseaseId'])['entrezGeneIds'].transform(
        lambda x: '|'.join(x))
    biosnap = biosnap.drop_duplicates()

    # output
    p = Path('DatasetsFormatted/disease/biosnapDiseases.csv')
    biosnap.to_csv(p, index=False, columns=['diseaseId','diseaseName','entrezGeneIds'])