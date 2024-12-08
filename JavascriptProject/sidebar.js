//Load sidebar data
var sidebar = JSON.parse(loadFile('nodejsserver/list.txt'));

//Init subset, switch and ordering
var subsetside = cy.collection();
var subsetsidedrugs = cy.collection();
var subsetsidediseases = cy.collection();
var subsetsideedges = cy.collection();
var mapnodesoccurrences = new Map();
var elemgenes = [];
var initswitch = "drug";
var inittab = "default";
var namesimilarity = "";
var indexsimilarity = "";
var t1order = "asc1";
var t2order = "asc2";
var t3order = "asc3";
var t4order = "asc4";
document.getElementById("drugswitch").style.backgroundColor = "#737373";
document.getElementById("resetsidebar").style.visibility = "hidden";
document.getElementById("ddsetscontainer").style.visibility = "hidden";
writelist("drug","asc1");

//Write list func
function writelist(ddswitch,order){

    inittab = "default";
    //Rewrite headers
    document.getElementById("sidebarscroll").style.top = "18%";
    document.getElementById("sidebarscroll").style.height = "80%";
    var sidebarcont = document.getElementById("sidehead");
    if(sidebarcont.getElementsByClassName("similaritytitle").length > 0){
        sidebarcont.getElementsByClassName("similaritytitle")[0].remove();
    }
    if(sidebarcont.getElementsByClassName("returnbutton").length > 0){
        sidebarcont.getElementsByClassName("returnbutton")[0].remove();
    }
    var sidebarhead = document.getElementById("sidebar");
    sidebarhead.innerHTML = "";
    var tr1 = document.createElement("tr");
    var tr2 = document.createElement("tr");
    var h11 = document.createElement("th");
    var h21 = document.createElement("th");
    var h31 = document.createElement("th");
    var h41 = document.createElement("th");
    var h12 = document.createElement("th");
    var h22 = document.createElement("th");
    var h32 = document.createElement("th");
    var h42 = document.createElement("th");
    var h52 = document.createElement("th");
    h31.colSpan = "2";
    h31.innerText = "Edges";
    h12.onclick = sortTable1;
    h12.innerHTML = "Name&nbsp;<img id='orderimg1' src='style/greenarrow.png' width='10' height='10'>";
    h22.onclick = sortTable2;
    h22.innerHTML = "Genes&nbsp;<img id='orderimg2' src='style/greenarrow.png' width='10' height='10'>";
    h32.onclick = sortTable3;
    h32.innerHTML = "Int&nbsp;<img id='orderimg3' src='style/greenarrow.png' width='10' height='10'>";
    h42.onclick = sortTable4;
    h42.innerHTML = "Ext&nbsp;<img id='orderimg4' src='style/greenarrow.png' width='10' height='10'>";
    h52.innerText = "Similar";
    tr1.appendChild(h11);
    tr1.appendChild(h21);
    tr1.appendChild(h31);
    tr1.appendChild(h41);
    tr2.appendChild(h12);
    tr2.appendChild(h22);
    tr2.appendChild(h32);
    tr2.appendChild(h42);
    tr2.appendChild(h52);
    sidebarhead.appendChild(tr1);
    sidebarhead.appendChild(tr2);
    sidebarcont.appendChild(sidebarhead);

    if(order === "asc1"){
        t1order = "des1";
        sidebar.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0));
        document.getElementById("orderimg1").src = "style/greenarrow.png";
        document.getElementById("orderimg1").style.visibility = "";
        document.getElementById("orderimg2").style.visibility = "hidden";
        document.getElementById("orderimg3").style.visibility = "hidden";
        document.getElementById("orderimg4").style.visibility = "hidden";
    }
    else if(order === "des1"){
        t1order = "asc1";
        sidebar.sort((a,b) => (a.name < b.name) ? 1 : ((b.name < a.name) ? -1 : 0));
        document.getElementById("orderimg1").src = "style/redarrow.png";
        document.getElementById("orderimg1").style.visibility = "";
        document.getElementById("orderimg2").style.visibility = "hidden";
        document.getElementById("orderimg3").style.visibility = "hidden";
        document.getElementById("orderimg4").style.visibility = "hidden";
    }
    else if(order === "asc2"){
        t2order = "des2";
        sidebar.sort((a,b) => (a.numGenes > b.numGenes) ? 1 : ((b.numGenes > a.numGenes) ? -1 : 0));
        document.getElementById("orderimg2").src = "style/greenarrow.png";
        document.getElementById("orderimg2").style.visibility = "";
        document.getElementById("orderimg1").style.visibility = "hidden";
        document.getElementById("orderimg3").style.visibility = "hidden";
        document.getElementById("orderimg4").style.visibility = "hidden";
    }
    else if(order === "des2"){
        t2order = "asc2";
        sidebar.sort((a,b) => (a.numGenes < b.numGenes) ? 1 : ((b.numGenes < a.numGenes) ? -1 : 0));
        document.getElementById("orderimg2").src = "style/redarrow.png";
        document.getElementById("orderimg2").style.visibility = "";
        document.getElementById("orderimg1").style.visibility = "hidden";
        document.getElementById("orderimg3").style.visibility = "hidden";
        document.getElementById("orderimg4").style.visibility = "hidden";
    }
    else if(order === "asc3"){
        t3order = "des3";
        sidebar.sort((a,b) => (a.intedges > b.intedges) ? 1 : ((b.intedges > a.intedges) ? -1 : 0));
        document.getElementById("orderimg3").src = "style/greenarrow.png";
        document.getElementById("orderimg3").style.visibility = "";
        document.getElementById("orderimg1").style.visibility = "hidden";
        document.getElementById("orderimg2").style.visibility = "hidden";
        document.getElementById("orderimg4").style.visibility = "hidden";
    }
    else if(order === "des3"){
        t3order = "asc3";
        sidebar.sort((a,b) => (a.intedges < b.intedges) ? 1 : ((b.intedges < a.intedges) ? -1 : 0));
        document.getElementById("orderimg3").src = "style/redarrow.png";
        document.getElementById("orderimg3").style.visibility = "";
        document.getElementById("orderimg1").style.visibility = "hidden";
        document.getElementById("orderimg2").style.visibility = "hidden";
        document.getElementById("orderimg4").style.visibility = "hidden";
    }
    else if(order === "asc4"){
        t4order = "des4";
        sidebar.sort((a,b) => (a.extedges > b.extedges) ? 1 : ((b.extedges > a.extedges) ? -1 : 0));
        document.getElementById("orderimg4").src = "style/greenarrow.png";
        document.getElementById("orderimg4").style.visibility = "";
        document.getElementById("orderimg1").style.visibility = "hidden";
        document.getElementById("orderimg2").style.visibility = "hidden";
        document.getElementById("orderimg3").style.visibility = "hidden";
    }
    else if(order === "des4"){
        t4order = "asc4";
        sidebar.sort((a,b) => (a.extedges < b.extedges) ? 1 : ((b.extedges < a.extedges) ? -1 : 0));
        document.getElementById("orderimg4").src = "style/redarrow.png";
        document.getElementById("orderimg4").style.visibility = "";
        document.getElementById("orderimg1").style.visibility = "hidden";
        document.getElementById("orderimg2").style.visibility = "hidden";
        document.getElementById("orderimg3").style.visibility = "hidden";
    }



    sidebar.forEach(element => {
        if(element.type === ddswitch && element.name !== ""){

            var table = document.getElementById("sidebarbody");
            var tr = document.createElement("tr");
            var td1 = document.createElement("td");
            var td2 = document.createElement("td");
            var td3 = document.createElement("td");
            var td4 = document.createElement("td");
            var td5 = document.createElement("td");
            var btn = document.createElement("IMG");

            td1.innerText = element.name;
            td2.innerText = element.numGenes;
            td3.innerText = element.intedges;
            td4.innerText = element.extedges;
            btn.src = "style/goto.png";
            btn.width = "20";
            btn.height = "20";

            tr.appendChild(td1);
            tr.appendChild(td2);
            tr.appendChild(td3);
            tr.appendChild(td4);
            tr.appendChild(td5);
            td5.appendChild(btn);
            table.appendChild(tr);

            td1.onclick = clicksideelem.bind(this,element.name,element.type,element.numGenes,element.intedges,element.extedges);
            btn.onclick = showsimilarity.bind(this,element.name,element.index);
        }
    });
}

//On click sidebar element func
function clicksideelem(name,type,numGenes,intedges,extedges){
    //Check if already created
    if(document.getElementById("menu"+name)){
        document.getElementById("sidebarcontainer").style.visibility = "hidden";
        return;
    };

    //Loading
    document.getElementById("loader").style.visibility = "visible";
    document.getElementById("sidebarcontainer").style.visibility = "hidden";

    //Reset var
    elemgenes = [];

    //Set opacity
    cy.nodes().style('background-opacity',0.5);

    //Init subset and subcluster
    subsetside = cy.collection();
    var subcluster = [];

    if(type === "drug"){

        var query = "MATCH (n: Drug {drugName: $named})-[r]->(m) RETURN n,r,m";
        var session = driver.session({database:"drugs", defaultAccessMode: neo4j.session.READ});
        var readTxResultPromise = session.readTransaction(txc => {
            var result = txc.run(query,{named: name})
            return result
        })
        readTxResultPromise
            .then(result => {
                result.records.forEach(element => {
                    var idGene = element._fields[2].properties.entrezGeneId;
                    cy.nodes().forEach(function( ele ){
                        if(ele.data("entrezGeneId") === idGene){
                            subsetsidedrugs = subsetsidedrugs.union(ele);
                            elemgenes.push(ele.id());
                            if(mapnodesoccurrences.has(ele.id())){
                                mapnodesoccurrences.set(ele.id(),mapnodesoccurrences.get(ele.id()) + 1);
                            }
                            else{
                                mapnodesoccurrences.set(ele.id(),1);
                            }
                        }
                        else if(Array.isArray(ele.data("nodesEntrez")) &&
                            ele.data("nodesEntrez").includes(idGene)){
                            var tuple = { cluster: ele.id(), gene: idGene };
                            subcluster.push(tuple);
                        }
                    });

                });
            })
            .catch(error => {
                console.log(error)
            })
            .then(() => {
                session.close();

                if(subcluster.length < 1){
                    displaySidebarElem(name,type,numGenes,intedges,extedges,elemgenes);
                }
                else {
                    extractNode(subcluster,name,type,numGenes,intedges,extedges,elemgenes);
                }
            })

    }
    else{

        var query = "MATCH (n: Disease {diseaseName: $named})-[r]->(m) RETURN n,r,m";
        var session = driver.session({database:"diseases", defaultAccessMode: neo4j.session.READ});
        var readTxResultPromise = session.readTransaction(txc => {
            var result = txc.run(query,{named: name})
            return result
        })
        readTxResultPromise
            .then(result => {
                result.records.forEach(element => {

                    var idGene = element._fields[2].properties.entrezGeneId;
                    cy.nodes().forEach(function( ele ){
                        if(ele.data("entrezGeneId") === idGene){
                            subsetsidediseases = subsetsidediseases.union(ele);
                            elemgenes.push(ele.id());
                            if(mapnodesoccurrences.has(ele.id())){
                                mapnodesoccurrences.set(ele.id(),mapnodesoccurrences.get(ele.id()) + 1);
                            }
                            else{
                                mapnodesoccurrences.set(ele.id(),1);
                            }
                        }
                        else if(Array.isArray(ele.data("nodesEntrez")) &&
                            ele.data("nodesEntrez").includes(idGene)){
                            var tuple = { cluster: ele.id(), gene: idGene };
                            subcluster.push(tuple);
                        }
                    });

                });
            })
            .catch(error => {
                console.log(error)
            })
            .then(() => {
                session.close();
                if(subcluster.length < 1){
                    displaySidebarElem(name,type,numGenes,intedges,extedges,elemgenes);
                }
                else {
                    extractNode(subcluster,name,type,numGenes,intedges,extedges,elemgenes);
                }
            })

    }

};

//Show similarity func
function showsimilarity(name,index){

    inittab = "similarity";
    namesimilarity = name;
    indexsimilarity = index;
    //Rewrite headers
    var sidehead = document.getElementById("sidehead");
    var sidebarhead = document.getElementById("sidebar");
    sidebarhead.innerHTML = "";
    var divh = document.createElement("div");
    var returnbtn = document.createElement("img");
    var tr = document.createElement("tr");
    var h1 = document.createElement("th");
    var h2 = document.createElement("th");
    var h3 = document.createElement("th");
    divh.className = "similaritytitle";
    divh.innerText = name;
    returnbtn.width = "27";
    returnbtn.height = "27";
    returnbtn.src = "style/return.png";
    returnbtn.style.display = "inline";
    returnbtn.className = "returnbutton";
    returnbtn.onclick = function (){
        var e = document.getElementById("sidebarbody");
        var child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }
        initswitch = "drug";
        inittab = "default";
        writelist(initswitch,"asc1");
        document.getElementById("drugswitch").style.backgroundColor = "#737373";
        document.getElementById("diseaseswitch").style.backgroundColor = "";
    };
    h1.innerText = "Name";
    h2.innerText = "Common";
    h3.innerText = "Jaccard";
    tr.appendChild(h1);
    tr.appendChild(h2);
    tr.appendChild(h3);
    sidehead.prepend(returnbtn);
    sidehead.prepend(divh);
    sidebarhead.appendChild(tr);

    //Rewrite body
    document.getElementById("sidebarscroll").style.top = "20.1%";
    document.getElementById("sidebarscroll").style.height = "78%";
    if(initswitch === "drug"){
        var similaritylist = JSON.parse(loadFile('nodejsserver/similarities/'+index+'drugs.txt'));
    }
    else{
        var similaritylist = JSON.parse(loadFile('nodejsserver/similarities/'+index+'diseases.txt'));
    }
    similaritylist.sort((a,b) => (a.common < b.common) ? 1 : ((b.common < a.common) ? -1 : 0));

    var e = document.getElementById("sidebarbody");
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }

    similaritylist.forEach(element => {
        if(element.name !== "") {

            var table = document.getElementById("sidebarbody");
            var tr = document.createElement("tr");
            var td1 = document.createElement("td");
            var td2 = document.createElement("td");
            var td3 = document.createElement("td");

            td1.innerText = element.name;
            td2.innerText = element.common;
            td3.innerText = element.jaccard.toFixed(2);

            tr.appendChild(td1);
            tr.appendChild(td2);
            tr.appendChild(td3);
            table.appendChild(tr);

            td1.onclick = function () {
                for (var i = 0; i < sidebar.length; i++) {
                    if (sidebar[i].name === element.name) {
                        clicksideelem(element.name, sidebar[i].type, sidebar[i].numGenes, sidebar[i].intedges, sidebar[i].extedges);
                        break;
                    }
                }
            }
        }
    });

    //Update search bar
    document.getElementById('myInputside').value = "";
    searchside();

};

//Extract from cluster
function extractNode(subcluster,name,type,numGenes,intedges,extedges,elemgenes){
    //Vars
    var filterel = cy.getElementById(subcluster[0].cluster);
    var idGene = subcluster[0].gene;
    var nodepos = filterel.position();
    var internallinks = 0;
    var externallinks = 0;

    //Delete data from cluster
    var nodes = filterel.data("nodes");
    for( var i = 0; i < nodes.length; i++){
        if ( nodes[i].split("|")[1] === idGene) {
            nodes.splice(i, 1);
        }
    }

    var nodesEntrez = filterel.data("nodesEntrez");
    for( var i = 0; i < nodesEntrez.length; i++){
        if ( nodesEntrez[i] === idGene) {
            nodesEntrez.splice(i, 1);
        }
    }

    var query = "MATCH (n: Gene {entrezGeneId: $named})-[r]-(m) RETURN n,r,m";
    var session = driver.session({database:"genes", defaultAccessMode: neo4j.session.READ});
    var readTxResultPromise = session.readTransaction(txc => {
        var result = txc.run(query,{named: idGene})
        return result
    })
    readTxResultPromise
        .then(result => {
            result.records.forEach(element => {

                id1 = element._fields[0].properties.uniprotId+"|"+
                    element._fields[0].properties.entrezGeneId+"|"+
                    element._fields[0].properties.ensemblId;
                id2 = element._fields[2].properties.uniprotId+"|"+
                    element._fields[2].properties.entrezGeneId+"|"+
                    element._fields[2].properties.ensemblId;

                if(nodes.includes(id2)){
                    internallinks = internallinks + 1;
                }
                else {
                    externallinks = externallinks + 1;
                }

                if(cy.getElementById(id1).length === 0){

                    cy.add({group: 'nodes',
                        data: {
                            id: id1, nodes: id1, nodesEntrez: element._fields[0].properties.entrezGeneId,
                            cluster: false, size: 1,
                            entrezGeneId: element._fields[0].properties.entrezGeneId,
                            uniprotId: element._fields[0].properties.uniprotId,
                            ensemblId: element._fields[0].properties.ensemblId,
                            hgncSymbol: element._fields[0].properties.hgncSymbol,
                            internalEdges: "none", externalEdges: "none"
                        },
                        position: { x: nodepos.x + getRandomArbitrary(-10,10), y: nodepos.y + getRandomArbitrary(-10,10) }
                    });
                    elemgenes.push(id1);
                    if(type === "drug"){
                        subsetsidedrugs = subsetsidedrugs.union(cy.getElementById(id1));
                    }
                    else {
                        subsetsidediseases = subsetsidediseases.union(cy.getElementById(id1));
                    }
                    if(mapnodesoccurrences.has(id1)){
                        mapnodesoccurrences.set(id1,mapnodesoccurrences.get(id1) + 1);
                    }
                    else{
                        mapnodesoccurrences.set(id1,1);
                    }
                }

                if(cy.getElementById(id2).length !== 0 && !cy.getElementById(id2).data("cluster")){
                    cy.add({group: 'edges',
                        data: {
                            source: id1, target: id2,
                            detectionMethod: element._fields[1].properties.detectionMethod,
                            interactionType: element._fields[1].properties.interactionType,
                            pubmedId: element._fields[1].properties.pubmedId,
                            dataSource: element._fields[1].properties.dataSource,
                            reliabilityScore: element._fields[1].properties.reliabilityScore
                        }
                    });
                }

            });
        })
        .catch(error => {
            console.log(error)
        })
        .then(() => {
            session.close();

            //Update data cluster
            filterel.data("nodes",nodes);
            filterel.data("nodesEntrez",nodesEntrez);
            let initintedges = filterel.data("internalEdges");
            let initextedges = filterel.data("externalEdges");
            filterel.data("internalEdges",initintedges-internallinks);
            filterel.data("externalEdges",initextedges-externallinks);

            //Recursion
            if(subcluster.length === 1){
                displaySidebarElem(name,type,numGenes,intedges,extedges,elemgenes);
            }
            else{
                subcluster.shift();
                extractNode(subcluster,name,type,numGenes,intedges,extedges,elemgenes);
            }
        })

}

//Display element of sidebar
function displaySidebarElem(name,type,numGenes,intedges,extedges,elemgenes){
    subsetside = subsetsidedrugs.union(subsetsidediseases);

    subsetside.style("width",30);
    subsetside.style("height",30);
    subsetside.style("background-opacity",1);
    subsetside.style("z-index",5);
    subsetside.forEach(function( ele ){
        ele.style("label",ele.data("hgncSymbol"));
    });
    subsetside.style("color","white");
    subsetside.style("font-size",6);
    subsetside.style("font-weight","bold");
    subsetside.style("text-halign","center");
    subsetside.style("text-valign","center");

    for (const [key, value] of mapnodesoccurrences) {
       if(subsetsidedrugs.difference(subsetsidediseases).includes(cy.getElementById(key))){
           if(value === 1){
               cy.getElementById(key).style("background-color","#7bccc4");
           }
           else if(value === 2){
               cy.getElementById(key).style("background-color","#4eb3d3");
           }
           else if(value === 3){
               cy.getElementById(key).style("background-color","#2b8cbe");
           }
           else{
               cy.getElementById(key).style("background-color","#08589e");
           }
       }
        else if(subsetsidediseases.difference(subsetsidedrugs).includes(cy.getElementById(key))){
            if(value === 1){
                cy.getElementById(key).style("background-color","#fc8d59");
            }
            else if(value === 2){
                cy.getElementById(key).style("background-color","#ef6548");
            }
            else if(value === 3){
                cy.getElementById(key).style("background-color","#d7301f");
            }
            else{
                cy.getElementById(key).style("background-color","#990000");
            }
        }
    }
    subsetsidedrugs.intersection(subsetsidediseases).style("background-color","#4daf4a");

    subsetsideedges = cy.collection();
    var low = 0;
    var medium = 0;
    var high = 0;
    subsetside.nodes().forEach(function( ele ){
        subsetsideedges = subsetsideedges.union(ele.edgesTo(subsetside));
    });

    subsetsideedges.forEach(function( ele ){
        if(ele.data("reliabilityScore") < 0.34){
            low = low + 1;
        }
        else if(ele.data("reliabilityScore") > 0.65){
            high = high + 1;
        }
        else {
            medium = medium + 1;
        }
    });
    let tuple1 = {x: "low", y: low};
    let tuple2 = {x: "medium", y: medium};
    let tuple3 = {x: "high", y: high};
    edgegraph([tuple1,tuple2,tuple3]);
    document.getElementById("edgegraph").style.visibility = "visible";

    subsetsideedges.style("display","element");
    subsetsideedges.style("width",3);
    subsetsideedges.style("z-index",4);

    cy.nodes().removeAllListeners();
    cy.edges().removeAllListeners();
    mouseovernodehandler();
    mouseoutnodehandler();
    mouseclicksinglenode();
    mouseclickclusternode();
    mouseoveredgehandler();
    mouseoutedgehandler();
    checkboxsets();

    cy.fit(subsetside,150);
    updatestats();

    //Add element to menu
    if(type === "drug"){
        addDrug(name,numGenes,intedges,extedges,elemgenes);
    }
    else{
        addDisease(name,numGenes,intedges,extedges,elemgenes);
    }

    var e = document.getElementById("sidebarbody");
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    initswitch = "drug";
    inittab = "default";
    writelist(initswitch,"asc1");
    document.getElementById("drugswitch").style.backgroundColor = "#737373";
    document.getElementById("diseaseswitch").style.backgroundColor = "";
    document.getElementById("resetsidebar").style.visibility = "";
    document.getElementById("ddsetscontainer").style.visibility = "";
    document.getElementById("loader").style.visibility = "hidden";

}

//On click drug/disease switch
document.getElementById("drugswitch").onclick = function(){

    if(initswitch === "disease"){

        var e = document.getElementById("sidebarbody");
        var child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }
        initswitch = "drug";
        if(inittab == "default"){
            writelist("drug","asc1");
        }
        else{
            var sidebarcont = document.getElementById("sidehead");
            sidebarcont.getElementsByClassName("similaritytitle")[0].remove();
            sidebarcont.getElementsByClassName("returnbutton")[0].remove();
            showsimilarity(namesimilarity,indexsimilarity);
        }
        searchside();

        document.getElementById("drugswitch").style.backgroundColor = "#737373";
        document.getElementById("diseaseswitch").style.backgroundColor = "";
    }
}
document.getElementById("diseaseswitch").onclick = function(){
    if(initswitch === "drug"){

        var e = document.getElementById("sidebarbody");
        var child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }
        initswitch = "disease";
        if(inittab == "default"){
            writelist("disease","asc1");
        }
        else{
            var sidebarcont = document.getElementById("sidehead");
            sidebarcont.getElementsByClassName("similaritytitle")[0].remove();
            sidebarcont.getElementsByClassName("returnbutton")[0].remove();
            showsimilarity(namesimilarity,indexsimilarity);
        }
        searchside();

        document.getElementById("drugswitch").style.backgroundColor = "";
        document.getElementById("diseaseswitch").style.backgroundColor = "#737373";
    }
}

//Search side func
function searchside() {

    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById('myInputside');
    filter = input.value.toUpperCase();
    table = document.getElementById("sidebarbody");
    tr = table.getElementsByTagName('tr');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }

}

//Sort list
function sortTable1() {
    var e = document.getElementById("sidebarbody");
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    writelist(initswitch,t1order);
    searchside();
}
function sortTable2() {
    var e = document.getElementById("sidebarbody");
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    writelist(initswitch,t2order);
    searchside();
}
function sortTable3() {
    var e = document.getElementById("sidebarbody");
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    writelist(initswitch,t3order);
    searchside();
}
function sortTable4() {
    var e = document.getElementById("sidebarbody");
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    writelist(initswitch,t4order);
    searchside();
}

//Reset function
function resetstyle(){

    //Loading
    document.getElementById("loader").style.visibility = "visible";

    cy.nodes().style('background-opacity',0.8);
    cy.nodes().style("label","");
    cy.nodes().style("z-index",3);
    cy.edges().style("display","none");
    cy.edges().style("z-index",2);
    subsetsidedrugs = cy.collection();
    subsetsidediseases = cy.collection();
    subsetside = cy.collection();
    subsetsideedges = cy.collection();
    mapnodesoccurrences.clear();
    nodesvisibility();
    colornodes();
    resizenodes();

    var divdrug = document.getElementById("drugdiv");
    var divdisease = document.getElementById("diseasediv");
    while (divdrug.lastChild.nodeName !== "I"){
        divdrug.removeChild(divdrug.lastChild);
    }
    while (divdisease.lastChild.nodeName !== "I"){
        divdisease.removeChild(divdisease.lastChild);
    }
    divdrug.appendChild(document.createElement("br"));
    divdisease.appendChild(document.createElement("br"));

    var e = document.getElementById("sidebarbody");
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    initswitch = "drug";
    inittab = "default";
    writelist(initswitch,"asc1");
    document.getElementById("drugswitch").style.backgroundColor = "#737373";
    document.getElementById("diseaseswitch").style.backgroundColor = "";

    document.getElementById("defaultdrug").style.visibility = "";
    document.getElementById("defaultdisease").style.visibility = "";
    document.getElementById("edgegraph").style.visibility = "hidden";
    document.getElementById("resetsidebar").style.visibility = "hidden";
    document.getElementById("ddsetscontainer").style.visibility = "hidden";
    document.getElementById("loader").style.visibility = "hidden";
}

//Random range number
function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

//On click checkbox sets
document.getElementById("drugset").onclick = checkboxsets;
document.getElementById("diseaseset").onclick = checkboxsets;
document.getElementById("intersectionset").onclick = checkboxsets;
function checkboxsets (){
    subsetside.style("display","none");
    var intersectionsets = subsetsidedrugs.intersection(subsetsidediseases);
    if(document.getElementById("drugset").checked){
        subsetsidedrugs.difference(intersectionsets).style("display","element");
    }
    if(document.getElementById("diseaseset").checked){
        subsetsidediseases.difference(intersectionsets).style("display","element");
    }
    if(document.getElementById("intersectionset").checked){
        intersectionsets.style("display","element");
    }
}