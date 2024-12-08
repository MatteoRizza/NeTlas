//Initial values
var initnumgenes = cy.nodes('[!cluster]').size();
var initnodesofclusters = 0;
cy.nodes('[?cluster]').forEach(function( ele ){
    initnodesofclusters = initnodesofclusters + ele.data("nodes").length;
});
var initnumtotgenes = initnumgenes + initnodesofclusters;
var initnumclusters = cy.nodes('[?cluster]').size();
var loc = window.location.pathname;
var dir = loc.substring(0, loc.lastIndexOf('/'));
console.log('LOC',loc);
console.log('DIR',dir);
let dbgenes = loadFile('./DatasetsFormatted/gene/genes.csv').split("\n");
let i=0;
dbgenes.forEach(el=>{
    let datasources = el.split(",")[11];
    if(typeof(datasources) === "undefined"){
    }
    else if(datasources.includes("biogrid") && document.getElementById("showbiogrid").checked){
        i = i+1;
    }
    else if(datasources.includes("intact") && document.getElementById("showintact").checked){
        i = i+1;
    }
    else if(datasources.includes("innatedb") && document.getElementById("showinnatedb").checked){
        i = i+1;
    }
    else if(datasources.includes("mint") && document.getElementById("showmint").checked){
        i = i+1;
    }
    else if(datasources.includes("dip") && document.getElementById("showdip").checked){
        i = i+1;
    }
    else if(datasources.includes("matrixdb") && document.getElementById("showmatrixdb").checked){
        i = i+1;
    }
});
var initnumtotedges = i;
var initnumvisualisededges = 0;

//Absolute values
var absnumgenes = initnumtotgenes;
var absnumclusters = initnumclusters;
var absnumtotgenes = initnumtotgenes;
var absnumtotedges = initnumtotedges;
var absnumvisualisededges = initnumtotedges;

//Actual values
var numgenes = initnumgenes;
var numclusters = initnumclusters;
var numtotgenes = initnumtotgenes;
var numtotedges = initnumtotedges;
var numvisualisededges = initnumvisualisededges;

//Update stats function
function updatestats(){
    var pastnumgenes = numgenes;
    var pastnumclusters = numclusters;
    var pastnumtotgenes = numtotgenes;
    var pastnumtotedges = numtotedges;
    var pastnumvisualisededges = numvisualisededges;

    numgenes = cy.nodes('[!cluster]').filter(function( ele ){
        if(ele.style().display === "element"){
            return true;
        }
        else {
            return false;
        }
    }).size();

    numclusters = cy.nodes('[?cluster]').size();

    var nodesofclusters = 0;
    cy.nodes('[?cluster]').forEach(function( ele ){
        nodesofclusters = nodesofclusters + ele.data("nodes").length;
    });
    numtotgenes = numgenes + nodesofclusters;

    let dbgenes = loadFile('./DatasetsFormatted/gene/genes.csv').split("\n");
    let i=0;
    dbgenes.forEach(el=>{
        let datasources = el.split(",")[11];
        if(typeof(datasources) === "undefined"){
        }
        else if(datasources.includes("biogrid") && document.getElementById("showbiogrid").checked){
            i = i+1;
        }
        else if(datasources.includes("intact") && document.getElementById("showintact").checked){
            i = i+1;
        }
        else if(datasources.includes("innatedb") && document.getElementById("showinnatedb").checked){
            i = i+1;
        }
        else if(datasources.includes("mint") && document.getElementById("showmint").checked){
            i = i+1;
        }
        else if(datasources.includes("dip") && document.getElementById("showdip").checked){
            i = i+1;
        }
        else if(datasources.includes("matrixdb") && document.getElementById("showmatrixdb").checked){
            i = i+1;
        }
    });
    numtotedges = i;

    numvisualisededges = cy.edges().filter(function( ele ){
        return ele.style("display") === "element";
    }).size();

    document.getElementById("livestats").innerHTML =
        "<tr><td style='padding-right: 25px'>" +
        "Total genes: <b>" + numtotgenes + "</b> / <b>" + absnumtotgenes +
        " ("+((numtotgenes/absnumtotgenes)*100).toFixed(2)+"%)</b>&nbsp;<img width='12' height='12'></td>" +
        "<td>Total edges: <b>" + numtotedges + "</b> / <b>" + absnumtotedges +
        " ("+((numtotedges/absnumtotedges)*100).toFixed(2)+"%)</b>&nbsp;<img width='12' height='12'></td></tr><tr>"+
        "<td>Single genes: <b>" + numgenes + "</b> / <b>" + absnumgenes +
        " ("+((numgenes/absnumgenes)*100).toFixed(2)+"%)</b>&nbsp;<img width='12' height='12'></td>" +
        "<td>Visualized edges: <b>" + numvisualisededges + "</b> / <b>" + absnumvisualisededges +
        " ("+((numvisualisededges/absnumvisualisededges)*100).toFixed(2)+"%)</b>&nbsp;<img width='12' height='12'></td></tr><tr>" +
        "<td>Clusters: <b>" + numclusters + "</b> / <b>" + absnumclusters +
        " ("+((numclusters/absnumclusters)*100).toFixed(2)+"%)</b>&nbsp;<img width='12' height='12'></td>" +
        "<td></td></tr>";

    if(numtotgenes < pastnumtotgenes){
        document.getElementById('livestats').getElementsByTagName('img')[0].src = "style/redarrow.png";
    }
    else if(numtotgenes > pastnumtotgenes){
        document.getElementById('livestats').getElementsByTagName('img')[0].src = "style/greenarrow.png";
    }
    else{
        document.getElementById('livestats').getElementsByTagName('img')[0].src = "style/equal.png";
    }
    if(numtotedges < pastnumtotedges){
        document.getElementById('livestats').getElementsByTagName('img')[1].src = "style/redarrow.png";
    }
    else if(numtotedges > pastnumtotedges){
        document.getElementById('livestats').getElementsByTagName('img')[1].src = "style/greenarrow.png";
    }
    else{
        document.getElementById('livestats').getElementsByTagName('img')[1].src = "style/equal.png";
    }
    if(numgenes < pastnumgenes){
        document.getElementById('livestats').getElementsByTagName('img')[2].src = "style/redarrow.png";
    }
    else if(numgenes > pastnumgenes){
        document.getElementById('livestats').getElementsByTagName('img')[2].src = "style/greenarrow.png";
    }
    else{
        document.getElementById('livestats').getElementsByTagName('img')[2].src = "style/equal.png";
    }
    if(numclusters < pastnumclusters){
        document.getElementById('livestats').getElementsByTagName('img')[4].src = "style/redarrow.png";
    }
    else if(numclusters > pastnumclusters){
        document.getElementById('livestats').getElementsByTagName('img')[4].src = "style/greenarrow.png";
    }
    else{
        document.getElementById('livestats').getElementsByTagName('img')[4].src = "style/equal.png";
    }
    if(numvisualisededges < pastnumvisualisededges){
        document.getElementById('livestats').getElementsByTagName('img')[3].src = "style/redarrow.png";
    }
    else if(numvisualisededges > pastnumvisualisededges){
        document.getElementById('livestats').getElementsByTagName('img')[3].src = "style/greenarrow.png";
    }
    else{
        document.getElementById('livestats').getElementsByTagName('img')[3].src = "style/equal.png";
    }

}

updatestats();

//Edgegraph function
function edgegraph(data){

    // set the dimensions and margins of the graph
    var margin = {top: 5, right: 5, bottom: 20, left: 25},
        width = 170 - margin.left - margin.right,
        height = 90 - margin.top - margin.bottom;

    d3.select("#edgegraph").select("svg").remove();
    // append the svg object to the body of the page
    var svg = d3.select("#edgegraph")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // X axis
    var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(data.map(function(d) { return d.x; }))
        .padding(0.2);
    svg.append("g")
        .attr('class', 'xAxis')
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

// Add Y axis
    var y = d3.scaleLinear()
        .domain([0, d3.max(data, function(d){return d.y})])
        .range([ height, 0]);
    svg.append("g")
        .attr('class', 'yAxis')
        .call(d3.axisLeft(y).ticks(5));

// Bars
    svg.selectAll("myedgebar")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", function(d) { return x(d.x); })
        .attr("y", function(d) { return y(d.y); })
        .attr("width", x.bandwidth())
        .attr("height", function(d) { return height - y(d.y); })
        .attr("fill", "#69b3a2")
        .on("mouseover", function(d) {
            subsetsideedges.style("display","none");
            if(d.x === "low"){
                subsetsideedges.filter(function( ele ){
                    return ele.data('reliabilityScore') < 0.34;
                }).style("display","element");
            }
            else if(d.x === "high"){
                subsetsideedges.filter(function( ele ){
                    return ele.data('reliabilityScore') > 0.65;
                }).style("display","element");
            }
            else {
                subsetsideedges.filter(function( ele ){
                    return ele.data('reliabilityScore') <= 0.65 && ele.data('reliabilityScore') >= 0.34;
                }).style("display","element");
            }
        })
        .on("mouseout", function() {
            subsetsideedges.style("display","element");
        });

}