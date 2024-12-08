//Load centrality data
var centralityfile = JSON.parse(loadFile('nodejsserver/centrality.txt'));

//Data
let ordinals = []
Object.entries(centralityfile).forEach(([key, value]) => {
    ordinals.push(value.hgncSymbol)
});


//Dimensions
let margin = {
        top: 0,
        right: 100,
        bottom: 10,
        left: 50
    },
    width = 480 - margin.left - margin.right,
    height = 180 - margin.top - margin.bottom,
    radius = (Math.min(width, height) / 2) - 10,
    node

//Svg
const svg = d3.select('#degreedistribution')
    .append('svg')
    .attr('width', 960)
    .attr('height', 700)
    .append('g')
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    .call(
        d3.zoom()
            .translateExtent([[0,0], [width, height]])
            .extent([[0, 0], [width, height]])
            .on('zoom', zoom)
    )

// Scale
let x = d3.scaleLinear().range([0, width])
let y = d3.scaleLinear().range([height, 0])
let xScale = x.domain([-1, ordinals.length])
let yScale = y.domain([0, d3.max(centralityfile, function(d){return d.centrality})])
// for the width of rect
let xBand = d3.scaleBand().domain(d3.range(-1, ordinals.length)).range([0, width])

// Zoomable rect
svg.append('rect')
    .attr('class', 'zoom-panel')
    .attr('width', width)
    .attr('height', height)

// X axis
let xAxis = svg.append('g')
    .attr('class', 'xAxis')
    .attr("transform", "translate(0," + height + ")")
    .call(
        d3.axisBottom(xScale).tickFormat((d, e) => {
            return ordinals[d]
        })
    )

// Y axis
let yAxis = svg.append('g')
    .attr('class', 'yAxis')
    .call(d3.axisLeft(yScale))

// Bars
let bars = svg.append('g')
    .attr('clip-path','url(#my-clip-path)')
    .selectAll('.bar')
    .data(centralityfile)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr("fill", "rgba(26, 140, 255, 1)")
    .style("opacity",1)
    .attr('x', function(d, i){
        return xScale(i) - xBand.bandwidth()*0.9/2
    })
    .attr('y', function(d, i){
        return yScale(d.centrality)
    })
    .attr('width', xBand.bandwidth()*0.9)
    .attr('height', function(d){
        return height - yScale(d.centrality)
    })

let defs = svg.append('defs')

// ClipPath
defs.append('clipPath')
    .attr('id', 'my-clip-path')
    .append('rect')
    .attr('width', width)
    .attr('height', height)

let hideTicksWithoutLabel = function() {
    d3.selectAll('.xAxis .tick text').each(function(d){
        if(this.innerHTML === '') {
            this.parentNode.style.display = 'none'
        }
    })
}

// Zoom
function zoom() {
    console.log(d3.event.transform.k);
    if (d3.event.transform.k < 1) {
        d3.event.transform.k = 1
        return
    }
    if (d3.event.transform.k > 4700) {
        d3.event.transform.k = 4700
        return
    }

    xAxis.call(
        d3.axisBottom(d3.event.transform.rescaleX(xScale)).tickFormat((d, e, target) => {
            // has bug when the scale is too big
            if (Math.floor(d) === d3.format(".1f")(d)) return ordinals[Math.floor(d)]
            return ordinals[d]
        })
    )

    hideTicksWithoutLabel()

    // the bars transform
    bars.attr("transform", "translate(" + d3.event.transform.x+",0)scale(" + d3.event.transform.k + ",1)")
}




