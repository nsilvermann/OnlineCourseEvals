# Created by Nathan Silverman on 9/15/2019

from flask import Flask, request, g, render_template, jsonify
from helperFunctions import *
from EvalScript import main

#Initializes flask app
app = Flask(__name__,
	 		static_url_path='/static', 
            static_folder='static')
app.config["DEBUG"] = True
DATABASE = 'evalDB.db'

#Listens to /courses and reponds to POST or GET calls
@app.route("/api/courses", methods=["POST","GET"])
def getCoruses():
    #parses json information
    requestBody= request.get_json()
    sid=requestBody[0:len(requestBody)]
    #if the student id is valid
    if(validSID(sid)):
        #getValidClasses() returns the list of valid courses or false
        courses= getValidClasses(sid)
        #if courses not flase
        if(courses):
            #returns a jsonified list of courses 
            return jsonify(courses)
        else:
    #Returns error messages if if statements return false
            errorMessage="No Evals To Take"
            print(errorMessage)
            return jsonify(errorMessage)
    else:
        errorMessage="Invalid Student ID Number"
        print(errorMessage)
        return jsonify(errorMessage)

#Listens to /finishedResponse and reponds to POSTs
@app.route("/api/finishedResponse", methods=["POST"])
def getRespnse():
    #parses json information
    requestBody= request.get_json()
    answers=requestBody[0:len(requestBody)]
    #stores the list of answers in the database
    Successful=tempstoreResponse(answers)
    returnable="Successful"
    #just returns "Successful"
    return jsonify(returnable)

#Listens to /finishedResponse and reponds to POST & GETs
@app.route("/api/teacher", methods=["POST","GET"])
def getTCoruses():
    #parses json information
    requestBody= request.get_json()
    name=requestBody[0:len(requestBody)]
    #if it is a valid instructor name
    if(validInstructor(name)):
        #gets the instructors id from their name
        inId=getInstructorID(name)
        #getValidClasses() returns the list of valid courses or false
        courseList=getInstructorCourses(inId)
        if(courseList):
            #getValidClasses() returns the list of valid courses or false
            return jsonify(courseList)
        else:
    #Returns error messages if if statements return false
            errorMessage= "Instructor Isn't Teaching Any Classes"
            print(errorMessage)
            return jsonify(errorMessage)
    else:
        errorMessage= "Invalid Instructor Name"
        print(errorMessage)
        return jsonify(errorMessage)
     
#Listens to /sendResponses and reponds to POST & GETs
@app.route("/api/sendResponses", methods=["POST","GET"])
def send():
    #parses json information
    requestBody= request.get_json()
    info=requestBody[0:len(requestBody)]
    #gets course id from the course string
    courseId=getCourseIDFromCourseString(info[1])
    allResponses=returnClassResponses(courseId)
    #returnClassResponses() returns all the respones for a given course or fals 
    if(allResponses):
        createExcelFile(allResponses)
        return jsonify(allResponses)
    else:
        errorMessage= "No Responses Received Yet"
        return jsonify("No Responses Received Yet")


def render_static():
    return render_template('index.html')

#sets port, hostname, and debug
if __name__ == '__main__':
    main()
    app.run(host="localhost", port=5500, debug=True)
