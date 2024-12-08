import pandas as pd
from pathlib import Path
from pandas_profiling import ProfileReport

#Use of pandas_profiling module to obtain information regarding the columns of the datasets
def dataquality():

    #dip - data quality
    p = Path('Datasets/gene/dip.txt')
    dip = pd.read_csv(p, sep='\t', index_col=False )
    profile = ProfileReport(dip, title="dip - data quality")
    p = Path("DataQuality/gene/dip.json")
    profile.to_file(p)
    p = Path("DataQuality/gene/dip.html")
    profile.to_file(p)

    #innatedb - data quality
    p = Path('Datasets/gene/innatedb.mitab')
    innatedb = pd.read_csv(p, sep='\t', index_col=False )
    profile = ProfileReport(innatedb, title="innatedb - data quality")
    p = Path("DataQuality/gene/innatedb.json")
    profile.to_file(p)
    p = Path("DataQuality/gene/innatedb.html")
    profile.to_file(p)

    #matrixdb - data quality
    p = Path('Datasets/gene/matrixdb.tab')
    matrixdb = pd.read_csv(p, sep='\t', index_col=False )
    profile = ProfileReport(matrixdb, title="matrixdb - data quality")
    p = Path("DataQuality/gene/matrixdb.json")
    profile.to_file(p)
    p = Path("DataQuality/gene/matrixdb.html")
    profile.to_file(p)

    #mint - data quality
    mintcolumns = ['uniprotIdA','uniprotIdB','intactA','intactB','symbolA','symbolB',
                   'detectionMethod','author','pubmedId','taxidA','taxidB',
                   'interactionType','discard1','discard2','miscore']
    p = Path('Datasets/gene/mint.txt')
    mint = pd.read_csv(p, sep='\t', index_col=False,names=mintcolumns )
    profile = ProfileReport(mint, title="mint - data quality")
    p = Path("DataQuality/gene/mint.json")
    profile.to_file(p)
    p = Path("DataQuality/gene/mint.html")
    profile.to_file(p)

    #biogrid - data quality
    p = Path('Datasets/gene/biogrid.txt')
    biogrid = pd.read_csv(p, sep='\t', index_col=False)
    profile = ProfileReport(biogrid, title="biogrid - data quality")
    p = Path("DataQuality/gene/biogrid.json")
    profile.to_file(p)
    p = Path("DataQuality/gene/biogrid.html")
    profile.to_file(p)

    #intact - data quality
    p = Path('Datasets/gene/intact.txt')
    intact = pd.read_csv(p, sep='\t', index_col=False)
    profile = ProfileReport(intact, title="intact - data quality")
    p = Path("DataQuality/gene/intact.json")
    profile.to_file(p)
    p = Path("DataQuality/gene/intact.html")
    profile.to_file(p)

    #biogridDrugs - data quality
    p = Path('Datasets/drug/biogridDrugs.txt')
    biogridDrugs = pd.read_csv(p, sep='\t', index_col=False )
    profile = ProfileReport(biogridDrugs, title="biogridDrugs - data quality")
    p = Path("DataQuality/drug/biogridDrugs.json")
    profile.to_file(p)
    p = Path("DataQuality/drug/biogridDrugs.html")
    profile.to_file(p)

    #dgiDrugs - data quality
    p = Path('Datasets/drug/dgiDrugs.tsv')
    dgiDrugs = pd.read_csv(p, sep='\t', index_col=False )
    profile = ProfileReport(dgiDrugs, title="dgiDrugs - data quality")
    p = Path("DataQuality/drug/dgiDrugs.json")
    profile.to_file(p)
    p = Path("DataQuality/drug/dgiDrugs.html")
    profile.to_file(p)

    #biosnapDiseases - data quality
    p = Path('Datasets/disease/biosnapDiseases.tsv')
    biosnapDiseases = pd.read_csv(p, sep='\t', index_col=False )
    profile = ProfileReport(biosnapDiseases, title="biosnapDiseases - data quality")
    p = Path("DataQuality/disease/biosnapDiseases.json")
    profile.to_file(p)
    p = Path("DataQuality/disease/biosnapDiseases.html")
    profile.to_file(p)

    #disgenetDiseases - data quality
    p = Path('Datasets/disease/disgenetDiseases.tsv')
    disgenetDiseases = pd.read_csv(p, sep='\t', index_col=False )
    profile = ProfileReport(disgenetDiseases, title="disgenetDiseases - data quality")
    p = Path("DataQuality/disease/disgenetDiseases.json")
    profile.to_file(p)
    p = Path("DataQuality/disease/disgenetDiseases.html")
    profile.to_file(p)
