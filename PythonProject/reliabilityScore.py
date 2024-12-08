import pandas as pd
import re
import math
from tqdm import tqdm
from pathlib import Path

# Through this function, we assign a reliability score to each tuple of the datasets relating to genes,
# based on 3 data: detention method, interaction type and number of publications
def reliabilityScore():

    #sources
    p = Path('DatasetsFormatted/gene/biogrid.csv')
    biogrid = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/dip.csv')
    dip = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/matrixdb.csv')
    matrix = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/mint.csv')
    mint = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/innatedb.csv')
    innate = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIdA':str, 'entrezGeneIdB':str, 'pubmedId':str})
    p = Path('DatasetsFormatted/gene/intact.csv')
    intact = pd.read_csv(p, header=0, index_col=False,dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})
    p = Path('DatasetsFormatted/gene/genes.csv')
    genes = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})
    p = Path('Datasets/mapping/Experiments.xlsx')
    experiments = pd.read_excel(p)

    #create reliability score columns
    biogrid['reliabilityScore'] = ''
    dip['reliabilityScore'] = ''
    matrix['reliabilityScore'] = ''
    mint['reliabilityScore'] = ''
    innate['reliabilityScore'] = ''
    intact['reliabilityScore'] = ''
    genes['reliabilityScore'] = ''

    #score function
    def scoring(db, nmax):

        for index, row in tqdm(db.iterrows(), total=db.shape[0]):

            # detection method
            score = 0
            det = re.split("\|", row['detectionMethod'])
            for el in det:
                flag = False
                for index, row1 in experiments.iterrows():
                    if (el == row1['Subcategory']):
                        flag = True
                        if (row1['Category'] == 'biophysical'):
                            score += 1
                        elif (row1['Category'] == 'protein complementation assay'):
                            score += 0.66
                        elif (row1['Category'] == 'genetic interference'):
                            score += 0.1
                        elif (row1['Category'] == 'post transcriptional interference'):
                            score += 0.1
                        elif (row1['Category'] == 'biochemical'):
                            score += 1
                        elif (row1['Category'] == 'imaging technique'):
                            score += 0.33
                        break
                if (not flag):
                    score += 0.05
            b = score + 3.21
            detScore = math.log(score + 1, b + 1)

            # pubmed id
            score = 0
            id = re.split("\|", row['pubmedId'])
            score = len(id)
            pubScore = math.log(score + 1, nmax)
            if(pubScore > 1):
                pubScore = 1

            # interaction type
            score = 0
            interact = re.split("\|", row['interactionType'])
            for el in interact:
                if (el == 'genetic interaction'):
                    score += 0.1
                elif (el == 'colocalization'):
                    score += 0.33
                elif (el == 'association'):
                    score += 0.33
                elif (el == 'physical association'):
                    score += 0.66
                elif (el == 'direct interaction'):
                    score += 1
                else:
                    score += 0.05
            b = score + 1.43
            intScore = math.log(score + 1, b + 1)

            # calculate reliability score
            row['reliabilityScore'] = round((0.3 * detScore) + (0.3 * pubScore) + (0.3 * intScore), 2)
            # In this case the three factors are weighted equally (customizable)

        return db

    #scoring datasets
    biogrid = scoring(biogrid, 7)
    dip = scoring(dip, 7)
    matrix = scoring(matrix, 7)
    mint = scoring(mint, 7)
    innate = scoring(innate, 7)
    intact = scoring(intact, 7)
    genes = scoring(genes, 7)

    #output
    p = Path('DatasetsFormatted/gene/biogrid.csv')
    biogrid.to_csv(p, index=False)
    p = Path('DatasetsFormatted/gene/dip.csv')
    dip.to_csv(p, index=False)
    p = Path('DatasetsFormatted/gene/matrixdb.csv')
    matrix.to_csv(p, index=False)
    p = Path('DatasetsFormatted/gene/mint.csv')
    mint.to_csv(p, index=False)
    p = Path('DatasetsFormatted/gene/innatedb.csv')
    innate.to_csv(p, index=False)
    p = Path('DatasetsFormatted/gene/intact.csv')
    intact.to_csv(p, index=False)
    p = Path('DatasetsFormatted/gene/genes.csv')
    genes.to_csv(p, index=False)
