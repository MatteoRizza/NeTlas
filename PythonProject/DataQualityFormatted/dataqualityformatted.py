import pandas as pd
from pathlib import Path
from pandas_profiling import ProfileReport

def dataqualityformatted():

    #dip - data quality
    p = Path('DatasetsFormatted/gene/dip.csv')
    dip = pd.read_csv(p, index_col=False )
    profile = ProfileReport(dip, title="dip - data quality")
    p = Path("DataQualityFormatted/gene/dip.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/gene/dip.html")
    profile.to_file(p)

    #innatedb - data quality
    p = Path('DatasetsFormatted/gene/innatedb.csv')
    innatedb = pd.read_csv(p, index_col=False )
    profile = ProfileReport(innatedb, title="innatedb - data quality")
    p = Path("DataQualityFormatted/gene/innatedb.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/gene/innatedb.html")
    profile.to_file(p)

    #matrixdb - data quality
    p = Path('DatasetsFormatted/gene/matrixdb.csv')
    matrixdb = pd.read_csv(p, index_col=False )
    profile = ProfileReport(matrixdb, title="matrixdb - data quality")
    p = Path("DataQualityFormatted/gene/matrixdb.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/gene/matrixdb.html")
    profile.to_file(p)

    #mint - data quality
    p = Path('DatasetsFormatted/gene/mint.csv')
    mint = pd.read_csv(p, index_col=False)
    profile = ProfileReport(mint, title="mint - data quality")
    p = Path("DataQualityFormatted/gene/mint.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/gene/mint.html")
    profile.to_file(p)

    #biogrid - data quality
    p = Path('DatasetsFormatted/gene/biogrid.csv')
    biogrid = pd.read_csv(p, index_col=False)
    profile = ProfileReport(biogrid, title="biogrid - data quality")
    p = Path("DataQualityFormatted/gene/biogrid.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/gene/biogrid.html")
    profile.to_file(p)

    #intact - data quality
    p = Path('DatasetsFormatted/gene/intact.csv')
    intact = pd.read_csv(p, index_col=False)
    profile = ProfileReport(intact, title="intact - data quality")
    p = Path("DataQualityFormatted/gene/intact.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/gene/intact.html")
    profile.to_file(p)

    # genes - data quality
    p = Path('DatasetsFormatted/gene/genes.csv')
    genes = pd.read_csv(p, index_col=False)
    profile = ProfileReport(genes, title="genes - data quality")
    p = Path("DataQualityFormatted/gene/genes.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/gene/genes.html")
    profile.to_file(p)

    #biogridDrugs - data quality
    p = Path('DatasetsFormatted/drug/biogridDrugs.csv')
    biogridDrugs = pd.read_csv(p, index_col=False )
    profile = ProfileReport(biogridDrugs, title="biogridDrugs - data quality")
    p = Path("DataQualityFormatted/drug/biogridDrugs.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/drug/biogridDrugs.html")
    profile.to_file(p)

    #dgiDrugs - data quality
    p = Path('DatasetsFormatted/drug/dgiDrugs.csv')
    dgiDrugs = pd.read_csv(p, index_col=False )
    profile = ProfileReport(dgiDrugs, title="dgiDrugs - data quality")
    p = Path("DataQualityFormatted/drug/dgiDrugs.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/drug/dgiDrugs.html")
    profile.to_file(p)

    # drugs - data quality
    p = Path('DatasetsFormatted/drug/drugs.csv')
    drugs = pd.read_csv(p, index_col=False)
    profile = ProfileReport(drugs, title="drugs - data quality")
    p = Path("DataQualityFormatted/drug/drugs.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/drug/drugs.html")
    profile.to_file(p)

    #biosnapDiseases - data quality
    p = Path('DatasetsFormatted/disease/biosnapDiseases.csv')
    biosnapDiseases = pd.read_csv(p, index_col=False )
    profile = ProfileReport(biosnapDiseases, title="biosnapDiseases - data quality")
    p = Path("DataQualityFormatted/disease/biosnapDiseases.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/disease/biosnapDiseases.html")
    profile.to_file(p)

    #disgenetDiseases - data quality
    p = Path('DatasetsFormatted/disease/disgenetDiseases.csv')
    disgenetDiseases = pd.read_csv(p, index_col=False )
    profile = ProfileReport(disgenetDiseases, title="disgenetDiseases - data quality")
    p = Path("DataQualityFormatted/disease/disgenetDiseases.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/disease/disgenetDiseases.html")
    profile.to_file(p)

    # diseases - data quality
    p = Path('DatasetsFormatted/disease/diseases.csv')
    diseases = pd.read_csv(p, index_col=False)
    profile = ProfileReport(diseases, title="diseases - data quality")
    p = Path("DataQualityFormatted/disease/diseases.json")
    profile.to_file(p)
    p = Path("DataQualityFormatted/disease/diseases.html")
    profile.to_file(p)
