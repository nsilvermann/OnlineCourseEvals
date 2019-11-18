//Created by Nathan Silverman on 10/15/19
//this function is called on load of page
function doFirst() {
    document.getElementById("button").addEventListener("click", validate);
    //loads the data from the prevous pages
    var cList=JSON.parse(sessionStorage.courses);
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
    //loads the data from the prevous pages
    var name=sessionStorage.teacherName;
    var email=sessionStorage.teacherEmail;
    var e= document.getElementById("inputGroupSelect01");
    var inputCourse = e.options[e.selectedIndex].text;
    //saves the course selection unless its null or Choose... 
    if (!(inputCourse === "" | inputCourse ==="Choose..." )){
        sessionStorage.selectedCourse = JSON.stringify(inputCourse);
        info=[name,inputCourse,email];
        fetchCourses(info);
        newLocation();
    }
}
//Calls sendData()
async function fetchCourses(answers) {
    const response = await sendData('/api/sendResponses', answers);
} 
//loads the new page 
function newLocation() {
    window.location="http://127.0.0.1:5500/static/teacherEnd.html";
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

