import pandas as pd
import re
from tqdm import tqdm
from pathlib import Path

def diseaseAggregation():
    #sources
    numColumns = [0, 1, 2]
    p = Path('DatasetsFormatted/disease/biosnapDiseases.csv')
    biosnap = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIds':str})
    p = Path('DatasetsFormatted/disease/disgenetDiseases.csv')
    disgenet = pd.read_csv(p, header=0, index_col=False, usecols=numColumns, dtype={'entrezGeneIds':str})

    #join
    result = pd.merge(biosnap, disgenet, on=['diseaseId'], how='outer')

    #merging other data
    result['diseaseName'] = 'AAA'
    result['entrezGeneIds'] = 'AAA'
    for index, row in tqdm(result.iterrows(), total=result.shape[0]):

        # disease name
        if(pd.isnull(row['diseaseName_x']) and pd.isnull(row['diseaseName_y'])):
            row['diseaseName'] = ''
        elif (not pd.isnull(row['diseaseName_x']) and pd.isnull(row['diseaseName_y'])):
            row['diseaseName'] = row['diseaseName_x']
        else:
            row['diseaseName'] = row['diseaseName_y']
        det = re.split("\|", row['diseaseName'])
        det = list(dict.fromkeys(det))
        detect = ''
        for el in det:
            detect += el + "|"
        detect = detect[:-1]
        row['diseaseName'] = detect

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
    p = Path('DatasetsFormatted/disease/diseases.csv')
    result.to_csv(p, index=False, columns=['diseaseId', 'diseaseName', 'entrezGeneIds'])