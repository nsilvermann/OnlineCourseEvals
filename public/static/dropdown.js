//Created by Nathan Silverman on 10/15/19
//this function is called on load of page
function doFirst() {
    //Button listener 
    document.getElementById("button").addEventListener("click", validate);
    //loads sid and courses
    var oldSid=sessionStorage.sid;
    var cList=JSON.parse(sessionStorage.courses);
    //console.log(cList);
    //console.log(oldSid);
    var select = document.getElementById("inputGroupSelect01"); 
    //populates the drop down menu with the courses
    for(var i = 0; i < cList.length; i++) {
        var opt = cList[i];
        var el = document.createElement("option");
        el.text = opt;
        el.value = opt;
        select.add(el);
    }

}
window.addEventListener("load", doFirst, false);

//Called when the button is clicked
function validate() {
    //gets the selection from the drop down menu
    var e= document.getElementById("inputGroupSelect01");
    var inputCourse = e.options[e.selectedIndex].text;
    //saves the course selection unless its null or Choose... 
    if (!(inputCourse === "" | inputCourse ==="Choose..." )){
        sessionStorage.selectedCourse = JSON.stringify(inputCourse);
        newLocation();
    }
}

//loads the new page 
function newLocation() {
    console.log("in newLocation");
    window.location="http://127.0.0.1:5500/static/questionsWithcomments.html";
}

//sendData communicates with the backend
async function sendData(url, data) {
    const response = await fetch(url,
        {
            method: 'POST',
            headers: {
                "content-type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );
    return await response.json();
}
