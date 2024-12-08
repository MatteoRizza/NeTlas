import pandas as pd
import re
from tqdm import tqdm
from pathlib import Path
from neo4j import GraphDatabase
import vars

def writeDiseases():

    #sources
    p = Path('DatasetsFormatted/disease/biosnapDiseases.csv')
    biosnap = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIds': str})
    p = Path('DatasetsFormatted/disease/disgenetDiseases.csv')
    disgenet = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIds': str})
    p = Path('DatasetsFormatted/disease/diseases.csv')
    diseases = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIds': str})

    #connect to db
    driver = GraphDatabase.driver(vars.serverurl, auth=(vars.servername, vars.serverpassword))

    #defining queries
    def init_datasets(tx):
        tx.run("CREATE OR REPLACE DATABASE biosnapDiseases")
        tx.run("CREATE OR REPLACE DATABASE disgenetDiseases")
        tx.run("CREATE OR REPLACE DATABASE diseases")

    def interaction(tx, diseaseId, diseaseName, entrezGeneId):
        tx.run("MERGE (a:Disease {diseaseId: $diseaseId, diseaseName: $diseaseName})"
               "MERGE (g:Gene {entrezGeneId: $entrezGeneId})"
               "MERGE (a)-[i:ACTS_ON]->(g)",
               diseaseId=diseaseId, diseaseName=diseaseName, entrezGeneId=entrezGeneId)

    #writing
    with driver.session() as session:
        session.write_transaction(init_datasets)

    for index, row in tqdm(biosnap.iterrows(), total=biosnap.shape[0]):
        id = re.split("\|", row['entrezGeneIds'])
        for el in id:
            with driver.session(database="biosnapDiseases") as session:
                session.write_transaction(interaction, row['diseaseId'], row['diseaseName'], el)

    for index, row in tqdm(disgenet.iterrows(), total=disgenet.shape[0]):
        id = re.split("\|", row['entrezGeneIds'])
        for el in id:
            with driver.session(database="disgenetDiseases") as session:
                session.write_transaction(interaction, row['diseaseId'], row['diseaseName'], el)

    for index, row in tqdm(diseases.iterrows(), total=diseases.shape[0]):
        id = re.split("\|", row['entrezGeneIds'])
        for el in id:
            with driver.session(database="diseases") as session:
                session.write_transaction(interaction, row['diseaseId'], row['diseaseName'], el)

    #close db
    driver.close()
