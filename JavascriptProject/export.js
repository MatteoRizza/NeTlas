//On click export
document.getElementById("expsubmit").onclick = function () {

    document.getElementById("loader").style.visibility = "visible";

    if(document.getElementById("expbiogrid").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/gene/biogrid.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'biogrid.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expmint").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/gene/mint.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'mint.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expmatrixdb").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/gene/matrixdb.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'matrixdb.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expinnatedb").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/gene/innatedb.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'innatedb.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expintact").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/gene/intact.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'intact.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expdip").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/gene/dip.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'dip.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expgenes").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/gene/genes.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'genes.csv';
        hiddenElement.click();
    }

    if(document.getElementById("exppartial").checked){

        var biogridcheck = document.getElementById("showbiogrid").checked;
        var intactcheck = document.getElementById("showintact").checked;
        var innatedbcheck = document.getElementById("showinnatedb").checked;
        var mintcheck = document.getElementById("showmint").checked;
        var dipcheck = document.getElementById("showdip").checked;
        var matrixdbcheck = document.getElementById("showmatrixdb").checked;

        var dbresult = loadFile("http://localhost:3000/visualizeddb?biogrid="+biogridcheck+
            "&intact="+intactcheck+"&innatedb="+innatedbcheck+"&mint="+mintcheck+"&dip="+dipcheck+
            "&matrixdb="+matrixdbcheck);
        //todo: set the url properly

        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(dbresult);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'visualizedDatabase.csv';
        hiddenElement.click();

    }

    if(document.getElementById("expbiogriddrugs").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/drug/biogridDrugs.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'biogridDrugs.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expdgidrugs").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/drug/dgiDrugs.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'dgiDrugs.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expdrugs").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/drug/drugs.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'drugs.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expdisgenetdiseases").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/disease/disgenetDiseases.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'disgenetDiseases.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expbiosnapdiseases").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/disease/biosnapDiseases.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'biosnapDiseases.csv';
        hiddenElement.click();
    }

    if(document.getElementById("expdiseases").checked){
        var textToSave = loadFile('./JavascriptProject/DatasetsFormatted/disease/diseases.csv');
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'diseases.csv';
        hiddenElement.click();
    }

    document.getElementById("loader").style.visibility = "hidden";

}