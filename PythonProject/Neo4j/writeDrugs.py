import pandas as pd
import re
from tqdm import tqdm
from pathlib import Path
from neo4j import GraphDatabase
import vars

def writeDrugs():

    #sources
    p = Path('DatasetsFormatted/drug/biogridDrugs.csv')
    biogrid = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIds': str, 'pubmedId': str})
    p = Path('DatasetsFormatted/drug/dgiDrugs.csv')
    dgi = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIds': str, 'pubmedId': str})
    p = Path('DatasetsFormatted/drug/drugs.csv')
    drugs = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIds': str, 'pubmedId': str})

    #connect to db
    driver = GraphDatabase.driver(vars.serverurl, auth=(vars.servername, vars.serverpassword))

    #defining queries
    def init_datasets(tx):
        tx.run("CREATE OR REPLACE DATABASE biogridDrugs")
        tx.run("CREATE OR REPLACE DATABASE dgiDrugs")
        tx.run("CREATE OR REPLACE DATABASE drugs")

    def interaction1(tx, drugName, entrezGeneId, pubmedId, author):
        tx.run("MERGE (a:Drug {drugName: $drugName})"
               "MERGE (g:Gene {entrezGeneId: $entrezGeneId})"
               "MERGE (a)-[i:ACTS_ON {pubmedId: $pubmedId, author: $author}]->(g)",
                drugName=drugName, entrezGeneId=entrezGeneId, pubmedId=pubmedId, author=author)

    def interaction2(tx, drugName, entrezGeneId, pubmedId):
        tx.run("MERGE (a:Drug {drugName: $drugName})"
               "MERGE (g:Gene {entrezGeneId: $entrezGeneId})"
               "MERGE (a)-[i:ACTS_ON {pubmedId: $pubmedId}]->(g)",
                drugName=drugName, entrezGeneId=entrezGeneId, pubmedId=pubmedId)

    #writing
    with driver.session() as session:
        session.write_transaction(init_datasets)

    for index, row in tqdm(biogrid.iterrows(), total=biogrid.shape[0]):
        id = re.split("\|", row['entrezGeneIds'])
        for el in id:
            with driver.session(database="biogridDrugs") as session:
                session.write_transaction(interaction1, row['drugName'], el, row['pubmedId'], row['author'])

    for index, row in tqdm(dgi.iterrows(), total=dgi.shape[0]):
        id = re.split("\|", row['entrezGeneIds'])
        for el in id:
            with driver.session(database="dgiDrugs") as session:
                session.write_transaction(interaction2, row['drugName'], el, row['pubmedId'])

    for index, row in tqdm(drugs.iterrows(), total=drugs.shape[0]):
        id = re.split("\|", row['entrezGeneIds'])
        for el in id:
            with driver.session(database="drugs") as session:
                session.write_transaction(interaction2, row['drugName'], el, row['pubmedId'])

    #close db
    driver.close()