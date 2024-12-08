import pandas as pd
from pathlib import Path
import re

pd.set_option('display.max_columns', None)

def parsingBiogridDrugs():
    #source file
    biogridColumns = ['useless1','useless2','entrezGeneIds','useless3','useless4','useless5','useless6',
                      'organism','useless7','useless8','author','pubmedId','useless9','useless10','drugName']
    numColumns = [2,7,10,11,14]
    p = Path('Datasets/drug/biogridDrugs.txt')
    biogrid = pd.read_csv(p, sep='\t', header=0, names=biogridColumns, usecols=numColumns, index_col=False,
                          dtype={'entrezGeneIds': str, 'pubmedId': str} )

    # deleting useless rows
    for index, row in biogrid.iterrows():

        # drug name
        if (row['drugName'] == ''):
            biogrid.drop(index, inplace=True)

        # organism
        elif (not re.match("Homo sapiens", row['organism'])):
            biogrid.drop(index, inplace=True)
    biogrid = biogrid.drop_duplicates()

    #rename
    for index, row in biogrid.iterrows():
         elem = row['drugName'].lower()
         row['drugName'] = elem
    biogrid = biogrid.drop_duplicates()

    # grouping tuples
    biogrid['entrezGeneIds'] = biogrid.groupby(['drugName'])['entrezGeneIds'].transform(
        lambda x: '|'.join(x))
    biogrid['pubmedId'] = biogrid.groupby(['drugName'])['pubmedId'].transform(
        lambda x: '|'.join(x))
    biogrid['author'] = biogrid.groupby(['drugName'])['author'].transform(
        lambda x: '|'.join(x))

    biogrid = biogrid.drop_duplicates()

    #standardizing columns
    for index, row in biogrid.iterrows():

        # drug name
        elem1 = row['drugName'].replace(","," -")
        elem = elem1.replace(";", " -")
        row['drugName'] = elem

        #entrez ids
        id = re.split("\|", row['entrezGeneIds'])
        id = list(dict.fromkeys(id))
        elem = ''
        for el in id:
            elem += el + "|"
        elem = elem[:-1]
        row['entrezGeneIds'] = elem

        # author
        id = re.split("\|", row['author'])
        id = list(dict.fromkeys(id))
        elem = ''
        for el in id:
            elem += el + "|"
        elem = elem[:-1]
        row['author'] = elem

        # pubmed id
        id = re.split("\|", row['pubmedId'])
        id = list(dict.fromkeys(id))
        elem = ''
        for el in id:
            elem += el + "|"
        elem = elem[:-1]
        row['pubmedId'] = elem

    biogrid = biogrid.drop_duplicates()

    # output
    p = Path('DatasetsFormatted/drug/biogridDrugs.csv')
    biogrid.to_csv(p, index=False, columns=['drugName', 'entrezGeneIds', 'pubmedId', 'author'])