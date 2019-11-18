//Created by Nathan Silverman on 10/15/19
//this function is called on load of page
function doFirst() {
    document.getElementById("but").addEventListener("click", validate);
}
window.addEventListener("load", doFirst, false);

//Onclick load the first page
function validate() {
    newLocation
}

function newLocation() {
    console.log("in newLocation");
    window.location="http://127.0.0.1:5500/static/teacher.html";
}