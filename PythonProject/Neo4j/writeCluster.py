import pandas as pd
from tqdm import tqdm
from pathlib import Path
from neo4j import GraphDatabase
import vars

def writeCluster():

    #sources
    p = Path('DatasetsFormatted/gene/genes.csv')
    genes = pd.read_csv(p, header=0, index_col=False,dtype={'entrezGeneIdA': str, 'entrezGeneIdB': str, 'pubmedId': str})

    #connect to db
    driver = GraphDatabase.driver(vars.serverurl, auth=(vars.servername, vars.serverpassword))

    #defining queries
    def init_datasets(tx):
        tx.run("CREATE OR REPLACE DATABASE genescluster2")

    def interaction(tx, uniprotIdA, entrezGeneIdA, ensemblIdA, hgncSymbolA,
                     uniprotIdB, entrezGeneIdB, ensemblIdB, hgncSymbolB,
                     detectionMethod, interactionType, pubmedId, dataSource, reliabilityScore):
        tx.run("MERGE (a:Gene {idm: ($uniprotIdA +'|'+ $entrezGeneIdA +'|'+ $ensemblIdA),"
               "uniprotId: $uniprotIdA, entrezGeneId: $entrezGeneIdA,"
               "ensemblId: $ensemblIdA, hgncSymbol: $hgncSymbolA, cluster: false})"
               "MERGE (b:Gene {idm: ($uniprotIdB +'|'+ $entrezGeneIdB +'|'+ $ensemblIdB),"
               "uniprotId: $uniprotIdB, entrezGeneId: $entrezGeneIdB,"
               "ensemblId: $ensemblIdB, hgncSymbol: $hgncSymbolB, cluster: false})"
               "MERGE (a)-[i:INTERACTION {detectionMethod: $detectionMethod, interactionType: $interactionType,"
               "pubmedId: $pubmedId, dataSource: $dataSource, reliabilityScore: $reliabilityScore}]->(b)",
               uniprotIdA=uniprotIdA, entrezGeneIdA=entrezGeneIdA, ensemblIdA=ensemblIdA, hgncSymbolA=hgncSymbolA,
               uniprotIdB=uniprotIdB, entrezGeneIdB=entrezGeneIdB, ensemblIdB=ensemblIdB, hgncSymbolB=hgncSymbolB,
               detectionMethod=detectionMethod, interactionType=interactionType, pubmedId=pubmedId,
               dataSource=dataSource, reliabilityScore=reliabilityScore)

    #Calculates centrality of only single nodes (not clusters)
    def centrality(tx):
        centrality = []
        result = tx.run("MATCH (u: Gene {cluster: false}) "
                        "RETURN u.idm AS name, "
                        "size((u) - [: INTERACTION]->({cluster: false})) AS follows, "
                        "size((u) < -[: INTERACTION]-({cluster: false})) AS followers "
                        "ORDER BY (follows+followers) DESC")
        for record in result:
            centrality.append((record["name"],record["follows"]+record["followers"]))
        return centrality

    #Returns the first 35 single nodes connected to the selected one
    def getNeighbors(tx, id):
        neighbors = []
        i = 0
        result = tx.run("MATCH (p:Gene {idm: $id}) "
                        "CALL apoc.neighbors.athop(p, 'INTERACTION', 1) YIELD node "
                        "RETURN node.idm AS name, node.cluster AS cluster", id=id)
        for record in result:
            i = i+1
            if(i < 35):
                if(record["cluster"] == False):
                    neighbors.append((record["name"], record["cluster"]))
                else:
                    i = i-1
        return neighbors

    #Returns all the nodes (single and clusters) connected to the selected node
    def getNeighbors2(tx, id):
        neighbors = []
        result = tx.run("MATCH (p:Gene {idm: $id}) "
                        "CALL apoc.neighbors.athop(p, 'INTERACTION', 1) YIELD node "
                        "RETURN node.idm AS name, node.cluster AS cluster", id=id)
        for record in result:
            neighbors.append((record["name"],record["cluster"]))
        return neighbors

    def deleteNode(tx, id):
        tx.run("MATCH (n:Gene {idm: $id}) DETACH DELETE n", id=id)

    def createClusterNode(tx, id, idcluster):
        tx.run("MERGE (a:Gene {idm: $id, cluster: true, idcluster: $idcluster})", id=id, idcluster=idcluster)

    def createClusterEdge(tx, id1, id2):
        tx.run("MATCH (a:Gene), (b:Gene) WHERE a.idm = $id1 AND b.idm = $id2 "
               "CREATE (a)-[i: INTERACTION]->(b) RETURN i", id1=id1, id2=id2)

    def saveEdgesOfClusters(tx, uni, ent, ens):
        neighbors = []
        result = tx.run("MATCH (p:Gene {uniprotId: $uni, entrezGeneId: $ent, ensemblId: $ens}) "
                        "CALL apoc.neighbors.athop(p, 'INTERACTION', 1) YIELD node "
                        "RETURN node.uniprotId AS uniId, node.entrezGeneId AS entId, node.ensemblId AS ensId", uni=uni, ent=ent, ens=ens)
        for record in result:
            id = record['uniId']+"|"+record['entId']+"|"+record['ensId']
            neighbors.append(id)
        return neighbors

    def setEdgeValues(tx, id, intEdges, extEdges):
        tx.run("MATCH (a:Gene) WHERE a.idm = $id "
               "SET a.internalEdges = $intEdges, a.externalEdges = $extEdges "
               "RETURN a", id=id, intEdges=intEdges, extEdges=extEdges)

    #rewriting database
    with driver.session() as session:
        session.write_transaction(init_datasets)

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
        with driver.session(database="genescluster2") as session:
            session.write_transaction(interaction, row['uniprotIdA'], row['entrezGeneIdA'], row['ensemblIdA'],
                                      row['hgncSymbolA'], row['uniprotIdB'], row['entrezGeneIdB'], row['ensemblIdB'],
                                      row['hgncSymbolB'], row['detectionMethod'], row['interactionType'],
                                      row['pubmedId'], row['dataSource'], row['reliabilityScore'])

    #clusterize
    clusters = []
    indexcluster = 0
    while(True):

        #calculate centrality
        with driver.session(database="genescluster2") as session:
             centralities = session.read_transaction(centrality)

             #clustering index
             if(centralities[0][1] > 15): #Min 15 nodes connected to create a cluster

                indexcluster = indexcluster + 1

                #get neighboring nodes
                clusterid = centralities[0][0]
                clusterEdges = []
                neighbors = session.read_transaction(getNeighbors,clusterid)
                neighbors2 = session.read_transaction(getNeighbors2, clusterid)
                for ele in neighbors2:
                    clusterEdges.append(ele[0])
                session.write_transaction(deleteNode, clusterid)

                #get cluster edges
                for ele in neighbors:
                    clusterid += ";" + ele[0]
                    neighbors2 = session.read_transaction(getNeighbors2, ele[0])
                    session.write_transaction(deleteNode, ele[0])
                    for ele2 in neighbors2:
                        clusterEdges.append(ele2[0])

                #clean edges (duplicates, internal edges)
                clusterEdges = list(dict.fromkeys(clusterEdges))
                if clusterEdges.count(centralities[0][0]) > 0:
                    clusterEdges.remove(centralities[0][0])
                for elems in neighbors:
                    if clusterEdges.count(elems[0]) > 0:
                        clusterEdges.remove(elems[0])

                #create cluster node
                idcluster = "cluster"+str(indexcluster)
                session.write_transaction(createClusterNode,clusterid,idcluster)
                clusters.append(clusterid)

                #create cluster edges
                for el in clusterEdges:
                    session.write_transaction(createClusterEdge, clusterid, el)

             else:
                break

    edgesOfClusters = []
    with driver.session(database="genes") as session:
        for el in clusters:
            doneclusters = []
            internaledges = 0
            externaledges = 0
            el2 = el.split(";")
            for el3 in el2:
                el4 = el3.split("|")
                neighbors = session.read_transaction(saveEdgesOfClusters,el4[0],el4[1],el4[2])
                for el5 in neighbors:
                    if el5 in doneclusters:
                        pass
                    elif el5 in el2:
                        internaledges = internaledges + 1
                    else:
                        externaledges = externaledges + 1
                doneclusters.append(el3)
            tuple = (el,internaledges,externaledges)
            edgesOfClusters.append(tuple)

    with driver.session(database="genescluster2") as session:
        for el in edgesOfClusters:
            session.write_transaction(setEdgeValues, el[0], el[1], el[2])

    #close db
    driver.close()