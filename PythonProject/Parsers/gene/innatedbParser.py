import pandas as pd
from pathlib import Path
import re

pd.set_option('display.max_columns', None)

def parsingInnatedb():
    #source file
    innatedbColumns = ['useless1','useless2','ensemblIdA','ensemblIdB','useless3','useless4','detectionMethod',
                       'author','pubmedId','taxidA','taxidB','interactionType']
    numColumns = [2,3,6,7,8,9,10,11]
    p = Path('Datasets/gene/innatedb.mitab')
    innatedb = pd.read_csv(p, sep='\t', header=0, names=innatedbColumns, usecols=numColumns, index_col=False )

    #identification
    for index, row in innatedb.iterrows():
        #ensembl id A
        idA = re.search("ensembl:([^\|]*)\|*",row['ensemblIdA'])
        if (idA != None):
            row['ensemblIdA'] = idA.group(1)
        else:
            row['ensemblIdA'] = ''
        #ensembl id B
        idB = re.search("ensembl:([^\|]*)\|*", row['ensemblIdB'])
        if (idB != None):
            row['ensemblIdB'] = idB.group(1)
        else:
            row['ensemblIdB'] = ''
        #ordering
        if (row['ensemblIdA'] > row['ensemblIdB']):
            idA = row['ensemblIdA']
            idB = row['ensemblIdB']
            row['ensemblIdA'] = idB
            row['ensemblIdB'] = idA

    # grouping tuples
    innatedb['detectionMethod'] = innatedb.groupby(['ensemblIdA', 'ensemblIdB'])['detectionMethod'].transform(
        lambda x: '|'.join(x))
    innatedb['author'] = innatedb.groupby(['ensemblIdA', 'ensemblIdB'])['author'].transform(
        lambda x: '|'.join(x))
    innatedb['pubmedId'] = innatedb.groupby(['ensemblIdA', 'ensemblIdB'])['pubmedId'].transform(
        lambda x: '|'.join(x))
    innatedb['interactionType'] = innatedb.groupby(['ensemblIdA', 'ensemblIdB'])['interactionType'].transform(
        lambda x: '|'.join(x))
    innatedb = innatedb.drop_duplicates()

    #standardizing columns
    for index, row in innatedb.iterrows():

        #detection method
        det = re.findall("\([^\)]*\)", row['detectionMethod'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            el1 = el.replace("(", "")
            el2 = el1.replace(")", "")
            detect += el2 + "|"
        detect = detect[:-1]
        row['detectionMethod'] = detect

        #pubmed id
        id = re.split("\|", row['pubmedId'])
        id = list(dict.fromkeys(id))
        elem = ''
        for el in id:
            el1 = el.replace("pubmed:", "")
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
        det = re.findall("\([^\)]*\)", row['interactionType'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            el1 = el.replace("(", "")
            el2 = el1.replace(")", "")
            detect += el2 + "|"
        detect = detect[:-1]
        row['interactionType'] = detect

    #deleting useless rows
    for index, row in innatedb.iterrows():

        # ensembl id A
        if (row['ensemblIdA'] == ''):
            innatedb.drop(index, inplace=True)

        # ensembl id B
        elif (row['ensemblIdB'] == ''):
            innatedb.drop(index, inplace=True)

        # ensembl ids identical
        elif (row['ensemblIdA'] == row['ensemblIdB']):
            innatedb.drop(index, inplace=True)

        # taxid A
        elif (not re.match("taxid:9606\(Human\)", row['taxidA'])):
            innatedb.drop(index, inplace=True)

        # taxid B
        elif (not re.match("taxid:9606\(Human\)", row['taxidB'])):
            innatedb.drop(index, inplace=True)

    innatedb = innatedb.drop_duplicates()

    # adding useful columns
    p = Path('Datasets/mapping/uniprot-entrez-ensembl-hgnc.xlsx')
    mapping = pd.read_excel(p, dtype={'entrezgeneid': str})
    result1 = pd.merge(innatedb, mapping, left_on='ensemblIdA', right_on='ensemblid', how='left')
    result1.drop('ensemblid', axis=1, inplace=True)
    result1.rename(columns={'entrezgeneid': 'entrezGeneIdA', 'uniprotid': 'uniprotIdA',
                            'hgncsymbol': 'hgncSymbolA'}, inplace=True)
    result = pd.merge(result1, mapping, left_on='ensemblIdB', right_on='ensemblid', how='left')
    result.drop('ensemblid', axis=1, inplace=True)
    result.rename(columns={'entrezgeneid': 'entrezGeneIdB', 'uniprotid': 'uniprotIdB',
                           'hgncsymbol': 'hgncSymbolB'}, inplace=True)

    # output
    p = Path('DatasetsFormatted/gene/innatedb.csv')
    result.to_csv(p, index=False, columns=['uniprotIdA', 'uniprotIdB','entrezGeneIdA', 'entrezGeneIdB',
                                           'ensemblIdA', 'ensemblIdB','hgncSymbolA', 'hgncSymbolB',
                                           'detectionMethod', 'interactionType','pubmedId', 'author'])

