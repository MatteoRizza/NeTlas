//Load graph and layout
var graph = JSON.parse(loadFile('nodejsserver/graph.txt'));
var layout = JSON.parse(loadFile('nodejsserver/layout.txt'));
var performanceini = loadFile('performanceini.txt');
if(performanceini === "false"){
    performanceini = false;
}
else{
    performanceini = true;
}

//Graph style
var cy = cytoscape({
    container: document.getElementById('cy'),
    elements: graph,
    style: [
        { selector: 'node',
            style: {
                'width': 'data(size)',
                'height': 'data(size)',
                'background-color': function( ele ){
                    if(ele.data("cluster")){
                        return 'yellow';
                    }
                    else {
                        return '#fff';
                    }
                },
                'background-opacity': 0.8,
                'z-index-compare': 'manual',
                'z-index': 3
            }},
        { selector: 'edge',
            style: {
                'curve-style': 'haystack',
                'width': 1,
                'line-color': function( ele ){
                    if(ele.data("reliabilityScore") < 0.34){
                        return '#d73027';
                    }
                    else if(ele.data("reliabilityScore") > 0.65){
                        return '#1a9850';
                    }
                    else {
                        return '#ffffbf';
                    }
                },
                'target-arrow-shape': 'none',
                'display': 'none',
                'z-index-compare': 'manual',
                'z-index': 2
            }}],
    hideEdgesOnViewport: performanceini,
    textureOnViewport: performanceini,
    pixelRatio: 1.0
});

//Layout style
Object.entries(layout).forEach(([key, value]) => {
    cy.getElementById(key).position({x: value.x, y: value.y});
});
cy.fit(10);
cy.minZoom(cy.zoom());

//Init vars
var clickednodes = cy.collection();

//Map
cy.nodes('[?cluster]').style("width",10);
cy.nodes('[?cluster]').style("height",10);
cy.nodes('[!cluster]').style("width",5);
cy.nodes('[!cluster]').style("height",5);

var map = cy.jpg({bg: 'black', quality: 1});
document.getElementById('map').setAttribute('src', map);
var initialextent = cy.extent();
var initialwidthmap = parseInt(getComputedStyle(document.getElementById("focus")).width);
var initialheightmap = parseInt(getComputedStyle(document.getElementById("focus")).height);

cy.nodes('[?cluster]').style("width",5);
cy.nodes('[?cluster]').style("height",5);
cy.nodes('[!cluster]').style("width",1);
cy.nodes('[!cluster]').style("height",1);

//Reliability bitmap options
cy.nodes().style("visibility","hidden");
cy.edges().style("display","element");
cy.edges().style("line-opacity",1);
var bitmap = cy.jpg({bg: 'black', quality: 1});

//Setting background
var background = new Image();
background.src = "style/blackbackground.bmp";
//background.src = bitmap;
//To get reliabilitymap background you have to uncomment the previous line

var bottomLayer = cy.cyCanvas({
    zIndex: -1,
});
var canvas = bottomLayer.getCanvas();
var ctx = canvas.getContext("2d");

cy.on("render cyCanvas.resize", (evt) => {
    bottomLayer.resetTransform(ctx);
    bottomLayer.clear(ctx);
    bottomLayer.setTransform(ctx);
    ctx.save();

    // Draw a background
    ctx.drawImage(background, initialextent.x1, initialextent.y1, initialextent.w, initialextent.h);
});

//Set initial state of graph
cy.nodes().style("visibility","visible");
cy.edges().style("display","none");
cy.edges().style("line-opacity",1);

//On click node cluster event
function mouseclickclusternode(){
    cy.nodes('[?cluster]').on('click', function(evt){

        document.getElementById("loader").style.visibility = "visible";

        //Expand area
        var xc = evt.target.position('x');
        var yc = evt.target.position('y');
        var nearnodes = cy.nodes().filter(function( ele ){
            return ele.position('x') > xc - 30 &&
                ele.position('x') < xc + 30 &&
                ele.position('y') > yc - 30 &&
                ele.position('y') < yc + 30;
        });
        nearnodes.forEach(function( ele ){
            if(ele.position('x') > xc){
                ele.shift("x", 30);
            }
            if(ele.position('x') < xc){
                ele.shift("x", -30);
            }
            if(ele.position('y') > yc){
                ele.shift("y", 30);
            }
            if(ele.position('y') < yc){
                ele.shift("y", -30);
            }
        });

        var clusternodes = evt.target.data("nodes");
        cy.getElementById(evt.target.data("id")).remove();

        var nodescollection = cy.collection();

        //Expand nodes and edges of the cluster
        var query = "MATCH (n {uniprotId: $uni, entrezGeneId: $ent, ensemblId: $ens})-[r1]-(m1)-[r2]-(m2) RETURN n,r1,m1,r2,m2";
        var session = driver.session({database:"genes", defaultAccessMode: neo4j.session.READ});
        var readTxResultPromise = session.readTransaction(txc => {
            var unid = clusternodes[0].split("|")[0];
            var entd = clusternodes[0].split("|")[1];
            var ensd = clusternodes[0].split("|")[2];
            var result = txc.run(query,{uni: unid, ent: entd, ens: ensd})
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
                    id3 = element._fields[4].properties.uniprotId+"|"+
                        element._fields[4].properties.entrezGeneId+"|"+
                        element._fields[4].properties.ensemblId;


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
                            position: { x: xc, y: yc }
                        });
                        cy.getElementById(id1).style('z-index-compare','manual');
                    }
                    if(cy.getElementById(id2).length === 0 && clusternodes.includes(id2)){
                        cy.add({group: 'nodes',
                            data: {
                                id: id2, nodes: id2, nodesEntrez: element._fields[2].properties.entrezGeneId,
                                cluster: false, size: 1,
                                entrezGeneId: element._fields[2].properties.entrezGeneId,
                                uniprotId: element._fields[2].properties.uniprotId,
                                ensemblId: element._fields[2].properties.ensemblId,
                                hgncSymbol: element._fields[2].properties.hgncSymbol,
                                internalEdges: "none", externalEdges: "none"
                            },
                            position: { x: xc, y: yc }
                        });
                        nodescollection = nodescollection.union(cy.getElementById(id2));
                    }


                    if(cy.getElementById(id2).length !== 0 &&
                        !cy.getElementById(id2).data("cluster") &&
                        cy.getElementById(id1).edgesWith(cy.getElementById(id2)).length === 0){
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
                    if(cy.getElementById(id2).length !== 0 &&
                        !cy.getElementById(id2).data("cluster") &&
                        cy.getElementById(id3).length !== 0 &&
                        !cy.getElementById(id3).data("cluster") &&
                        cy.getElementById(id3).edgesWith(cy.getElementById(id2)).length === 0){
                        cy.add({group: 'edges',
                            data: {
                                source: id2, target: id3,
                                detectionMethod: element._fields[3].properties.detectionMethod,
                                interactionType: element._fields[3].properties.interactionType,
                                pubmedId: element._fields[3].properties.pubmedId,
                                dataSource: element._fields[3].properties.dataSource,
                                reliabilityScore: element._fields[3].properties.reliabilityScore
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

                //Set circular layout for nodes added
                var layout = nodescollection.layout({
                    name: 'circle',
                    fit: false,
                    boundingBox: { x1:xc-28, y1:yc-28, x2:xc+28, y2:yc+28 }
                });
                layout.run();
                nodescollection.style('z-index-compare','manual');

                //Update events on the elements of the graph
                cy.nodes().removeAllListeners();
                cy.edges().removeAllListeners();
                mouseovernodehandler();
                mouseoutnodehandler();
                mouseclicksinglenode();
                mouseclickclusternode();
                mouseoveredgehandler();
                mouseoutedgehandler();
                nodesvisibility();
                colornodes();
                resizenodes();

                document.getElementById("loader").style.visibility = "hidden";
            })

    });
}
mouseclickclusternode();

//On click single node event
function mouseclicksinglenode(){
    cy.nodes('[!cluster]').on('click', function(evt){
        if(evt.target.connectedEdges().size() > 0){

            //Check if already clicked
            if(clickednodes.contains(evt.target)){
                clickednodes = clickednodes.difference(evt.target);
                evt.target.connectedEdges().difference(subsetsideedges).difference(clickednodes.connectedEdges()).style("display","none");
            }
            else{
                clickednodes = clickednodes.union(evt.target);

                //Select edges to show
                evt.target.connectedEdges().filter(function( ele ){
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
                        return false;
                    }
                }).style("display","element");
            }
            updatestats();
        }
    });
}
mouseclicksinglenode();

//On mouse over node event
var tooltipnode;
function mouseovernodehandler(){
    cy.nodes().on('mouseover', function(evt){
        tooltipnode = setTimeout(function(){

            //Create tooltip
            var tooltip = evt.target.popper({
                content: () => {
                    var div = document.createElement('div');
                    var tab = document.createElement('table');
                    var tr = document.createElement('tr');
                    var th1 = document.createElement('th');
                    var th2 = document.createElement('th');
                    var img1 = document.createElement("img");
                    var img2 = document.createElement("img");

                    th1.innerText = "ID";
                    th2.innerText = "Degree";
                    th1.onclick = sortTableTooltip1.bind(this,tab,img1,img2);
                    th2.onclick = sortTableTooltip2.bind(this,tab,img1,img2);

                    img1.src = "style/greenarrow.png";
                    img1.width = 10;
                    img1.height = 10;
                    img2.src = "style/greenarrow.png";
                    img2.width = 10;
                    img2.height = 10;
                    img2.style.visibility= "hidden";

                    th1.appendChild(img1);
                    th2.appendChild(img2);
                    tr.appendChild(th1);
                    tr.appendChild(th2);
                    tab.appendChild(tr);

                    //Check if cluster or single node
                    if(evt.target.data("cluster")){
                        div.className = "target-popper-cluster";
                        var start = document.createElement("div");
                        start.id = "start"+evt.target.id();

                        var sizenodes = evt.target.data("nodes").length;
                        var divhead = document.createElement("div");
                        var hr = document.createElement("hr");
                        var divmin = document.createElement("div");

                        divhead.innerHTML = "<u><b>CLUSTER</b></u><br>Number of nodes: " + sizenodes +
                            "<br>Internal edges: "+evt.target.data("internalEdges")+
                            "<br>External edges: "+evt.target.data("externalEdges");

                        divhead.style.display = "inline-block";
                        divmin.style.display = "inline-block";

                        div.appendChild(start);
                        div.appendChild(divhead);
                        div.appendChild(divmin);
                        div.appendChild(hr);
                        div.appendChild(tab);

                        var sorted = [...evt.target.data("nodes")].sort();
                        var datadegree = [];
                        sorted.forEach(el => {
                            var tr = document.createElement('tr');
                            var td1 = document.createElement('td');
                            var td2 = document.createElement('td');
                            td1.innerText = el;
                            td2.innerText = centralityfile.find(x => x.id === el).centrality;
                            tr.appendChild(td1);
                            tr.appendChild(td2);
                            tab.appendChild(tr);
                            var tuple = {id: td1.innerText, centrality: parseInt(td2.innerText)};
                            datadegree.push(tuple);
                        });
                        datadegree.sort((a,b) => (a.centrality < b.centrality) ? 1 : ((b.centrality < a.centrality) ? -1 : 0));
                        var hr = document.createElement("hr");
                        div.appendChild(hr);
                        writedistr(div,datadegree,start.id);
                        writedistrmin(divmin,datadegree);
                        var end = document.createElement("div");
                        end.id = "end"+evt.target.id();
                        div.appendChild(end);
                        divmin.onclick = function (){
                            window.location.href = "#"+end.id;
                        };
                    }
                    else{
                        div.className = "target-popper";
                        div.innerHTML = "<u><b>GENE</b></u><br>" +
                            "<b>Uniprot id: </b>"+evt.target.data("uniprotId")+"<br>"+
                            "<b>Entrez gene id: </b>"+evt.target.data("entrezGeneId")+"<br>"+
                            "<b>Ensembl id: </b>"+evt.target.data("ensemblId")+"<br>"+
                            "<b>Hgnc symbol: </b>"+evt.target.data("hgncSymbol") +"<br>"+
                            "<b>Degree: </b>"+centralityfile.find(x => x.id === evt.target.id()).centrality;
                    }
                    document.body.appendChild(div);

                    return div;
                },
                popper: {placement: "bottom"}
            });

            //On out event
            let destroy = () => {
                tooltip.destroy();
            };
            let update = () => {
                tooltip.forceUpdate();
            };
            evt.target.on('mouseout', destroy);
            evt.target.on('position', update);
            cy.on('pan zoom resize', update);


        }, 1000);
    });
}
mouseovernodehandler();

//On mouse out node event
function mouseoutnodehandler(){
    cy.nodes().on('mouseout', function(evt){
        clearTimeout(tooltipnode);
    });
}
mouseoutnodehandler();

//On mouse over edge event
var tooltipedge;
function mouseoveredgehandler(){
    cy.edges().on('mouseover', function(evt){

        //Create tooltip
        tooltipedge = setTimeout(function (){
            var tooltip = evt.target.popper({
                content: () => {
                    var div = document.createElement('div');
                    div.className = "target-popper-edge";
                    div.innerHTML = "<u><b>INTERACTION</b></u><br>" +
                        "<b>Gene A: </b>"+evt.target.data("source").replace(/\|/g, ' | ')+"<br>"+
                        "<b>Gene B: </b>"+evt.target.data("target").replace(/\|/g, ' | ')+"<br>"+
                        "<b>Detection method: </b>"+evt.target.data("detectionMethod").replace(/\|/g, ' | ')+"<br>"+
                        "<b>Interaction type: </b>"+evt.target.data("interactionType").replace(/\|/g, ' | ') +"<br>"+
                        "<b>Pubmed ID: </b>"+evt.target.data("pubmedId").replace(/\|/g, ' | ') +"<br>"+
                        "<b>Data source: </b>"+evt.target.data("dataSource").replace(/\|/g, ' | ') +"<br>"+
                        "<b>Reliability score: </b>"+evt.target.data("reliabilityScore");

                    document.body.appendChild(div);

                    return div;
                },
                renderedPosition: () => (evt.renderedPosition),
                popper: {}
            });

            let destroy = () => {
                tooltip.destroy();
            };
            let update = () => {
                tooltip.forceUpdate();
            };
            evt.target.on('mouseout', destroy);
            evt.target.on('position', update);
            cy.on('pan zoom resize', update);
        }, 1000);
    });
}
mouseoveredgehandler();

//On mouse out edge event
function mouseoutedgehandler(){
    cy.edges().on('mouseout', function(evt){
        clearTimeout(tooltipedge);
    });
}
mouseoutedgehandler();

//On zoom event
cy.on('zoom', function(evt){
    document.getElementById("focus").style.width =
        ((cy.extent().w * initialwidthmap) / initialextent.w) + "px";
    document.getElementById("focus").style.height =
        ((cy.extent().h * initialheightmap) / initialextent.h) + "px";
    document.getElementById("focus").style.left =
        (((cy.extent().x1 - initialextent.x1) / initialextent.w)*100) + "%";
    document.getElementById("focus").style.right =
        (((initialextent.x2 - cy.extent().x2) / initialextent.w)*100) + "%";
    document.getElementById("focus").style.top =
        (((cy.extent().y1 - initialextent.y1) / initialextent.h)*100) + "%";
    document.getElementById("focus").style.bottom =
        (((initialextent.y2 - cy.extent().y2) / initialextent.h)*100) + "%";
});

//On pan event
cy.on('pan', function(evt){
    document.getElementById("focus").style.width =
        ((cy.extent().w * initialwidthmap) / initialextent.w) + "px";
    document.getElementById("focus").style.height =
        ((cy.extent().h * initialheightmap) / initialextent.h) + "px";
    document.getElementById("focus").style.left =
        (((cy.extent().x1 - initialextent.x1) / initialextent.w)*100) + "%";
    document.getElementById("focus").style.right =
        (((initialextent.x2 - cy.extent().x2) / initialextent.w)*100) + "%";
    document.getElementById("focus").style.top =
        (((cy.extent().y1 - initialextent.y1) / initialextent.h)*100) + "%";
    document.getElementById("focus").style.bottom =
        (((initialextent.y2 - cy.extent().y2) / initialextent.h)*100) + "%";
});

//Sorting tooltip func
function sortTableTooltip1(table,img1,img2) {
    var rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    switching = true;
    // Set the sorting direction to ascending:
    dir = "asc";
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /* Loop through all table rows (except the
        first, which contains table headers): */
        for (i = 1; i < (rows.length - 1); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare,
            one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[0];
            y = rows[i + 1].getElementsByTagName("TD")[0];
            /* Check if the two rows should switch place,
            based on the direction, asc or desc: */
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch
            and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // Each time a switch is done, increase this count by 1:
            switchcount ++;
        } else {
            img1.style.visibility = "visible";
            img2.style.visibility = "hidden";
            if(dir == "asc"){
                img1.src = "style/greenarrow.png";
            }
            else {
                img1.src = "style/redarrow.png";
            }
            /* If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again. */
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}
function sortTableTooltip2(table,img1,img2) {
    var rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    switching = true;
    // Set the sorting direction to ascending:
    dir = "asc";
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /* Loop through all table rows (except the
        first, which contains table headers): */
        for (i = 1; i < (rows.length - 1); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare,
            one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[1];
            y = rows[i + 1].getElementsByTagName("TD")[1];
            /* Check if the two rows should switch place,
            based on the direction, asc or desc: */
            if (dir == "asc") {
                if (Number(x.innerHTML) > Number(y.innerHTML)) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (Number(x.innerHTML) < Number(y.innerHTML)) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch
            and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // Each time a switch is done, increase this count by 1:
            switchcount ++;
        } else {
            img1.style.visibility = "hidden";
            img2.style.visibility = "visible";
            if(dir == "asc"){
                img2.src = "style/greenarrow.png";
            }
            else {
                img2.src = "style/redarrow.png";
            }
            /* If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again. */
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

//Write distribution func
function writedistr(div,data,startdiv){

    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 0, bottom: 10, left: 40},
        width = 290 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    d3.select("#tooltipdistribution").select("svg").remove();
    var svg = d3.select('#tooltipdistribution')
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    //title
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", (0 + margin.top))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .style("fill", "white")
        .text("Degree distribution");

    //Up button
    svg.append("svg:image")
        .attr("class","upbutton")
        .attr("x", (width - margin.left))
        .attr("y", 0)
        .attr("width", 60)
        .attr("height", 20)
        .attr("xlink:href", "style/up.png")
        .on("click", function(){
            window.location.href = "#"+startdiv;
        });

    // Add X axis
    var x = d3.scaleBand()
        .domain(data.map(function(d) { return d.id; }))
        .range([ 0, width ]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickValues([]));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return +d.centrality; })])
        .range([ height, 0 ]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // Add the area
    svg.append("path")
        .datum(data)
        .attr("fill", "#cce5df")
        .attr("stroke", "#69b3a2")
        .attr("stroke-width", 1.5)
        .attr("d", d3.area()
            .x(function(d) { return x(d.id) })
            .y0(y(0))
            .y1(function(d) { return y(d.centrality) })
        )

    svg.selectAll("dot")
        .data(data)
        .enter().append("circle")
        .attr("r", 2.5)
        .attr("class","dotdegreedistr")
        .attr("fill","blue")
        .attr("cx", function(d) { return x(d.id); })
        .attr("cy", function(d) { return y(d.centrality); })
        .on("mouseover", function(d) {
            svg.append("text")
                .attr("class","infocircle")
                .attr("x", (width / 5))
                .attr("y", (0 + margin.top+25))
                .style("font-size", "12px")
                .style("fill", "white")
                .text("Id: "+d.id);
            svg.append("text")
                .attr("class","infocircle")
                .attr("x", (width / 5))
                .attr("y", (0 + margin.top+40))
                .style("font-size", "12px")
                .style("fill", "white")
                .text("Degree: "+d.centrality);
        })
        .on("mouseout", function() {
            svg.selectAll(".infocircle").remove()
        });

    div.appendChild(document.getElementById("tooltipdistribution"));
}

function writedistrmin(div,data){

    // set the dimensions and margins of the graph
    var margin = {top: 5, right: 0, bottom: 5, left: 15},
        width = 160 - margin.left - margin.right,
        height = 65 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    d3.select("#tooltipdistributionmin").select("svg").remove();
    var svg = d3.select('#tooltipdistributionmin')
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Add X axis
    var x = d3.scaleBand()
        .domain(data.map(function(d) { return d.id; }))
        .range([ 0, width ]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickValues([]));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return +d.centrality; })])
        .range([ height, 0 ]);
    svg.append("g")
        .call(d3.axisLeft(y).tickValues([]));

    // Add the area
    svg.append("path")
        .datum(data)
        .attr("fill", "#cce5df")
        .attr("stroke", "#69b3a2")
        .attr("stroke-width", 1.5)
        .attr("d", d3.area()
            .x(function(d) { return x(d.id) })
            .y0(y(0))
            .y1(function(d) { return y(d.centrality) })
        )

    div.appendChild(document.getElementById("tooltipdistributionmin"));
}

