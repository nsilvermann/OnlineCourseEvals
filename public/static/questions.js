//Created by Nathan Silverman on 10/15/19
//this function is called on load of page
function doFirst() {
    document.getElementById("submit").addEventListener("click", combineQuestions);
}
window.addEventListener("load", doFirst, false);

//puts the answers form all the questions in a list
function combineQuestions() {
    //loads all the data from the old pages
    var oldSid=sessionStorage.sid;
    var courseString=JSON.parse(sessionStorage.selectedCourse);
    
    //gets all the answers from the webpage
    var y=yearAtK();
    var courseT=courseType();
    var a1= oneQuestion();
    var a2= twoQuestion();
    var a3= threeQuestion();
    var a4= fourQuestion();
    var a5= fiveQuestion();
    var a6= sixQuestion();
    var a7= sevenQuestion();
    var a8= eightQuestion();
    var c1=document.getElementById("comment1").value;
    var a9= nineQuestion();
    var a10= tenQuestion();
    var a11= elevenQuestion();
    var a12= twelveQuestion();
    var a13= thirteenQuestion();
    var a14= fourteenQuestion();
    var a15= fifteenQuestion();
    var a16= sixteenQuestion();
    var a17= seventeenQuestion();
    var a18= eighteenQuestion();
    var a19= nineteenQuestion();
    var c2=document.getElementById("comment2").value;
    var a20= twentyQuestion();
    var a21= twentyoneQuestion();
    var c3=document.getElementById("comment3").value;
    var a22= twentytwoQuestion();
    var a23= twentythreeQuestion();
    var c4=document.getElementById("comment4").value;
    var a24= twentyfourQuestion();
    var a25= twentyfiveQuestion();
    var c5=document.getElementById("comment5").value;
    //Puts all the aswers in a list and calls sendAnswers() with it
    var answerList = [oldSid,courseString, y, courseT, a1,a2, a3,a4,a5,a6,a7,a8,c1,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,c2,a20,a21,c3,a22,a23,c4,a24,a25,c5];
    sendAnswers(answerList);
}

//Sends the answers to the data base
async function sendAnswers(answers) {
    console.log(answers);
    //sends the list to the database with sendData() function.
    const response = await sendData('/api/finishedResponse', answers);
    console.log(response);
    newLocation();
} 

//loads the new webpage
function newLocation() {
    console.log("in newLocation");
    window.location="http://127.0.0.1:5500/static/thanks.html";
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

