import pandas as pd
from tqdm import tqdm
from pathlib import Path
from neo4j import GraphDatabase
import vars

#Move dbs from csv to Neo4j format
def writeGenes():

    #sources
    p = Path('DatasetsFormatted/gene/biogrid.csv')
    biogrid = pd.read_csv(p, header=0, index_col=False,dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})
    p = Path('DatasetsFormatted/gene/dip.csv')
    dip = pd.read_csv(p, header=0, index_col=False, dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})
    p = Path('DatasetsFormatted/gene/matrixdb.csv')
    matrix = pd.read_csv(p, header=0, index_col=False,dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})
    p = Path('DatasetsFormatted/gene/mint.csv')
    mint = pd.read_csv(p, header=0, index_col=False,dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})
    p = Path('DatasetsFormatted/gene/innatedb.csv')
    innate = pd.read_csv(p, header=0, index_col=False,dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})
    p = Path('DatasetsFormatted/gene/intact.csv')
    intact = pd.read_csv(p, header=0, index_col=False,dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})
    p = Path('DatasetsFormatted/gene/genes.csv')
    genes = pd.read_csv(p, header=0, index_col=False,dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})

    #connect to db
    driver = GraphDatabase.driver(vars.serverurl, auth=(vars.servername, vars.serverpassword))

    #defining queries
    def init_datasets(tx):
        tx.run("CREATE OR REPLACE DATABASE biogrid")
        tx.run("CREATE OR REPLACE DATABASE dip")
        tx.run("CREATE OR REPLACE DATABASE matrixdb")
        tx.run("CREATE OR REPLACE DATABASE mint")
        tx.run("CREATE OR REPLACE DATABASE innatedb")
        tx.run("CREATE OR REPLACE DATABASE intact")
        tx.run("CREATE OR REPLACE DATABASE genes")

    def interaction1(tx, uniprotIdA, entrezGeneIdA, ensemblIdA, hgncSymbolA,
                        uniprotIdB, entrezGeneIdB, ensemblIdB, hgncSymbolB,
                        detectionMethod, interactionType, pubmedId, author, throughput, reliabilityScore):
        tx.run("MERGE (a:Gene {uniprotId: $uniprotIdA, entrezGeneId: $entrezGeneIdA,"
               "ensemblId: $ensemblIdA, hgncSymbol: $hgncSymbolA})"
               "MERGE (b:Gene {uniprotId: $uniprotIdB, entrezGeneId: $entrezGeneIdB,"
               "ensemblId: $ensemblIdB, hgncSymbol: $hgncSymbolB})" 
               "MERGE (a)-[i:INTERACTION {detectionMethod: $detectionMethod, interactionType: $interactionType,"
               "pubmedId: $pubmedId, author: $author, throughput: $throughput, reliabilityScore: $reliabilityScore}]->(b)",
               uniprotIdA=uniprotIdA, entrezGeneIdA=entrezGeneIdA, ensemblIdA=ensemblIdA, hgncSymbolA=hgncSymbolA,
               uniprotIdB=uniprotIdB, entrezGeneIdB=entrezGeneIdB, ensemblIdB=ensemblIdB, hgncSymbolB=hgncSymbolB,
               detectionMethod=detectionMethod, interactionType=interactionType, pubmedId=pubmedId,
               author=author, throughput=throughput, reliabilityScore=reliabilityScore)

    def interaction2(tx, uniprotIdA, entrezGeneIdA, ensemblIdA, hgncSymbolA,
                        uniprotIdB, entrezGeneIdB, ensemblIdB, hgncSymbolB,
                        detectionMethod, interactionType, pubmedId, throughput, reliabilityScore):
        tx.run("MERGE (a:Gene {uniprotId: $uniprotIdA, entrezGeneId: $entrezGeneIdA,"
               "ensemblId: $ensemblIdA, hgncSymbol: $hgncSymbolA})"
               "MERGE (b:Gene {uniprotId: $uniprotIdB, entrezGeneId: $entrezGeneIdB,"
               "ensemblId: $ensemblIdB, hgncSymbol: $hgncSymbolB})" 
               "MERGE (a)-[i:INTERACTION {detectionMethod: $detectionMethod, interactionType: $interactionType,"
               "pubmedId: $pubmedId, throughput: $throughput, reliabilityScore: $reliabilityScore}]->(b)",
               uniprotIdA=uniprotIdA, entrezGeneIdA=entrezGeneIdA, ensemblIdA=ensemblIdA, hgncSymbolA=hgncSymbolA,
               uniprotIdB=uniprotIdB, entrezGeneIdB=entrezGeneIdB, ensemblIdB=ensemblIdB, hgncSymbolB=hgncSymbolB,
               detectionMethod=detectionMethod, interactionType=interactionType, pubmedId=pubmedId,
               throughput=throughput, reliabilityScore=reliabilityScore)

    def interaction3(tx, uniprotIdA, entrezGeneIdA, ensemblIdA, hgncSymbolA,
                     uniprotIdB, entrezGeneIdB, ensemblIdB, hgncSymbolB,
                     detectionMethod, interactionType, pubmedId, author, reliabilityScore):
        tx.run("MERGE (a:Gene {uniprotId: $uniprotIdA, entrezGeneId: $entrezGeneIdA,"
               "ensemblId: $ensemblIdA, hgncSymbol: $hgncSymbolA})"
               "MERGE (b:Gene {uniprotId: $uniprotIdB, entrezGeneId: $entrezGeneIdB,"
               "ensemblId: $ensemblIdB, hgncSymbol: $hgncSymbolB})"
               "MERGE (a)-[i:INTERACTION {detectionMethod: $detectionMethod, interactionType: $interactionType,"
               "pubmedId: $pubmedId, author: $author, reliabilityScore: $reliabilityScore}]->(b)",
               uniprotIdA=uniprotIdA, entrezGeneIdA=entrezGeneIdA, ensemblIdA=ensemblIdA, hgncSymbolA=hgncSymbolA,
               uniprotIdB=uniprotIdB, entrezGeneIdB=entrezGeneIdB, ensemblIdB=ensemblIdB, hgncSymbolB=hgncSymbolB,
               detectionMethod=detectionMethod, interactionType=interactionType, pubmedId=pubmedId,
               author=author, reliabilityScore=reliabilityScore)

    def interaction4(tx, uniprotIdA, entrezGeneIdA, ensemblIdA, hgncSymbolA,
                     uniprotIdB, entrezGeneIdB, ensemblIdB, hgncSymbolB,
                     detectionMethod, interactionType, pubmedId, dataSource, reliabilityScore):
        tx.run("MERGE (a:Gene {uniprotId: $uniprotIdA, entrezGeneId: $entrezGeneIdA,"
               "ensemblId: $ensemblIdA, hgncSymbol: $hgncSymbolA})"
               "MERGE (b:Gene {uniprotId: $uniprotIdB, entrezGeneId: $entrezGeneIdB,"
               "ensemblId: $ensemblIdB, hgncSymbol: $hgncSymbolB})"
               "MERGE (a)-[i:INTERACTION {detectionMethod: $detectionMethod, interactionType: $interactionType,"
               "pubmedId: $pubmedId, dataSource: $dataSource, reliabilityScore: $reliabilityScore}]->(b)",
               uniprotIdA=uniprotIdA, entrezGeneIdA=entrezGeneIdA, ensemblIdA=ensemblIdA, hgncSymbolA=hgncSymbolA,
               uniprotIdB=uniprotIdB, entrezGeneIdB=entrezGeneIdB, ensemblIdB=ensemblIdB, hgncSymbolB=hgncSymbolB,
               detectionMethod=detectionMethod, interactionType=interactionType, pubmedId=pubmedId,
               dataSource=dataSource, reliabilityScore=reliabilityScore)

    #writing
    with driver.session() as session:
        session.write_transaction(init_datasets)

    for index, row in tqdm(biogrid.iterrows(), total=biogrid.shape[0]):
        if(pd.isnull(row['uniprotIdA'])):
            row['uniprotIdA'] = '-'
        if(pd.isnull(row['uniprotIdB'])):
            row['uniprotIdB'] = '-'
        if (pd.isnull(row['entrezGeneIdA'])):
            row['entrezGeneIdA'] = '-'
        if (pd.isnull(row['entrezGeneIdB'])):
            row['entrezGeneIdB'] = '-'
        if (pd.isnull(row['ensemblIdA'])):
            row['ensemblIdA'] = '-'
        if (pd.isnull(row['ensemblIdB'])):
            row['ensemblIdB'] = '-'
        if (pd.isnull(row['hgncSymbolA'])):
            row['hgncSymbolA'] = '-'
        if (pd.isnull(row['hgncSymbolB'])):
            row['hgncSymbolB'] = '-'
        with driver.session(database="biogrid") as session:
            session.write_transaction(interaction1, row['uniprotIdA'], row['entrezGeneIdA'], row['ensemblIdA'],
                                      row['hgncSymbolA'], row['uniprotIdB'], row['entrezGeneIdB'], row['ensemblIdB'],
                                      row['hgncSymbolB'], row['detectionMethod'], row['interactionType'],
                                      row['pubmedId'], row['author'], row['throughput'], row['reliabilityScore'])

    for index, row in tqdm(dip.iterrows(), total=dip.shape[0]):
        if(pd.isnull(row['uniprotIdA'])):
            row['uniprotIdA'] = '-'
        if(pd.isnull(row['uniprotIdB'])):
            row['uniprotIdB'] = '-'
        if (pd.isnull(row['entrezGeneIdA'])):
            row['entrezGeneIdA'] = '-'
        if (pd.isnull(row['entrezGeneIdB'])):
            row['entrezGeneIdB'] = '-'
        if (pd.isnull(row['ensemblIdA'])):
            row['ensemblIdA'] = '-'
        if (pd.isnull(row['ensemblIdB'])):
            row['ensemblIdB'] = '-'
        if (pd.isnull(row['hgncSymbolA'])):
            row['hgncSymbolA'] = '-'
        if (pd.isnull(row['hgncSymbolB'])):
            row['hgncSymbolB'] = '-'
        with driver.session(database="dip") as session:
            session.write_transaction(interaction2, row['uniprotIdA'], row['entrezGeneIdA'], row['ensemblIdA'],
                                      row['hgncSymbolA'], row['uniprotIdB'], row['entrezGeneIdB'], row['ensemblIdB'],
                                      row['hgncSymbolB'], row['detectionMethod'], row['interactionType'],
                                      row['pubmedId'], row['throughput'], row['reliabilityScore'])

    for index, row in tqdm(matrix.iterrows(), total=matrix.shape[0]):
        if(pd.isnull(row['uniprotIdA'])):
            row['uniprotIdA'] = '-'
        if(pd.isnull(row['uniprotIdB'])):
            row['uniprotIdB'] = '-'
        if (pd.isnull(row['entrezGeneIdA'])):
            row['entrezGeneIdA'] = '-'
        if (pd.isnull(row['entrezGeneIdB'])):
            row['entrezGeneIdB'] = '-'
        if (pd.isnull(row['ensemblIdA'])):
            row['ensemblIdA'] = '-'
        if (pd.isnull(row['ensemblIdB'])):
            row['ensemblIdB'] = '-'
        if (pd.isnull(row['hgncSymbolA'])):
            row['hgncSymbolA'] = '-'
        if (pd.isnull(row['hgncSymbolB'])):
            row['hgncSymbolB'] = '-'
        with driver.session(database="matrixdb") as session:
            session.write_transaction(interaction3, row['uniprotIdA'], row['entrezGeneIdA'], row['ensemblIdA'],
                                      row['hgncSymbolA'], row['uniprotIdB'], row['entrezGeneIdB'], row['ensemblIdB'],
                                      row['hgncSymbolB'], row['detectionMethod'], row['interactionType'],
                                      row['pubmedId'], row['author'], row['reliabilityScore'])

    for index, row in tqdm(mint.iterrows(), total=mint.shape[0]):
        if(pd.isnull(row['uniprotIdA'])):
            row['uniprotIdA'] = '-'
        if(pd.isnull(row['uniprotIdB'])):
            row['uniprotIdB'] = '-'
        if (pd.isnull(row['entrezGeneIdA'])):
            row['entrezGeneIdA'] = '-'
        if (pd.isnull(row['entrezGeneIdB'])):
            row['entrezGeneIdB'] = '-'
        if (pd.isnull(row['ensemblIdA'])):
            row['ensemblIdA'] = '-'
        if (pd.isnull(row['ensemblIdB'])):
            row['ensemblIdB'] = '-'
        if (pd.isnull(row['hgncSymbolA'])):
            row['hgncSymbolA'] = '-'
        if (pd.isnull(row['hgncSymbolB'])):
            row['hgncSymbolB'] = '-'
        with driver.session(database="mint") as session:
            session.write_transaction(interaction3, row['uniprotIdA'], row['entrezGeneIdA'], row['ensemblIdA'],
                                      row['hgncSymbolA'], row['uniprotIdB'], row['entrezGeneIdB'], row['ensemblIdB'],
                                      row['hgncSymbolB'], row['detectionMethod'], row['interactionType'],
                                      row['pubmedId'], row['author'], row['reliabilityScore'])

    for index, row in tqdm(innate.iterrows(), total=innate.shape[0]):
        if(pd.isnull(row['uniprotIdA'])):
            row['uniprotIdA'] = '-'
        if(pd.isnull(row['uniprotIdB'])):
            row['uniprotIdB'] = '-'
        if (pd.isnull(row['entrezGeneIdA'])):
            row['entrezGeneIdA'] = '-'
        if (pd.isnull(row['entrezGeneIdB'])):
            row['entrezGeneIdB'] = '-'
        if (pd.isnull(row['ensemblIdA'])):
            row['ensemblIdA'] = '-'
        if (pd.isnull(row['ensemblIdB'])):
            row['ensemblIdB'] = '-'
        if (pd.isnull(row['hgncSymbolA'])):
            row['hgncSymbolA'] = '-'
        if (pd.isnull(row['hgncSymbolB'])):
            row['hgncSymbolB'] = '-'
        with driver.session(database="innatedb") as session:
            session.write_transaction(interaction3, row['uniprotIdA'], row['entrezGeneIdA'], row['ensemblIdA'],
                                      row['hgncSymbolA'], row['uniprotIdB'], row['entrezGeneIdB'], row['ensemblIdB'],
                                      row['hgncSymbolB'], row['detectionMethod'], row['interactionType'],
                                      row['pubmedId'], row['author'], row['reliabilityScore'])

    for index, row in tqdm(intact.iterrows(), total=intact.shape[0]):
        if(pd.isnull(row['uniprotIdA'])):
            row['uniprotIdA'] = '-'
        if(pd.isnull(row['uniprotIdB'])):
            row['uniprotIdB'] = '-'
        if (pd.isnull(row['entrezGeneIdA'])):
            row['entrezGeneIdA'] = '-'
        if (pd.isnull(row['entrezGeneIdB'])):
            row['entrezGeneIdB'] = '-'
        if (pd.isnull(row['ensemblIdA'])):
            row['ensemblIdA'] = '-'
        if (pd.isnull(row['ensemblIdB'])):
            row['ensemblIdB'] = '-'
        if (pd.isnull(row['hgncSymbolA'])):
            row['hgncSymbolA'] = '-'
        if (pd.isnull(row['hgncSymbolB'])):
            row['hgncSymbolB'] = '-'
        with driver.session(database="intact") as session:
            session.write_transaction(interaction3, row['uniprotIdA'], row['entrezGeneIdA'], row['ensemblIdA'],
                                      row['hgncSymbolA'], row['uniprotIdB'], row['entrezGeneIdB'], row['ensemblIdB'],
                                      row['hgncSymbolB'], row['detectionMethod'], row['interactionType'],
                                      row['pubmedId'], row['author'], row['reliabilityScore'])

    for index, row in tqdm(genes.iterrows(), total=genes.shape[0]):
        if(pd.isnull(row['uniprotIdA'])):
            row['uniprotIdA'] = '-'
        if(pd.isnull(row['uniprotIdB'])):
            row['uniprotIdB'] = '-'
        if (pd.isnull(row['entrezGeneIdA'])):
            row['entrezGeneIdA'] = '-'
        if (pd.isnull(row['entrezGeneIdB'])):
            row['entrezGeneIdB'] = '-'
        if (pd.isnull(row['ensemblIdA'])):
            row['ensemblIdA'] = '-'
        if (pd.isnull(row['ensemblIdB'])):
            row['ensemblIdB'] = '-'
        if (pd.isnull(row['hgncSymbolA'])):
            row['hgncSymbolA'] = '-'
        if (pd.isnull(row['hgncSymbolB'])):
            row['hgncSymbolB'] = '-'
        with driver.session(database="genes") as session:
            session.write_transaction(interaction4, row['uniprotIdA'], row['entrezGeneIdA'], row['ensemblIdA'],
                                      row['hgncSymbolA'], row['uniprotIdB'], row['entrezGeneIdB'], row['ensemblIdB'],
                                      row['hgncSymbolB'], row['detectionMethod'], row['interactionType'],
                                      row['pubmedId'], row['dataSource'], row['reliabilityScore'])

    #close db
    driver.close()