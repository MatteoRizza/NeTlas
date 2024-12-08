var listUniprot = []
var listEntrez = []
var listEnsembl = []
var listHgnc = []

Object.entries(centralityfile).forEach(([key, value]) => {
    if(value.uniprotId !== "-"){
        listUniprot.push([value.uniprotId,value.id,value.centrality])
    }
    if(value.entrezGeneId !== "-"){
        listEntrez.push([value.entrezGeneId,value.id,value.centrality])
    }
    if(value.ensemblId !== "-"){
        listEnsembl.push([value.ensemblId,value.id,value.centrality])
    }
    if(value.hgncSymbol !== "-"){
        listHgnc.push([value.hgncSymbol,value.id,value.centrality])
    }
});

listUniprot = [...new Set(listUniprot)];
listEntrez = [...new Set(listEntrez)];
listEnsembl = [...new Set(listEnsembl)];
listHgnc = [...new Set(listHgnc)];

listUniprot.forEach(el => {
    var ul = document.getElementById("myUL");
    var li = document.createElement("li");
    var a = document.createElement("a");
    a.href = "#";
    a.innerText = el[0] + " (" + el[2] + ")";

    li.appendChild(a);
    ul.appendChild(li);
    li.onclick = gotogene.bind(this, el);
});

var listselected = "uniprot";
document.getElementById("unibutton").style.backgroundColor = "#b22222";

function searchgene() {

    // Declare variables
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName('li');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }

}

document.getElementById("unibutton").onclick = function(){
    if(listselected !== "uniprot"){

        listselected = "uniprot";

        document.getElementById("unibutton").style.backgroundColor = "#b22222";
        document.getElementById("entbutton").style.backgroundColor = "";
        document.getElementById("ensbutton").style.backgroundColor = "";
        document.getElementById("hgncbutton").style.backgroundColor = "";

        var e = document.getElementById("myUL");
        var child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }
        listUniprot.forEach(el => {
            var ul = document.getElementById("myUL");
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.href = "#";
            a.innerText = el[0] + " (" + el[2] + ")";

            li.appendChild(a);
            ul.appendChild(li);
            li.onclick = gotogene.bind(this, el);
        });

        searchgene();
    }
}
document.getElementById("entbutton").onclick = function(){
    if(listselected !== "entrez"){

        listselected = "entrez";

        document.getElementById("entbutton").style.backgroundColor = "#b22222";
        document.getElementById("unibutton").style.backgroundColor = "";
        document.getElementById("ensbutton").style.backgroundColor = "";
        document.getElementById("hgncbutton").style.backgroundColor = "";


        var e = document.getElementById("myUL");
        var child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }
        listEntrez.forEach(el => {
            var ul = document.getElementById("myUL");
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.href = "#";
            a.innerText = el[0] + " (" + el[2] + ")";

            li.appendChild(a);
            ul.appendChild(li);
            li.onclick = gotogene.bind(this, el);
        });

        searchgene();
    }
}
document.getElementById("ensbutton").onclick = function(){
    if(listselected !== "ensembl"){

        listselected = "ensembl";

        document.getElementById("ensbutton").style.backgroundColor = "#b22222";
        document.getElementById("unibutton").style.backgroundColor = "";
        document.getElementById("entbutton").style.backgroundColor = "";
        document.getElementById("hgncbutton").style.backgroundColor = "";

        var e = document.getElementById("myUL");
        var child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }
        listEnsembl.forEach(el => {
            var ul = document.getElementById("myUL");
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.href = "#";
            a.innerText = el[0] + " (" + el[2] + ")";

            li.appendChild(a);
            ul.appendChild(li);
            li.onclick = gotogene.bind(this, el);
        });

        searchgene();
    }
}
document.getElementById("hgncbutton").onclick = function(){
    if(listselected !== "hgnc"){

        listselected = "hgnc";

        document.getElementById("hgncbutton").style.backgroundColor = "#b22222";
        document.getElementById("unibutton").style.backgroundColor = "";
        document.getElementById("ensbutton").style.backgroundColor = "";
        document.getElementById("entbutton").style.backgroundColor = "";

        var e = document.getElementById("myUL");
        var child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }
        listHgnc.forEach(el => {
            var ul = document.getElementById("myUL");
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.href = "#";
            a.innerText = el[0] + " (" + el[2] + ")";

            li.appendChild(a);
            ul.appendChild(li);
            li.onclick = gotogene.bind(this, el);
        });

        searchgene();
    }
}

function gotogene(data){

    if(cy.getElementById(data[1]).length > 0){
        cy.fit(cy.getElementById(data[1]),300);
        var size = parseInt(cy.getElementById(data[1]).style("width"), 10)*3;
        var ani = cy.getElementById(data[1]).animation({
            style: {
                'width': size,
                'height': size
            },
            duration: 1000
        });
        ani.play().promise('completed').then(function(){
                ani.reverse().rewind().play();
        });
    }
    else {
        cy.nodes('?cluster').forEach(function( ele ){
            if(ele.data("nodes").includes(data[1])){
                cy.fit(ele,300);
                var size = parseInt(ele.style("width"), 10)*3;
                var ani = ele.animation({
                    style: {
                        'width': size,
                        'height': size
                    },
                    duration: 1000
                });
                ani.play().promise('completed').then(function(){
                    ani.reverse().rewind().play();
                });
            }
        });
    }
}