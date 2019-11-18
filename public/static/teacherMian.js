//Created by Nathan Silverman on 10/15/19
//With assistance from Doug Shipp 
//this function is called on load of page
function doFirst() {
    document.getElementById("button").addEventListener("click", validate);
}
window.addEventListener("load", doFirst, false);

//Called when button clicked
function validate() {
    //gets the teachers name and email
    var teacherName = document.getElementById("name").value;
    var teacherEmail = document.getElementById("email").value;
    sessionStorage.teacherEmail = teacherEmail;
    console.log(teacherName);
    fetchCourses(teacherName);
}

//calls send data and newLocation.
async function fetchCourses(teacherName) {
    //Sends the teacher's name to the back end and gets all the courses the teacher teaches
    const response = await sendData('/api/teacher', teacherName);
    //Doesn't allow user to proceed to a new page if invalid name or aren't teaching any classes 
    //if (!(response === "errorMessage")){
    if (!(response === "Instructor Isn't Teaching Any Classes" || response ==="Invalid Instructor Name")){
        newLocation(teacherName,response);
    }
    else{
        //Puts Error Messages On Screen
        var result_display = document.getElementById('error');
        //result_display.innerHTML = "Either Invalid Student ID or You Have No Evals To Take";
        result_display.innerHTML = response;
    }
} 

//Loads new page
function newLocation(teacherName,response) {
    //session stores the teacher name and email so they can be accessed in the next file
    sessionStorage.teacherName = teacherName;
    sessionStorage.courses = JSON.stringify(response);
    window.location="http://127.0.0.1:5500/static/teacherSelect.html";
}

//sendData communicates with the backend
async function sendData(url, data) {
    console.log("data sent");
    console.log(url);
    console.log(data);
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

