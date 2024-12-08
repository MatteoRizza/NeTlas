import pandas as pd
from pathlib import Path
from tqdm import tqdm
import re

pd.set_option('display.max_columns', None)

def parsingBiogrid():
    #source file
    biogridColumns = ['useless1','entrezGeneIdA','entrezGeneIdB','useless2','useless3','useless4','useless5',
                      'useless8', 'useless9','useless6','useless7','detectionMethod','interactionType',
                      'author','pubmedId','taxidA','taxidB','throughput']
    numColumns = [1,2,11,12,13,14,15,16,17]
    p = Path('Datasets/gene/biogrid.txt')
    biogrid = pd.read_csv(p, sep='\t', header=0, names=biogridColumns, usecols=numColumns, index_col=False,
                          dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'taxidA': str, 'taxidB': str} )
    #identification
    for index, row in biogrid.iterrows():
        #ordering
        if(str(row['entrezGeneIdA']) > str(row['entrezGeneIdB'])):
            idA = row['entrezGeneIdA']
            idB = row['entrezGeneIdB']
            row['entrezGeneIdA'] = idB
            row['entrezGeneIdB'] = idA

    # grouping tuples
    biogrid['detectionMethod'] = biogrid.groupby(['entrezGeneIdA', 'entrezGeneIdB'])['detectionMethod'].transform(
        lambda x: '|'.join(x))
    print("group by 1 done")
    biogrid['author'] = biogrid.groupby(['entrezGeneIdA', 'entrezGeneIdB'])['author'].transform(
        lambda x: '|'.join(x))
    print("group by 2 done")
    biogrid['pubmedId'] = biogrid.groupby(['entrezGeneIdA', 'entrezGeneIdB'])['pubmedId'].transform(
        lambda x: '|'.join(x))
    print("group by 3 done")
    biogrid['interactionType'] = biogrid.groupby(['entrezGeneIdA', 'entrezGeneIdB'])['interactionType'].transform(
        lambda x: '|'.join(x))
    print("group by 4 done")
    biogrid['throughput'] = biogrid.groupby(['entrezGeneIdA', 'entrezGeneIdB'])['throughput'].transform(
        lambda x: '|'.join(x))
    print("group by 5 done")
    biogrid = biogrid.drop_duplicates()

    #standardizing columns
    for index, row in tqdm(biogrid.iterrows(), total=biogrid.shape[0]):

        #detection method
        det = re.split("\|", row['detectionMethod'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['detectionMethod'] = detect

        #pubmed id
        id = re.split("\|", row['pubmedId'])
        id = list(dict.fromkeys(id))
        elem = ''
        for el in id:
            el1 = el.replace("PUBMED:", "")
            elem += el1 + "|"
        elem = elem[:-1]
        row['pubmedId'] = elem

        # author
        id = re.split("\|", row['author'])
        id = list(dict.fromkeys(id))
        elem = ''
        for el in id:
            elem += el + "|"
        elem = elem[:-1]
        row['author'] = elem

        #interaction type
        det = re.split("\|", row['interactionType'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            if (el == 'physical'):
                el1 = 'physical association'
            else:
                el1 = 'genetic interaction'
            detect += el1 + "|"
        detect = detect[:-1]
        row['interactionType'] = detect

        #throughput
        t = re.split("\|", row['throughput'])
        t = list(dict.fromkeys(t))
        detect = ''
        for el in t:
            if (el == 'High Throughput'):
                el1 = 'high throughput'
            else:
                el1 = 'small scale'
            detect += el1 + "|"
        detect = detect[:-1]
        row['throughput'] = detect

    #deleting useless rows
    for index, row in tqdm(biogrid.iterrows(), total=biogrid.shape[0]):

        # entrez gene id A
        if (row['entrezGeneIdA'] == ''):
            biogrid.drop(index, inplace=True)

        # entrez gene id B
        elif (row['entrezGeneIdB'] == ''):
            biogrid.drop(index, inplace=True)

        # entrez gene ids identical
        elif (row['entrezGeneIdA'] == row['entrezGeneIdB']):
            biogrid.drop(index, inplace=True)

        # taxid A
        elif (not re.match("9606", row['taxidA'])):
            biogrid.drop(index, inplace=True)

        # taxid B
        elif (not re.match("9606", row['taxidB'])):
            biogrid.drop(index, inplace=True)

    biogrid = biogrid.drop_duplicates()

    # adding useful columns
    p = Path('Datasets/mapping/uniprot-entrez-ensembl-hgnc.xlsx')
    mapping = pd.read_excel(p, dtype={'entrezgeneid': str})
    result1 = pd.merge(biogrid, mapping, left_on='entrezGeneIdA', right_on='entrezgeneid', how='left')
    result1.drop('entrezgeneid', axis=1, inplace=True)
    result1.rename(columns={'ensemblid': 'ensemblIdA', 'uniprotid': 'uniprotIdA',
                            'hgncsymbol': 'hgncSymbolA'}, inplace=True)
    result = pd.merge(result1, mapping, left_on='entrezGeneIdB', right_on='entrezgeneid', how='left')
    result.drop('entrezgeneid', axis=1, inplace=True)
    result.rename(columns={'ensemblid': 'ensemblIdB', 'uniprotid': 'uniprotIdB',
                           'hgncsymbol': 'hgncSymbolB'}, inplace=True)

    # output
    p = Path('DatasetsFormatted/gene/biogrid.csv')
    result.to_csv(p, index=False, columns=['uniprotIdA', 'uniprotIdB','entrezGeneIdA', 'entrezGeneIdB',
                                           'ensemblIdA', 'ensemblIdB','hgncSymbolA', 'hgncSymbolB',
                                           'detectionMethod', 'interactionType','pubmedId', 'author','throughput'])