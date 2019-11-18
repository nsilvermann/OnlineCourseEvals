# Created by Nathan Silverman on 9/15/2019
# The main function of this file is to populate the database
from __future__ import print_function
from httplib2 import Http
import pandas as pd
import numpy as np
import pyexcel as p
import sqlite3
import json
from flask import Flask, jsonify, g, redirect, request, url_for
import http.client


#Initializes global variables 
my_dict = p.get_array(file_name="TestRoster.xlsx", name_columns_by_row=0)
connect = sqlite3.connect('evalDB.db')
cur = connect.cursor()

#main function used for testing and will be called everytime the server starts up 
def main():
	#deleteResponseRow(1)

	#dropTableStatement = "DROP TABLE Responses"
	#cur.execute(dropTableStatement)
	# cur.execute("CREATE TABLE Courses(CourseId    INTEGER PRIMARY KEY, Term  TEXT NOT NULL, CourseName  TEXT NOT NULL, Section  TEXT NOT NULL, Instructor INTEGER NOT NULL, FOREIGN KEY(Instructor) REFERENCES Instructors(InstructorID));")
	# cur.execute("CREATE TABLE Instructors(InstructorID    INTEGER PRIMARY KEY AUTOINCREMENT, Name  TEXT NOT NULL, Email  TEXT NOT NULL);")
	# cur.execute("CREATE TABLE Students(ID INTEGER PRIMARY KEY, StudentID  INTEGER NOT NULL, Email  TEXT NOT NULL );")
	#cur.execute("CREATE TABLE Classes(ClassID INTEGER PRIMARY KEY, StudentID  INTEGER NOT NULL, Course  INTEGER NOT NULL, EvalStatus  INTEGER DEFAULT 0, FOREIGN KEY(StudentID) REFERENCES Students(StudentID) FOREIGN KEY(Course) REFERENCES Courses(CourseId) );")
	#cur.execute("CREATE TABLE Responses(ResponseID INTEGER PRIMARY KEY,studentInCourseID, CourseName, year, courseType, a1,a2,a3,a4,a5,a6,a7,a8,c1,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,c2,a20,a21,c3,a22,a23,c4,a24,a25,c5);")
	#connect.commit()
	# dropTableStatement = "DROP TABLE Eval"
	# cur.execute(dropTableStatement)

	#cur.execute("CREATE TABLE Eval(EvalID INTEGER PRIMARY KEY, classID  INTEGER NOT NULL, EvalStatus  INTEGER DEFAULT 0, FOREIGN KEY(classID) REFERENCES Classes(ClassID));")

	# r=[2, '2019FA TEST-101 2', 2, 4, 2, 1, 5, 3, 1, 5, 'Comment 1', 5, 4, 5, 4, 4, 4, 3, 4, 2, 4, 1,'Comment 2', 1, 1, 'Comment 3', 5, 3, 'Comment 4', 3, 3, "Comment 5"]
	# print("r: ",r)
	# print("len r: ",len(r))
	#cur.execute("INSERT INTO Responses VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18], r[19], r[20], r[21], r[22], r[23], r[24], r[25], r[26], r[27], r[28, r[29], r[30], r[31]))
	#?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	#cur.execute("INSERT INTO Responses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18], r[19], r[20], r[21], r[22], r[23], r[24], r[25], r[26], r[27], r[28, r[29], r[30], r[31]))
	#for item in r:
	# cur.execute('insert into Responses values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(r))

	addStudents()
	addInstructors()
	addCourse()
	addStudentToClass()
	#changeEvalStatus(555555,0)
	#createEvalList()
	#deleteResponseRow(1)
	#resetAll()
	connect.commit()
	#print(my_dict)

	#Bools to control printing for testing
	printStudents= False
	printInstructors= False
	printCourses= False
	printClasses= False
	printResponses= False

	# print("new student id: ",getNewStudentID(123456))
	# print("get studentinclass id ",getStudentInClassID(my_dict[1][7], getCourseID(str(my_dict[1][0]),str(my_dict[1][1]),str(my_dict[1][2]))))
	# print(getClasses(123456))

	#printing everything in tables for testing 
	if(printStudents):
		cur.execute('SELECT * FROM Students')
		a = cur.fetchall()
		print ("Students ", a)

	if(printInstructors):
		cur.execute('SELECT * FROM Instructors')
		b = cur.fetchall()
		print ("Instructors ", b)

	if(printCourses):
		cur.execute('SELECT * FROM Courses')
		c= cur.fetchall()
		print ("Courses ", c)

	if(printClasses):
		cur.execute('SELECT * FROM Classes')
		d= cur.fetchall()
		print ("Students In Classes ", d)

	if(printResponses):
		cur.execute('SELECT * FROM Responses')
		e= cur.fetchall()
		print ("Responses: ", e)



#Function to fill Students tables from a given class roster.
def addStudents():
	#Iterates through the every student in the class roster
	for i in range(1, len(my_dict)):
		studentID=my_dict[i][7]	#gets the student's ID from the file
		email=my_dict[i][8]	#gets the student's email from the file
		cur.execute('SELECT * FROM Students WHERE StudentID=?', (studentID,)) #checks to make sure the student doesnt already exist
		isStudent = cur.fetchall()
		#if there is not a students with that student id in the database
		if (len(isStudent)==0):
			cur.execute("INSERT INTO Students VALUES (null, ?, ?)", (studentID, email))
		else:	
			print("Student Already Exsists")
			

def addInstructors():
		instructorName=my_dict[1][5]
		email="fake@email.com"
		#print("Instructor name",instructorName)
		cur.execute("SELECT * FROM Instructors WHERE Name=?", (instructorName,))
		isInstructor = cur.fetchall()
		#print(isInstructor)
		if len(isInstructor)==0:	
			cur.execute("INSERT INTO Instructors VALUES (null, ?, ?)", (instructorName, email))
			#cur.execute("DELETE FROM Instructors WHERE email LIKE 'fake@email.com'")
		else:
			print("Instructor Already Exsists")

		# cur.execute('SELECT * FROM Instructors')
		# data_5 = cur.fetchall()
		# print ("Instructors ", data_5)
			
def addCourse():
	for i in range(1, len(my_dict)):
		Term= str(my_dict[i][0])
		CourseName= str(my_dict[i][1])
		Section= str(my_dict[i][2])
		instructorName=my_dict[i][5]
		cur.execute("SELECT * FROM Instructors WHERE Name=?", (instructorName,))
		InstructorID = cur.fetchall()[0]

		cur.execute("SELECT * FROM Courses WHERE Section=? AND CourseName=? AND Term=?", (Section, CourseName, Term,))
		isClass = cur.fetchall()
		#print("class info: ", isClass)
		if len(isClass)==0:
			#print(Term, CourseName, instructorName, InstructorID[0])
			cur.execute("INSERT INTO Courses VALUES (null, ?, ?, ?, ?)", (Term, CourseName, Section, InstructorID[0]))

		print("Course Already Exsists")


def getCourseID(t, c ,s):
	Term= str(t)
	CourseName= str(c)
	Section= str(s)
	#print("input ",Term,CourseName,Section)

	cur.execute("SELECT * FROM Courses WHERE Section=? AND CourseName=? AND Term=?", (Section, CourseName, Term,))
	isCourse= cur.fetchall()
	#print("Course Info: ",isCourse)
	if len(isCourse)!=0:
		#print("course ID: ",isCourse[0][0])
		return isCourse[0][0]
	else:
		print("No Course Found")
		return

def getNewStudentID(idnum):
	sid= idnum

	cur.execute('SELECT * FROM Students WHERE StudentID=?', (sid,))	
	isStudent= cur.fetchall()
	#print("Course Info: ",isCourse)
	if len(isStudent)!=0:
		#print("course ID: ",isCourse[0][0])
		return isStudent[0][0]
	else:
		print("No Student Found")
		return

def getStudentInClassID(idnum,courseID):
	sid= idnum
	c=courseID
	cur.execute('SELECT * FROM Classes WHERE StudentID=? AND Course=?', (sid,c))	
	found= cur.fetchall()
	#print("Course Info: ",isCourse)
	if len(found)!=0:
		#print("course ID: ",isCourse[0][0])
		return found[0][0]
	else:
		print("Student Not In Class")
		return


def changeEvalStatus(studentID,classID):
	sid=studentID
	cid=classID
	cur.execute('SELECT * FROM Classes WHERE StudentID=? AND Course=?', (sid,cid))	
	temp=cur.fetchall()
	if (len(temp)!=0 & temp[0][3]==0):
		cur.execute('UPDATE Classes SET EvalStatus = 1 WHERE StudentID=? AND Course=?', (sid,cid))
		print("Eval Status changed")
	else:
		print("EvalStatus Not Changed")


def addStudentToClass():
	for i in range(1, len(my_dict)):
		studentID=my_dict[i][7]
		Term= str(my_dict[i][0])
		CourseName= str(my_dict[i][1])
		Section= str(my_dict[i][2])
		coID=getCourseID(Term,CourseName,Section)

		#print("course ID: ",coID)
		#print("Student ID", studentID)
		cur.execute("SELECT * FROM Classes WHERE StudentID=? AND Course=?", (studentID, coID,))
		inClass= cur.fetchall()
		#print("In Class: ",inClass)
		if len(inClass)==0:
			cur.execute("INSERT INTO Classes VALUES (null, ?, ?, 0)", (studentID, coID))
			# print("Student Already In Class")

def getClasses(sid):
	cur.execute("SELECT * FROM Classes WHERE StudentID=?", (sid,))
	sidClasses= cur.fetchall()
	classList=[]
	if(sidClasses!=0):
		for i in range(len(sidClasses)):
			temp=sidClasses[i]
			#print(temp)
			cur.execute("SELECT * FROM Courses WHERE CourseId=?", (temp[2],))
			a= cur.fetchall()
			#print(a)
			classList.append(a)
		return classList
	return None

def deleteResponseRow(rowID):
	#print("rowID: ",rowID)
	cur.execute("DELETE FROM Responses WHERE ResponseID=?", (rowID,))
	connect.commit()

def validSID(sid):
	cur.execute("SELECT * FROM Students WHERE StudentID=?", (sid,))
	isStudent= cur.fetchall()
	if(len(isStudent)!=0):
		return True
	else:
		return False

#Resets all entries and eval statuses
def resetAll():
	cur.execute('SELECT * FROM Classes')
	everyone=cur.fetchall()
	print("everyone: ",everyone)
	for i in range(len(everyone)):
		resetEvalStatusSID(everyone[i][1])
	cur.execute('SELECT * FROM Classes')
	reset=cur.fetchall()
	print("reset: ",reset)
	cur.execute('SELECT * FROM Responses')
	p=cur.fetchall()
	print("all responses: ",p)
	for j in range(len(p)):
		deleteResponseRow(j+1)
	cur.execute('SELECT * FROM Responses')
	q=cur.fetchall()
	print("reset responses: ",q)

#Resets the eval status of one student using student id
def resetEvalStatusSID(sid):
	cur.execute('UPDATE Classes SET EvalStatus = 0 WHERE StudentID=?', (sid,))
	connect.commit()
	print("Eval Status changed")
	

main()





