import pandas as pd
from pathlib import Path
import re

pd.set_option('display.max_columns', None)

def parsingDip():
    #source file
    dipColumns = ['uniprotIdA','uniprotIdB','useless1','useless2','useless3','useless4','detectionMethod',
                  'useless5','pubmedId','taxidA','taxidB','interactionType','useless6','useless7','useless8','throughput']
    numColumns = [0,1,6,8,9,10,11,15]
    p = Path('Datasets/gene/dip.txt')
    dip = pd.read_csv(p, sep='\t', header=0, names=dipColumns, usecols=numColumns, index_col=False )

    #standardizing columns
    for index, row in dip.iterrows():

        # uniprot id A
        idA = re.search("uniprotkb:([^\|]*)\|*", row['uniprotIdA'])
        if (idA != None):
            row['uniprotIdA'] = idA.group(1)
        else:
            row['uniprotIdA'] = ''
        # uniprot id B
        idB = re.search("uniprotkb:([^\|]*)\|*", row['uniprotIdB'])
        if (idB != None):
            row['uniprotIdB'] = idB.group(1)
        else:
            row['uniprotIdB'] = ''
        # ordering
        if (row['uniprotIdA'] > row['uniprotIdB']):
            idA = row['uniprotIdA']
            idB = row['uniprotIdB']
            row['uniprotIdA'] = idB
            row['uniprotIdB'] = idA

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
        for el in id:
            if(re.match(".*DIP.*", el) or re.match(".*rtd.*", el)):
                id.remove(el)
        elem = ''
        for el in id:
            el1 = el.replace("pubmed:", "")
            elem += el1 + "|"
        elem = elem[:-1]
        row['pubmedId'] = elem

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

        #throughput
        det = re.findall("\([^\)]*\)", row['throughput'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            el1 = el.replace("(", "")
            el2 = el1.replace(")", "")
            detect += el2 + "|"
        detect = detect[:-1]
        row['throughput'] = detect

    #deleting useless rows
    for index, row in dip.iterrows():

        # uniprot id A
        if (row['uniprotIdA'] == '' or re.match(".*,.*",row['uniprotIdA'])):
            dip.drop(index, inplace=True)

        # uniprot id B
        elif (row['uniprotIdB'] == '' or re.match(".*,.*",row['uniprotIdB'])):
            dip.drop(index, inplace=True)

        # uniprot ids identical
        elif (row['uniprotIdA'] == row['uniprotIdB']):
            dip.drop(index, inplace=True)

        # taxid A
        elif (not re.match("taxid:9606\(Homo sapiens\)", row['taxidA'])):
            dip.drop(index, inplace=True)

        # taxid B
        elif (not re.match("taxid:9606\(Homo sapiens\)", row['taxidB'])):
            dip.drop(index, inplace=True)

    dip = dip.drop_duplicates()

    #adding useful columns
    p = Path('Datasets/mapping/uniprot-entrez-ensembl-hgnc.xlsx')
    mapping = pd.read_excel(p, dtype={'entrezgeneid':str})
    result1 = pd.merge(dip,mapping,left_on='uniprotIdA',right_on='uniprotid',how='left')
    result1.drop('uniprotid', axis=1, inplace=True)
    result1.rename(columns={'entrezgeneid': 'entrezGeneIdA', 'ensemblid': 'ensemblIdA' ,
                            'hgncsymbol': 'hgncSymbolA'}, inplace=True)
    result = pd.merge(result1,mapping,left_on='uniprotIdB',right_on='uniprotid',how='left')
    result.drop('uniprotid', axis=1, inplace=True)
    result.rename(columns={'entrezgeneid': 'entrezGeneIdB', 'ensemblid': 'ensemblIdB',
                           'hgncsymbol': 'hgncSymbolB'}, inplace=True)

    #output
    p = Path('DatasetsFormatted/gene/dip.csv')
    result.to_csv(p, index=False, columns=['uniprotIdA','uniprotIdB','entrezGeneIdA','entrezGeneIdB',
                                           'ensemblIdA','ensemblIdB','hgncSymbolA','hgncSymbolB',
                                           'detectionMethod','interactionType','pubmedId','throughput'])

