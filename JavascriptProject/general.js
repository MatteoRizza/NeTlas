
//Wait for loading
window.onload = function() {
    document.getElementById("loader").style.visibility = "hidden";
    document.getElementById("black").style.visibility = "hidden";
};

//Connection to the db server
var driver = neo4j.driver(serverurl, neo4j.auth.basic(servername, serverpassword))

//Load function
function loadFile(filePath) {
    var result = null;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", filePath, false);
    xmlhttp.send();
    if (xmlhttp.status===200) {
        result = xmlhttp.responseText;
    }
    return result;
}

//On click stats
document.getElementById("stats").onclick = function(){
    document.getElementById("degreedistribution").style.visibility = "visible";
    document.getElementById("searchgene").style.visibility = "visible";
    document.getElementById("mapcontainer").style.visibility = "hidden";
    document.getElementById("stats").style.visibility = "hidden";
};

//On click close stats
document.getElementById("closestats").onclick = function(){
    document.getElementById("degreedistribution").style.visibility = "hidden";
    document.getElementById("searchgene").style.visibility = "hidden";
    document.getElementById("mapcontainer").style.visibility = "visible";
    document.getElementById("stats").style.visibility = "visible";
};

//On click sidebar
document.getElementById("sidebarbutton").onclick = function(){
    document.getElementById("sidebarcontainer").style.visibility = "visible";
};

//On click close sidebar
document.getElementById("closesidebar").onclick = function(){
    document.getElementById("sidebarcontainer").style.visibility = "hidden";
};

//On click export
document.getElementById("export").onclick = function(){
    document.getElementById("exportcontainer").style.visibility = "visible";
};

//On click close export
document.getElementById("closeexport").onclick = function(){
    document.getElementById("exportcontainer").style.visibility = "hidden";
};
