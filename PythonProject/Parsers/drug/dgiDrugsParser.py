import pandas as pd
from pathlib import Path
import re

pd.set_option('display.max_columns', None)

def parsingDgiDrugs():
    #source file
    dgiColumns = ['useless1','useless2','entrezGeneIds','useless3','useless4','drugName','useless6',
                  'useless5','useless7','pubmedId']
    numColumns = [2,5,9]
    p = Path('Datasets/drug/dgiDrugs.tsv')
    dgi = pd.read_csv(p, sep='\t', header=0, names=dgiColumns, usecols=numColumns, index_col=False,
                          dtype={'entrezGeneIds': str, 'drugName': str, 'pubmedId': str} )

    # deleting useless rows
    for index, row in dgi.iterrows():

        # drug name
        if (row['drugName'] == '' or re.match("[^a-zA-Z]",str(row['drugName']))):
            dgi.drop(index, inplace=True)

        # entrez gene ids
        elif (pd.isnull(row['entrezGeneIds'])):
            dgi.drop(index, inplace=True)

        #pubmed id and standardize drug name
        elif(pd.isnull(row['pubmedId'])):
            row['pubmedId'] = ''
    dgi = dgi.drop_duplicates()

    #rename
    for index, row in dgi.iterrows():
         elem = str(row['drugName']).lower()
         row['drugName'] = elem
    dgi = dgi.drop_duplicates()

    #standardizing columns
    for index, row in dgi.iterrows():

        # drug name
        elem1 = str(row['drugName']).replace(","," -")
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

        # pubmed id
        if not (pd.isnull(row['pubmedId'])):
            id = re.split(",", row['pubmedId'])
            id = list(dict.fromkeys(id))
            elem = ''
            for el in id:
                elem += el + ","
            elem = elem[:-1]
            row['pubmedId'] = elem
        else:
            row['pubmedId'] = ''

    dgi = dgi.drop_duplicates()

    # grouping tuples
    dgi['entrezGeneIds'] = dgi.groupby(['drugName'])['entrezGeneIds'].transform(lambda x: '|'.join(x))
    dgi['pubmedId'] = dgi.groupby(['drugName'])['pubmedId'].transform(lambda x: ','.join(x))
    dgi = dgi.drop_duplicates()

    # standardizing columns pt.2
    for index, row in dgi.iterrows():

        # entrez ids
        id = re.split("\|", row['entrezGeneIds'])
        id = list(dict.fromkeys(id))
        elem = ''
        for el in id:
            elem += el + "|"
        elem = elem[:-1]
        row['entrezGeneIds'] = elem

        # pubmed id
        if not (pd.isnull(row['pubmedId'])):
            id = re.split(",", row['pubmedId'])
            id = list(dict.fromkeys(id))
            elem = ''
            for el in id:
                if(el != ''):
                    elem += el + "|"
            elem = elem[:-1]
            row['pubmedId'] = elem
        else:
            row['pubmedId'] = ''

    dgi = dgi.drop_duplicates()

    # output
    p = Path('DatasetsFormatted/drug/dgiDrugs.csv')
    dgi.to_csv(p, index=False, columns=['drugName', 'entrezGeneIds', 'pubmedId'])
