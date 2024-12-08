//Add drug function
function addDrug(name,numgenes,intedges,extedges,elemgenes) {
    document.getElementById("defaultdrug").style.visibility = "hidden";
    var div = document.createElement("div");
    div.id = "menu" + name;
    div.className = "menuelement";
    div.innerHTML = "<b><u>" + name + "</u></b><br>Genes affected: " + numgenes +
        "<br>Internal edges: " + intedges + "<br>External edges: " + extedges;
    document.getElementById("drugdiv").appendChild(div);
    if (document.getElementById("drugmenu").className !== "active") {
        document.getElementById("drugmenu").click();
    }
    div.onmouseover = function () {
        subsetside.style("background-opacity", 0.3);
        subsetsideedges.style("line-opacity", 0.3);
        let nodecoll = cy.collection();
        let edgecoll = cy.collection();
        elemgenes.forEach(el => {
            nodecoll = nodecoll.union(cy.getElementById(el));
        });
        nodecoll.forEach(function( ele ){
            edgecoll = edgecoll.union(ele.edgesTo(nodecoll));
        });
        nodecoll.style("background-opacity", 1);
        edgecoll.style("line-opacity", 1);
    };
    div.onmouseout = function (){
        subsetside.style("background-opacity", 1);
        subsetsideedges.style("line-opacity", 1);
    };

}

//Add disease function
function addDisease(name,numgenes,intedges,extedges,elemgenes){
    document.getElementById("defaultdisease").style.visibility = "hidden";
        var div = document.createElement("div");
        div.id = "menu"+name;
        div.className = "menuelement";
        div.innerHTML = "<b><u>"+ name +"</u></b><br>Genes affected: " + numgenes +
            "<br>Internal edges: " + intedges + "<br>External edges: " + extedges;
        document.getElementById("diseasediv").appendChild(div);
        if(document.getElementById("diseasemenu").className !== "active"){
            document.getElementById("diseasemenu").click();
        }
    div.onmouseover = function () {
        subsetside.style("background-opacity", 0.3);
        subsetsideedges.style("line-opacity", 0.3);
        let nodecoll = cy.collection();
        let edgecoll = cy.collection();
        elemgenes.forEach(el => {
            nodecoll = nodecoll.union(cy.getElementById(el));
        });
        nodecoll.forEach(function( ele ){
            edgecoll = edgecoll.union(ele.edgesTo(nodecoll));
        });
        nodecoll.style("background-opacity", 1);
        edgecoll.style("line-opacity", 1);
    };
    div.onmouseout = function (){
        subsetside.style("background-opacity", 1);
        subsetsideedges.style("line-opacity", 1);
    };
}