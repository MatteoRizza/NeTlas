import pandas as pd
import re
from tqdm import tqdm
from pathlib import Path

def geneAggregation():
    #sources
    numColumns = [0,1,2,3,4,5,6,7,8,9,10]
    p = Path('DatasetsFormatted/gene/biogrid.csv')
    biogrid = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/dip.csv')
    dip = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/matrixdb.csv')
    matrix = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/mint.csv')
    mint = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/innatedb.csv')
    innate = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/intact.csv')
    intact = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})

    #join1
    biogrid['dataSource'] = 'biogrid'
    dip['dataSource'] = 'dip'

    #ordering
    for index, row in biogrid.iterrows():
        if(str(row['uniprotIdA']) > str(row['uniprotIdB'])):
            idA = row['uniprotIdA']
            idB = row['uniprotIdB']
            row['uniprotIdA'] = idB
            row['uniprotIdB'] = idA
            idA = row['entrezGeneIdA']
            idB = row['entrezGeneIdB']
            row['entrezGeneIdA'] = idB
            row['entrezGeneIdB'] = idA
            idA = row['ensemblIdA']
            idB = row['ensemblIdB']
            row['ensemblIdA'] = idB
            row['ensemblIdB'] = idA
            idA = row['hgncSymbolA']
            idB = row['hgncSymbolB']
            row['hgncSymbolA'] = idB
            row['hgncSymbolB'] = idA

    result1 = pd.merge(biogrid, dip, on=['uniprotIdA', 'uniprotIdB',
                                         'entrezGeneIdA', 'entrezGeneIdB',
                                         'ensemblIdA', 'ensemblIdB',
                                         'hgncSymbolA', 'hgncSymbolB'], how='outer')

    #merging other data
    result1['detectionMethod'] = 'AAA'
    result1['interactionType'] = 'AAA'
    result1['pubmedId'] = 'AAA'
    result1['dataSource'] = 'AAA'

    for index, row in tqdm(result1.iterrows(), total=result1.shape[0]):

        # detection method
        if(pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = ''
        elif (pd.isnull(row['detectionMethod_x']) and not pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_y']
        elif (not pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_x']
        else:
            row['detectionMethod'] = row['detectionMethod_x'] + "|" + row['detectionMethod_y']
        det = re.split("\|", row['detectionMethod'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['detectionMethod'] = detect

        # interaction type
        if (pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = ''
        elif (pd.isnull(row['interactionType_x']) and not pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_y']
        elif (not pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_x']
        else:
            row['interactionType'] = row['interactionType_x'] + "|" + row['interactionType_y']
        det = re.split("\|", row['interactionType'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['interactionType'] = detect

        # pubmed id
        if (pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = ''
        elif (pd.isnull(row['pubmedId_x']) and not pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_y']
        elif (not pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_x']
        else:
            row['pubmedId'] = row['pubmedId_x'] + "|" + row['pubmedId_y']
        det = re.split("\|", row['pubmedId'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['pubmedId'] = detect

        # data source
        if (pd.isnull(row['dataSource_x']) and not pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_y']
        elif (not pd.isnull(row['dataSource_x']) and pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_x']
        else:
            row['dataSource'] = row['dataSource_x'] + "|" + row['dataSource_y']

    #deleting useless columns
    result1.drop('detectionMethod_x', axis=1, inplace=True)
    result1.drop('detectionMethod_y', axis=1, inplace=True)
    result1.drop('interactionType_x', axis=1, inplace=True)
    result1.drop('interactionType_y', axis=1, inplace=True)
    result1.drop('pubmedId_x', axis=1, inplace=True)
    result1.drop('pubmedId_y', axis=1, inplace=True)
    result1.drop('dataSource_x', axis=1, inplace=True)
    result1.drop('dataSource_y', axis=1, inplace=True)

    # join2
    matrix['dataSource'] = 'matrixdb'
    result2 = pd.merge(result1, matrix, on=['uniprotIdA', 'uniprotIdB',
                                         'entrezGeneIdA', 'entrezGeneIdB',
                                         'ensemblIdA', 'ensemblIdB',
                                         'hgncSymbolA', 'hgncSymbolB'], how='outer')

    # merging other data
    result2['detectionMethod'] = 'AAA'
    result2['interactionType'] = 'AAA'
    result2['pubmedId'] = 'AAA'
    result2['dataSource'] = 'AAA'
    for index, row in tqdm(result2.iterrows(), total=result2.shape[0]):

        # detection method
        if (pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = ''
        elif (pd.isnull(row['detectionMethod_x']) and not pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_y']
        elif (not pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_x']
        else:
            row['detectionMethod'] = row['detectionMethod_x'] + "|" + row['detectionMethod_y']
        det = re.split("\|", row['detectionMethod'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['detectionMethod'] = detect

        # interaction type
        if (pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = ''
        elif (pd.isnull(row['interactionType_x']) and not pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_y']
        elif (not pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_x']
        else:
            row['interactionType'] = row['interactionType_x'] + "|" + row['interactionType_y']
        det = re.split("\|", row['interactionType'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['interactionType'] = detect

        # pubmed id
        if (pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = ''
        elif (pd.isnull(row['pubmedId_x']) and not pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_y']
        elif (not pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_x']
        else:
            row['pubmedId'] = row['pubmedId_x'] + "|" + row['pubmedId_y']
        det = re.split("\|", row['pubmedId'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['pubmedId'] = detect

        # data source
        if (pd.isnull(row['dataSource_x']) and not pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_y']
        elif (not pd.isnull(row['dataSource_x']) and pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_x']
        else:
            row['dataSource'] = row['dataSource_x'] + "|" + row['dataSource_y']

    # deleting useless columns
    result2.drop('detectionMethod_x', axis=1, inplace=True)
    result2.drop('detectionMethod_y', axis=1, inplace=True)
    result2.drop('interactionType_x', axis=1, inplace=True)
    result2.drop('interactionType_y', axis=1, inplace=True)
    result2.drop('pubmedId_x', axis=1, inplace=True)
    result2.drop('pubmedId_y', axis=1, inplace=True)
    result2.drop('dataSource_x', axis=1, inplace=True)
    result2.drop('dataSource_y', axis=1, inplace=True)

    # join3
    mint['dataSource'] = 'mint'
    result3 = pd.merge(result2, mint, on=['uniprotIdA', 'uniprotIdB',
                                            'entrezGeneIdA', 'entrezGeneIdB',
                                            'ensemblIdA', 'ensemblIdB',
                                            'hgncSymbolA', 'hgncSymbolB'], how='outer')

    # merging other data
    result3['detectionMethod'] = 'AAA'
    result3['interactionType'] = 'AAA'
    result3['pubmedId'] = 'AAA'
    result3['dataSource'] = 'AAA'
    for index, row in tqdm(result3.iterrows(), total=result3.shape[0]):

        # detection method
        if (pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = ''
        elif (pd.isnull(row['detectionMethod_x']) and not pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_y']
        elif (not pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_x']
        else:
            row['detectionMethod'] = row['detectionMethod_x'] + "|" + row['detectionMethod_y']
        det = re.split("\|", row['detectionMethod'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['detectionMethod'] = detect

        # interaction type
        if (pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = ''
        elif (pd.isnull(row['interactionType_x']) and not pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_y']
        elif (not pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_x']
        else:
            row['interactionType'] = row['interactionType_x'] + "|" + row['interactionType_y']
        det = re.split("\|", row['interactionType'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['interactionType'] = detect

        # pubmed id
        if (pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = ''
        elif (pd.isnull(row['pubmedId_x']) and not pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_y']
        elif (not pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_x']
        else:
            row['pubmedId'] = row['pubmedId_x'] + "|" + row['pubmedId_y']
        det = re.split("\|", row['pubmedId'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['pubmedId'] = detect

        # data source
        if (pd.isnull(row['dataSource_x']) and not pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_y']
        elif (not pd.isnull(row['dataSource_x']) and pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_x']
        else:
            row['dataSource'] = row['dataSource_x'] + "|" + row['dataSource_y']

    # deleting useless columns
    result3.drop('detectionMethod_x', axis=1, inplace=True)
    result3.drop('detectionMethod_y', axis=1, inplace=True)
    result3.drop('interactionType_x', axis=1, inplace=True)
    result3.drop('interactionType_y', axis=1, inplace=True)
    result3.drop('pubmedId_x', axis=1, inplace=True)
    result3.drop('pubmedId_y', axis=1, inplace=True)
    result3.drop('dataSource_x', axis=1, inplace=True)
    result3.drop('dataSource_y', axis=1, inplace=True)

    # join4
    innate['dataSource'] = 'innatedb'

    #ordering
    for index, row in innate.iterrows():
        if(str(row['uniprotIdA']) > str(row['uniprotIdB'])):
            idA = row['uniprotIdA']
            idB = row['uniprotIdB']
            row['uniprotIdA'] = idB
            row['uniprotIdB'] = idA
            idA = row['entrezGeneIdA']
            idB = row['entrezGeneIdB']
            row['entrezGeneIdA'] = idB
            row['entrezGeneIdB'] = idA
            idA = row['ensemblIdA']
            idB = row['ensemblIdB']
            row['ensemblIdA'] = idB
            row['ensemblIdB'] = idA
            idA = row['hgncSymbolA']
            idB = row['hgncSymbolB']
            row['hgncSymbolA'] = idB
            row['hgncSymbolB'] = idA

    result4 = pd.merge(result3, innate, on=['uniprotIdA', 'uniprotIdB',
                                            'entrezGeneIdA', 'entrezGeneIdB',
                                            'ensemblIdA', 'ensemblIdB',
                                            'hgncSymbolA', 'hgncSymbolB'], how='outer')

    # merging other data
    result4['detectionMethod'] = 'AAA'
    result4['interactionType'] = 'AAA'
    result4['pubmedId'] = 'AAA'
    result4['dataSource'] = 'AAA'
    for index, row in tqdm(result4.iterrows(), total=result4.shape[0]):

        # detection method
        if (pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = ''
        elif (pd.isnull(row['detectionMethod_x']) and not pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_y']
        elif (not pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_x']
        else:
            row['detectionMethod'] = row['detectionMethod_x'] + "|" + row['detectionMethod_y']
        det = re.split("\|", row['detectionMethod'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['detectionMethod'] = detect

        # interaction type
        if (pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = ''
        elif (pd.isnull(row['interactionType_x']) and not pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_y']
        elif (not pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_x']
        else:
            row['interactionType'] = row['interactionType_x'] + "|" + row['interactionType_y']
        det = re.split("\|", row['interactionType'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['interactionType'] = detect

        # pubmed id
        if (pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = ''
        elif (pd.isnull(row['pubmedId_x']) and not pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_y']
        elif (not pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_x']
        else:
            row['pubmedId'] = row['pubmedId_x'] + "|" + row['pubmedId_y']
        det = re.split("\|", row['pubmedId'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['pubmedId'] = detect

        # data source
        if (pd.isnull(row['dataSource_x']) and not pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_y']
        elif (not pd.isnull(row['dataSource_x']) and pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_x']
        else:
            row['dataSource'] = row['dataSource_x'] + "|" + row['dataSource_y']

    # deleting useless columns
    result4.drop('detectionMethod_x', axis=1, inplace=True)
    result4.drop('detectionMethod_y', axis=1, inplace=True)
    result4.drop('interactionType_x', axis=1, inplace=True)
    result4.drop('interactionType_y', axis=1, inplace=True)
    result4.drop('pubmedId_x', axis=1, inplace=True)
    result4.drop('pubmedId_y', axis=1, inplace=True)
    result4.drop('dataSource_x', axis=1, inplace=True)
    result4.drop('dataSource_y', axis=1, inplace=True)

    # final join
    intact['dataSource'] = 'intact'
    result = pd.merge(result4, intact, on=['uniprotIdA', 'uniprotIdB',
                                           'entrezGeneIdA', 'entrezGeneIdB',
                                           'ensemblIdA', 'ensemblIdB',
                                           'hgncSymbolA', 'hgncSymbolB'], how='outer')

    # merging other data
    result['detectionMethod'] = 'AAA'
    result['interactionType'] = 'AAA'
    result['pubmedId'] = 'AAA'
    result['dataSource'] = 'AAA'
    for index, row in tqdm(result.iterrows(), total=result.shape[0]):

        # detection method
        if (pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = ''
        elif (pd.isnull(row['detectionMethod_x']) and not pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_y']
        elif (not pd.isnull(row['detectionMethod_x']) and pd.isnull(row['detectionMethod_y'])):
            row['detectionMethod'] = row['detectionMethod_x']
        else:
            row['detectionMethod'] = row['detectionMethod_x'] + "|" + row['detectionMethod_y']
        det = re.split("\|", row['detectionMethod'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['detectionMethod'] = detect

        # interaction type
        if (pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = ''
        elif (pd.isnull(row['interactionType_x']) and not pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_y']
        elif (not pd.isnull(row['interactionType_x']) and pd.isnull(row['interactionType_y'])):
            row['interactionType'] = row['interactionType_x']
        else:
            row['interactionType'] = row['interactionType_x'] + "|" + row['interactionType_y']
        det = re.split("\|", row['interactionType'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['interactionType'] = detect

        # pubmed id
        if (pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = ''
        elif (pd.isnull(row['pubmedId_x']) and not pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_y']
        elif (not pd.isnull(row['pubmedId_x']) and pd.isnull(row['pubmedId_y'])):
            row['pubmedId'] = row['pubmedId_x']
        else:
            row['pubmedId'] = row['pubmedId_x'] + "|" + row['pubmedId_y']
        det = re.split("\|", row['pubmedId'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['pubmedId'] = detect

        # data source
        if (pd.isnull(row['dataSource_x']) and not pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_y']
        elif (not pd.isnull(row['dataSource_x']) and pd.isnull(row['dataSource_y'])):
            row['dataSource'] = row['dataSource_x']
        else:
            row['dataSource'] = row['dataSource_x'] + "|" + row['dataSource_y']

    # deleting useless columns
    result.drop('detectionMethod_x', axis=1, inplace=True)
    result.drop('detectionMethod_y', axis=1, inplace=True)
    result.drop('interactionType_x', axis=1, inplace=True)
    result.drop('interactionType_y', axis=1, inplace=True)
    result.drop('pubmedId_x', axis=1, inplace=True)
    result.drop('pubmedId_y', axis=1, inplace=True)
    result.drop('dataSource_x', axis=1, inplace=True)
    result.drop('dataSource_y', axis=1, inplace=True)

    # output
    p = Path('DatasetsFormatted/gene/genes.csv')
    result.to_csv(p, index=False, columns=['uniprotIdA', 'uniprotIdB', 'entrezGeneIdA', 'entrezGeneIdB',
                                           'ensemblIdA', 'ensemblIdB', 'hgncSymbolA', 'hgncSymbolB',
                                           'detectionMethod', 'interactionType', 'pubmedId', 'dataSource'])