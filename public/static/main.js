//Created by Nathan Silverman on 10/15/19
//With assistance from Doug Shipp 
//this function is called on load of page
function doFirst() {
    document.getElementById("button").addEventListener("click", validate);
}
window.addEventListener("load", doFirst, false);

//Called when button clicked
function validate() {
    //gets student id value from page 
    var inputId = document.getElementById("idNum").value;
    console.log(inputId);
    //gets the courses the ID is in 
    fetchCourses(inputId);
    
}

//calls send data and newLocation. sid= Student Id Number
async function fetchCourses(sid) {
    //gets all courses that the student id is registerd in and has not taken eval for 
    const response = await sendData('/api/courses', sid);
    console.log(response);
    //Doesn't allow user to proceed to a new page if invalid id or if they don't have any evals to take 
   // if (!(response === "errorMessage")){
    if (!(response === "Invalid Student ID Number" || response ==="No Evals To Take")){
        newLocation(sid,response);
    }
    else{
        //Puts Error Messages On Screen
        var result_display = document.getElementById('error');
        //result_display.innerHTML = "Either Invalid Student ID or You Have No Evals To Take";
        result_display.innerHTML = response;
    }
} 
//Loads new page
function newLocation(sid,courses) {
    //session stores the student id number and courses so they can be accessed in the next file
    sessionStorage.sid = sid;
    sessionStorage.courses = JSON.stringify(courses);
    window.location="http://127.0.0.1:5500/static/dropdown.html";
}
//sendData communicates with the backend
async function sendData(url, data) {
    //console.log(url);
    //console.log(data);
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

