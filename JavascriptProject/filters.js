//On click switch and size
document.getElementById("switchbutton").onclick = resizenodes
document.getElementById("sizenodes").onclick = resizenodes
//Resizenodes func
function resizenodes(){
    if(document.getElementById("switchbutton").checked &&
        document.getElementById("sizenodes").checked){
        document.getElementById("switchlabel").innerText = "Clusters";
        cy.nodes('[?cluster]').style("width",10);
        cy.nodes('[?cluster]').style("height",10);
        cy.nodes('[!cluster]').difference(subsetside).style("width",5);
        cy.nodes('[!cluster]').difference(subsetside).style("height",5);
    }else if(document.getElementById("switchbutton").checked &&
        !document.getElementById("sizenodes").checked){
        document.getElementById("switchlabel").innerText = "Clusters";
        cy.nodes('[?cluster]').style("width",5);
        cy.nodes('[?cluster]').style("height",5);
        cy.nodes('[!cluster]').difference(subsetside).style("width",1);
        cy.nodes('[!cluster]').difference(subsetside).style("height",1);
    }else if(!document.getElementById("switchbutton").checked &&
        document.getElementById("sizenodes").checked){
        document.getElementById("switchlabel").innerText = "Nodes";
        cy.nodes('[?cluster]').style("width",5);
        cy.nodes('[?cluster]').style("height",5);
        cy.nodes('[!cluster]').difference(subsetside).style("width",10);
        cy.nodes('[!cluster]').difference(subsetside).style("height",10);
    }else{
        document.getElementById("switchlabel").innerText = "Nodes";
        cy.nodes('[?cluster]').style("width",1);
        cy.nodes('[?cluster]').style("height",1);
        cy.nodes('[!cluster]').difference(subsetside).style("width",5);
        cy.nodes('[!cluster]').difference(subsetside).style("height",5);
    }
}

//On click checkbox
document.getElementById("showbiogrid").onclick = nodesvisibility
document.getElementById("showintact").onclick = nodesvisibility
document.getElementById("showinnatedb").onclick = nodesvisibility
document.getElementById("showmint").onclick = nodesvisibility
document.getElementById("showdip").onclick = nodesvisibility
document.getElementById("showmatrixdb").onclick = nodesvisibility
document.getElementById("showunconnectednodes").onclick = nodesvisibility
//Nodevisibility func
function nodesvisibility() {
    var visiblenodes = [];
    if(!document.getElementById("showbiogrid").checked && biogridcolorset){
        biogridcolorset = false;
        document.getElementById("biogridcolor").style.border = "none";
        colornodes();
    }
    if(!document.getElementById("showinnatedb").checked && innatedbcolorset){
        innatedbcolorset = false;
        document.getElementById("innatedbcolor").style.border = "none";
        colornodes();
    }
    if(!document.getElementById("showintact").checked && intactcolorset){
        intactcolorset = false;
        document.getElementById("intactcolor").style.border = "none";
        colornodes();
    }
    if(!document.getElementById("showmint").checked && mintcolorset){
        mintcolorset = false;
        document.getElementById("mintcolor").style.border = "none";
        colornodes();
    }
    if(!document.getElementById("showdip").checked && dipcolorset){
        dipcolorset = false;
        document.getElementById("dipcolor").style.border = "none";
        colornodes();
    }
    if(!document.getElementById("showmatrixdb").checked && matrixdbcolorset){
        matrixdbcolorset = false;
        document.getElementById("matrixdbcolor").style.border = "none";
        colornodes();
    }
    cy.edges().forEach(function( ele ){
        if(document.getElementById("showbiogrid").checked &&
            ele.data("dataSource").split("|").includes("biogrid")){
            if(!visiblenodes.includes(ele.data("source"))){
                visiblenodes.push(ele.data("source"));
            }
            if(!visiblenodes.includes(ele.data("target"))){
                visiblenodes.push(ele.data("target"));
            }
        }
        else if(document.getElementById("showintact").checked &&
            ele.data("dataSource").split("|").includes("intact")){
            if(!visiblenodes.includes(ele.data("source"))){
                visiblenodes.push(ele.data("source"));
            }
            if(!visiblenodes.includes(ele.data("target"))){
                visiblenodes.push(ele.data("target"));
            }
        }
        else if(document.getElementById("showinnatedb").checked &&
            ele.data("dataSource").split("|").includes("innatedb")){
            if(!visiblenodes.includes(ele.data("source"))){
                visiblenodes.push(ele.data("source"));
            }
            if(!visiblenodes.includes(ele.data("target"))){
                visiblenodes.push(ele.data("target"));
            }
        }
        else if(document.getElementById("showmint").checked &&
            ele.data("dataSource").split("|").includes("mint")){
            if(!visiblenodes.includes(ele.data("source"))){
                visiblenodes.push(ele.data("source"));
            }
            if(!visiblenodes.includes(ele.data("target"))){
                visiblenodes.push(ele.data("target"));
            }
        }
        else if(document.getElementById("showdip").checked &&
            ele.data("dataSource").split("|").includes("dip")){
            if(!visiblenodes.includes(ele.data("source"))){
                visiblenodes.push(ele.data("source"));
            }
            if(!visiblenodes.includes(ele.data("target"))){
                visiblenodes.push(ele.data("target"));
            }
        }
        else if(document.getElementById("showmatrixdb").checked &&
            ele.data("dataSource").split("|").includes("matrixdb")){
            if(!visiblenodes.includes(ele.data("source"))){
                visiblenodes.push(ele.data("source"));
            }
            if(!visiblenodes.includes(ele.data("target"))){
                visiblenodes.push(ele.data("target"));
            }
        }
    });
    cy.nodes('[!cluster]').style("display","none");
    visiblenodes.forEach(function (item, index) {
        cy.getElementById(item).style("display","element");
    });

    if(document.getElementById("showunconnectednodes").checked){
        cy.nodes().filter(function( ele ){
            return ele.degree() === 0;
        }).style("display","element");
    }
    clickednodes.connectedEdges().filter(function( ele ){
        var datasources = ele.data('dataSource').split("|");
        if(datasources.includes("biogrid") && document.getElementById("showbiogrid").checked){
            return true;
        }
        else if(datasources.includes("intact") && document.getElementById("showintact").checked){
            return true;
        }
        else if(datasources.includes("innatedb") && document.getElementById("showinnatedb").checked){
            return true;
        }
        else if(datasources.includes("mint") && document.getElementById("showmint").checked){
            return true;
        }
        else if(datasources.includes("dip") && document.getElementById("showdip").checked){
            return true;
        }
        else if(datasources.includes("matrixdb") && document.getElementById("showmatrixdb").checked){
            return true;
        }
        else {
            ele.style("display","none");
            return false;
        }
    }).style("display","element");
    subsetside.style("display","element");
    updatestats();
}

//Initialize colors var
var biogridcolorset = false;
var intactcolorset = false;
var innatedbcolorset = false;
var mintcolorset = false;
var dipcolorset = false;
var matrixdbcolorset = false;
//On click color
document.getElementById("biogridcolor").onclick = function (){

    if(!document.getElementById("showbiogrid").checked){
        return;
    }
    if(biogridcolorset){
        biogridcolorset = false;
        document.getElementById("biogridcolor").style.border = "none";
    }
    else {
        biogridcolorset = true;
        document.getElementById("biogridcolor").style.border = "solid white";
    }

    colornodes();
}
document.getElementById("innatedbcolor").onclick = function (){

    if(!document.getElementById("showinnatedb").checked){
        return;
    }
    if(innatedbcolorset){
        innatedbcolorset = false;
        document.getElementById("innatedbcolor").style.border = "none";
    }
    else {
        innatedbcolorset = true;
        document.getElementById("innatedbcolor").style.border = "solid white";
    }

    colornodes();
}
document.getElementById("intactcolor").onclick = function (){

    if(!document.getElementById("showintact").checked){
        return;
    }
    if(intactcolorset){
        intactcolorset = false;
        document.getElementById("intactcolor").style.border = "none";
    }
    else {
        intactcolorset = true;
        document.getElementById("intactcolor").style.border = "solid white";
    }

    colornodes();
}
document.getElementById("mintcolor").onclick = function (){

    if(!document.getElementById("showmint").checked){
        return;
    }
    if(mintcolorset){
        mintcolorset = false;
        document.getElementById("mintcolor").style.border = "none";
    }
    else {
        mintcolorset = true;
        document.getElementById("mintcolor").style.border = "solid white";
    }

    colornodes();
}
document.getElementById("dipcolor").onclick = function (){

    if(!document.getElementById("showdip").checked){
        return;
    }
    if(dipcolorset){
        dipcolorset = false;
        document.getElementById("dipcolor").style.border = "none";
    }
    else {
        dipcolorset = true;
        document.getElementById("dipcolor").style.border = "solid white";
    }

   colornodes();
}
document.getElementById("matrixdbcolor").onclick = function (){

    if(!document.getElementById("showmatrixdb").checked){
        return;
    }
    if(matrixdbcolorset){
        matrixdbcolorset = false;
        document.getElementById("matrixdbcolor").style.border = "none";
    }
    else {
        matrixdbcolorset = true;
        document.getElementById("matrixdbcolor").style.border = "solid white";
    }

    colornodes();
}
//Colornodes func
function colornodes(){

    if(!biogridcolorset && !intactcolorset && !innatedbcolorset && !mintcolorset && !dipcolorset && !matrixdbcolorset){
        cy.nodes('[!cluster]').difference(subsetside).style("background-color","#fff");
        cy.nodes().difference(subsetside).style("background-opacity",0.8);
    }
    else {
        cy.nodes('[?cluster]').style("background-opacity",0.05);
        cy.nodes('[!cluster]').forEach(function( ele ){
            var sources = [];
            ele.connectedEdges().forEach(function (ele2){
                ele2.data("dataSource").split("|").forEach(function (item, index) {
                    sources.push(item);
                });
            });

            sources = [...new Set(sources)];

            if(sources.includes("biogrid") && !biogridcolorset){
                sources.splice( sources.indexOf("biogrid"), 1 );
            }
            if(sources.includes("intact") && !intactcolorset){
                sources.splice( sources.indexOf("intact"), 1 );
            }
            if(sources.includes("innatedb") && !innatedbcolorset){
                sources.splice( sources.indexOf("innatedb"), 1 );
            }
            if(sources.includes("mint") && !mintcolorset){
                sources.splice( sources.indexOf("mint"), 1 );
            }
            if(sources.includes("dip") && !dipcolorset){
                sources.splice( sources.indexOf("dip"), 1 );
            }
            if(sources.includes("matrixdb") && !matrixdbcolorset){
                sources.splice( sources.indexOf("matrixdb"), 1 );
            }
            if(subsetside.contains(ele)){

            }
            else if(sources.length > 1){
                ele.style("background-color","#990000");
                ele.style("background-opacity",1);
            }
            else if(sources.length === 0){
                ele.style("background-color","#fff");
                ele.style("background-opacity",0.05);
            }
            else if(sources[0] === "biogrid"){
                ele.style("background-color","#ff7f00");
                ele.style("background-opacity",1);
            }
            else if(sources[0] === "intact"){
                ele.style("background-color","#66a61e");
                ele.style("background-opacity",1);
            }
            else if(sources[0] === "innatedb"){
                ele.style("background-color","#1f78b4");
                ele.style("background-opacity",1);
            }
            else if(sources[0] === "mint"){
                ele.style("background-color","#a6cee3");
                ele.style("background-opacity",1);
            }
            else if(sources[0] === "dip"){
                ele.style("background-color","#e7298a");
                ele.style("background-opacity",1);
            }
            else if(sources[0] === "matrixdb"){
                ele.style("background-color","#7570b3");
                ele.style("background-opacity",1);
            }

        });
    }

}

