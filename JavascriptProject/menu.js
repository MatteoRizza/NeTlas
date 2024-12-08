//Initial state
document.getElementById("drugdiv").style.visibility = "hidden";
document.getElementById("diseasediv").style.visibility = "hidden";

//On click dataset menu
document.getElementById("datasetmenu").onclick = function (){
    if(document.getElementById("datasetmenu").className === "active"){
        document.getElementById("datasetmenu").className = "";
        document.getElementById("filters").style.visibility = "hidden";
    }
    else {
        document.getElementById("datasetmenu").className = "active";
        document.getElementById("drugmenu").className = "";
        document.getElementById("diseasemenu").className = "";
        document.getElementById("drugdiv").style.visibility = "hidden";
        document.getElementById("diseasediv").style.visibility = "hidden";
        document.getElementById("filters").style.visibility = "visible";
    }
};

//On click drug menu
document.getElementById("drugmenu").onclick = function (){
    if(document.getElementById("drugmenu").className === "active"){
        document.getElementById("drugmenu").className = "";
        document.getElementById("drugdiv").style.visibility = "hidden";
    }
    else {
        document.getElementById("datasetmenu").className = "";
        document.getElementById("drugmenu").className = "active";
        document.getElementById("diseasemenu").className = "";
        document.getElementById("filters").style.visibility = "hidden";
        document.getElementById("diseasediv").style.visibility = "hidden";
        document.getElementById("drugdiv").style.visibility = "visible";
    }
};

//On click disease menu
document.getElementById("diseasemenu").onclick = function (){
    if(document.getElementById("diseasemenu").className === "active"){
        document.getElementById("diseasemenu").className = "";
        document.getElementById("diseasediv").style.visibility = "hidden";
    }
    else {
        document.getElementById("datasetmenu").className = "";
        document.getElementById("drugmenu").className = "";
        document.getElementById("diseasemenu").className = "active";
        document.getElementById("drugdiv").style.visibility = "hidden";
        document.getElementById("filters").style.visibility = "hidden";
        document.getElementById("diseasediv").style.visibility = "visible";
    }
};