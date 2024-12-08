from DataQuality.dataquality import dataquality
from Parsers.gene.dipParser import parsingDip
from Parsers.gene.innatedbParser import parsingInnatedb
from Parsers.gene.matrixdbParser import parsingMatrixdb
from Parsers.gene.mintParser import parsingMint
from Parsers.gene.biogridParser import parsingBiogrid
from Parsers.gene.intactParser import parsingIntact
from Parsers.drug.biogridDrugsParser import parsingBiogridDrugs
from Parsers.drug.dgiDrugsParser import parsingDgiDrugs
from Parsers.disease.biosnapDiseasesParser import parsingBiosnapDiseases
from Parsers.disease.disgenetDiseasesParser import parsingDisgenetDiseases
from Aggregation.geneAggregation import geneAggregation
from Aggregation.drugAggregation import drugAggregation
from Aggregation.diseaseAggregation import diseaseAggregation
from reliabilityScore import reliabilityScore
from DataQualityFormatted.dataqualityformatted import dataqualityformatted
from Neo4j.writeGenes import writeGenes
from Neo4j.writeDrugs import writeDrugs
from Neo4j.writeDiseases import writeDiseases
from Neo4j.writeCluster import writeCluster

print("ATTENTION! ALL THE PROCESS COULD TAKE A LONG TIME")

#Data quality on datasets
print("Data Quality started")
dataquality()
print("Data Quality done")

#Parsing files
print("parsingBiogrid started")
parsingBiogrid()
print("parsingBiogrid done")

print("parsingDip started")
parsingDip()
print("parsingDip done")

print("parsingInnatedb started")
parsingInnatedb()
print("parsingInnatedb done")

print("parsingMatrixdb started")
parsingMatrixdb()
print("parsingMatrixdb done")

print("parsingMint started")
parsingMint()
print("parsingMint done")

print("parsingIntact started")
parsingIntact()
print("parsingIntact done")

print("parsingBiogridDrugs started")
parsingBiogridDrugs()
print("parsingBiogridDrugs done")

print("parsingDgiDrugs started")
parsingDgiDrugs()
print("parsingDgiDrugs done")

print("parsingBiosnapDiseases started")
parsingBiosnapDiseases()
print("parsingBiosnapDiseases done")

print("parsingDisgenetDiseases started")
parsingDisgenetDiseases()
print("parsingDisgenetDiseases done")

#Data Aggregation
print("geneAggregation started")
geneAggregation()
print("geneAggregation done")

print("drugAggregation started")
drugAggregation()
print("drugAggregation done")

print("diseaseAggregation started")
diseaseAggregation()
print("diseaseAggregation done")

#Reliability score
print("reliabilityScore started")
reliabilityScore()
print("reliabilityScore done")

#Data quality on formatted datasets
print("Data Quality Formatted started")
dataqualityformatted()
print("Data Quality Formatted done")

#Moving to neo4j
print("write genes to neo4j started")
writeGenes()
print("write genes to neo4j done")

print("write drugs to neo4j started")
writeDrugs()
print("write drugs to neo4j done")

print("write diseases to neo4j started")
writeDiseases()
print("write diseases to neo4j done")

print("write cluster to neo4j started")
writeCluster()
print("write cluster to neo4j done")
