# Created by Nathan Silverman on 9/15/2019
# With assistance from Danny Henry
import numpy as np
import pyexcel as p
import sqlite3
import xlsxwriter
from datetime import datetime
from EvalScript import main
from xlsxwriter.utility import xl_rowcol_to_cell

#Main function used for testing different methods
def main():
	#a method must have some command inside of it
	print()
	#test respones
	r=[(1, 1, '2019FA TEST-101 1', 'Senior', 'Elective', 1, 2, 1, 5, 4, 1, 2, 1, 'Comment', 5, 4, 4, 2, 2, 1, 1, 3, 3, 1, 5, 'Comment', 4, 2, 'Comment', 3, 5, 'Comment', 3, 2, 'Comment'), (2, 1, '2019FA TEST-101 1', 'Senior', 'Elective', 1, 2, 1, 5, 4, 1, 2, 1, 'Comment', 5, 4, 4, 2, 2, 1, 1, 3, 3, 1, 5, 'Comment', 4, 2, 'Comment', 3, 5, 'Comment', 3, 2, 'Comment'), (3, 1, '2019FA TEST-101 1', 'Junior', 'Requirement', 2, 2, 1, 3, 1, 1, 5, 5, 'c', 1, 5, 4, 3, 3, 1, 1, 4, 3, 2, 4, 'c', 1, 5, 'c', 4, 5, 'c', 2, 1, 'c'),(1, 1, '2019FA TEST-101 1', 'Sophmore', 'Requirement', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ' ', ' ', '', ' ', ' ', '', ' ', ' ', ''), (2, 1, '2019FA TEST-101 1', 'Sophmore', 'Requirement', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ' ', ' ', '', ' ', ' ', '', ' ', ' ', ''), (3, 1, '2019FA TEST-101 1', 'Junior', 'Elective', 5, 5, 3, 1, 3, 2, 2, 3, 'Comment', 5, 5, 4, 4, 5, 2, 1, 5, 5, 1, 5, 'Comment ', 4, 2, 'Comment', 5, 5, 'Comment', 3, 2, 'Comment'), (4, 1, '2019FA TEST-101 1', 'Junior', 'EElectivele', 5, 5, 3, 1, 3, 2, 2, 3, 'Comment', 5, 5, 4, 4, 5, 2, 1, 5, 5, 1, 5, 'Comment ', 4, 2, 'Comment', 5, 5, 'Comment', 3, 2, 'Comment'), (5, 1, '2019FA TEST-101 1', 'Senior', 'EElectivele', 3, ' ', 5, 1, ' ', 5, 3, 1, 'Comment', 2, 4, 4, 2, 1, 1, 1, 5, 5, 4, 5, 'Comment', 2, 1, 'Comment', 5, 5, 'Comment', 4, 1, 'Comment')]
	# for q in r:
	# 	testStore(q)
	#print(testFunction(r))
	#createExcelFile(r)
	#deleteResponseRow(1)
	#resetEvalStatus(1)
	#stestAnswers=[503445, "2019FA TEST-101 1", 0, 1, 2, 3, 4, 5, "I really liked this class", 0, 0, 0, "Word Question" ]
	#blank=["","","","","","","",""]
	#storeResponse(testAnswers)

	#resetEvalStatusSID(503445)
	
	#Prints all respones in database
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute("SELECT * FROM Responses")
	asd= cur.fetchall()
	createExcelFile(asd)
	# print("All stdents in all classes ",asd)
	#getInstructorCourses(1)

	#resetAll()

	#a= getValidClasses(123456)
	#print("getValidClasses: ",a)
	#b= getStudentInClassID(123456,a[0])
	#print("getStudentInClassID ",b)
	#c=hasNotTakenEval(b)
	#print(c)
	#d=getCourseInfo(1)
	#e=getStudentInClassID(123456,"2019FA TEST-101 1")
	#print("getCourseInfo: ",d)
	#print("getStudentInClassID: ",e)



#getValidClasses(StudentIDNuimber)
#Input: student Id number 
#Output: List of all class names the student is in, in one string or false
#Ex.) ['2019FA TEST-101 1'] 
def getValidClasses(sid):
	#connects to database
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	# print("sid: ",sid)
	# print("is valid: ",validSID(sid))
	# cur.execute("SELECT * FROM Classes WHERE StudentID=?", (sid,))
	# b= cur.fetchall()
	# print("all classes: ",b)
	# cur.execute("SELECT * FROM Responses WHERE studentInCourseID=?", (b[0][0],))
	# d= cur.fetchall()
	# print("r: ",d)

	#if the student id is valid
	if(validSID(sid)):
		#gets all instances of the student id in the linker table where the eval status is 0
		cur.execute("SELECT * FROM Classes WHERE StudentID=? AND EvalStatus=?", (sid,0))
		sidClasses= cur.fetchall()
		#print("sidclasses: ",sidClasses)
		classList=[]
		#if there is atleast one instance form classes
		if(len(sidClasses)!=0):
			#for all instances in classes
			for i in range(len(sidClasses)):
				temp=sidClasses[i]
				#gets the course info from the course id
				cur.execute("SELECT * FROM Courses WHERE CourseId=?", (temp[2],))
				courseInfo= cur.fetchall()
				#makes a string from term, course name, and section
				fullClass=" ".join(courseInfo[0][1:4])
				#adds string to list
				classList.append(fullClass)
			return classList
		else:
			print("No Eval's to take")
			return False
	else:
		print("Invalid Student ID")
		return False

# getCourseID(term, course, section)
# Input: A term, course, and section 
# Ex.) 2019FA, TEST-101, 1
# Output: The course ID number or false
def getCourseID(term, course, section):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	Term= str(term)
	CourseName= str(course)
	Section= str(section)
	#gets courses matching Section, CourseName, and Term
	cur.execute("SELECT * FROM Courses WHERE Section=? AND CourseName=? AND Term=?", (Section, CourseName, Term,))
	isCourse= cur.fetchall()
	if len(isCourse)!=0:
		return isCourse[0][0]
	else:
		print("Invalid Course")
		return False

# getCourseID(term, course, section)
# Input: A term, course, and section 
# Ex.) 2019FA, TEST-101, 1
# Output: The course ID number or false
def getCourseIDFromCourseString(courseString):
	listOfClassInfo=courseString.split(' ')
	courseID=getCourseID(listOfClassInfo[0],listOfClassInfo[1],listOfClassInfo[2])
	return courseID

# getCourseInfo(studentInClassID)
# Input: studentInClassID
# Output: All infomation about the given course or false
# Ex.) (1, '2019FA', 'TEST-101', '1', 1)
def getCourseInfo(studentInClassID):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute("SELECT * FROM Courses WHERE CourseId=? ", (studentInClassID,))
	studentincourseInfo= cur.fetchall()
	if len(studentincourseInfo)!=0:
		return studentincourseInfo[0]
	else:
		print("Invalid Course")
		return False

# getStudentInClassID(studentID,courseString)
# Input: Student ID number and the name of course string given to drop down menu
# Ex.) (123456, "2019FA TEST-101 1")
# Output: The row/ID number of the linker table of the student ID and course ID.
def getStudentInClassID(studentID,courseString):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	#splits the course string into Section, CourseName, and Term
	listOfClassInfo=courseString.split(' ')
	courseID=getCourseID(listOfClassInfo[0],listOfClassInfo[1],listOfClassInfo[2])
	cur.execute('SELECT * FROM Classes WHERE StudentID=? AND Course=?', (studentID,courseID))
	isStudentInClass=cur.fetchall()
	if (len(isStudentInClass)!=0):
		return isStudentInClass[0][2]
	else:
		print("Student not registered in that class")
		return False

# validSID(StudentIDNuimber)
# Input: student Id number 
# Output: True or False depending on if the student Id number is in the database.
def validSID(sid):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute("SELECT * FROM Students WHERE StudentID=?", (sid,))
	isStudent= cur.fetchall()
	if(len(isStudent)!=0):
		return True
	else:
		return False

# validInstructor(name)
# Input: Instructor name
# Output: True or False depending on if the student Id number is in the database.
def validInstructor(name):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute("SELECT * FROM Instructors WHERE Name=?", (name,))
	isInstructor= cur.fetchall()
	print(isInstructor)
	if(len(isInstructor)!=0):
		return True
	else:
		return False


# getInstructorID(nameOfInstructor)
# Input: a Name of instructor
# Output: The instructor's database ID number or false.
def getInstructorID(name):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute("SELECT * FROM Instructors WHERE Name=?", (name,))
	instructorInfo= cur.fetchall()
	print(instructorInfo)
	if(len(instructorInfo)!=0):
		inID=instructorInfo[0][0]
		return inID
	else:
		print("Invalid Instructor Name")
		return False

# getInstructorID(nameOfInstructor)
# Input: The instructor's database ID number
# Output: The list of courses the instructor has taught or false.
def getInstructorCourses(instructorID):
	inId=instructorID
	courseList=[]
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	#print("sid: ",sid)
	cur.execute("SELECT * FROM Courses WHERE Instructor=?", (inId,))
	inCourses= cur.fetchall()
	print("inCourses: ",inCourses)
	if(len(inCourses)!=0):
		for i in range(len(inCourses)):
				fullClass=" ".join(inCourses[i][1:4])
				courseList.append(fullClass)

		print("list: ", courseList)
		return courseList
	else:
		print("Invalid Instructor Instructor ID")
		return False


# validStudentInClassId(studentInClassID)
# Input: ID number of the linker table of the student ID and course ID
# Output: True or False depending on if the Id number is in the database.
def validStudentInClassId(studentInClassID):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute("SELECT * FROM Classes WHERE ClassID=?", (studentInClassID,))
	isValid= cur.fetchall()
	if(len(isValid)!=0):
		return True
	else:
		return False


# changeEvalStatus(studentID,courseID):
# Input: Student ID number and Course ID.
# Output: None, it changes the evalStatus from 0 to 1
def changeEvalStatus(studentID,courseID):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	sid=studentID
	cid=courseID
	print("")
	cur.execute('SELECT * FROM Classes WHERE StudentID=? AND Course=?', (sid,cid))	
	temp=cur.fetchall()
	if (len(temp)!=0 & temp[0][3]==0):
		cur.execute('UPDATE Classes SET EvalStatus = 1 WHERE StudentID=? AND Course=?', (sid,cid))
		connect.commit()
		print("Eval Status changed")
	else:
		print("EvalStatus Not Changed")


# changeEvalStatusByClass(studentInClassID)
# Input: The row/ID number of the linker table of the student ID and course ID.
# Output:  None, it changes the evalStatus from 0 to 1
def changeEvalStatusByClass(studentInClassID):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute('SELECT * FROM Classes WHERE ClassID=?', (studentInClassID,))	
	temp=cur.fetchall()
	if (len(temp)!=0):
		cur.execute('UPDATE Classes SET EvalStatus = 1 WHERE ClassID=?', (studentInClassID,))
		connect.commit()
		print("Eval Status changed")
	else:
		print("EvalStatus Not Changed")

# resetEvalStatus(studentInClassID)
# Used for testing purposes.
# Input: The row/ID number of the linker table of the student ID and course ID.
# Output: None, it changes the evalStatus from 1 to 0
def resetEvalStatusSID(sid):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute('UPDATE Classes SET EvalStatus = 0 WHERE StudentID=?', (sid,))
	connect.commit()
	print("Eval Status changed")


#Resets eval status based on a linker table id
def resetEvalStatus(studentInClassID):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute('UPDATE Classes SET EvalStatus = 0 WHERE ClassID=?', (studentInClassID,))
	connect.commit()
	print("Eval Status changed")

# hasNotTakenEval(studentInClassID)
# Input: The row/ID number of the linker table of the student ID and course ID.
# Output: True or False
def hasNotTakenEval(studentInClassID):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	if(validStudentInClassId(studentInClassID)):
		cur.execute('SELECT * FROM Classes WHERE ClassID=?', (studentInClassID,))
		temp=cur.fetchall()
		if(temp[0][3]==0):
			return True
		else:
			return False

	else:
		print("Invalid ID")
		return False

#Stores respones in the database 
def tempstoreResponse(response):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()

	cur.execute('SELECT * FROM Classes')
	d= cur.fetchall()
	print ("Students In Classes ", d)

	cur.execute('SELECT * FROM Responses')
	e= cur.fetchall()
	print ("Responses: ", e)


	#print("response: ",response)
	if(len(response) != 0):
		sid=response[0]
		if(validSID(sid)):
			studentClass=getStudentInClassID(response[0],response[1])
			courseInfo=getCourseInfo(studentClass)
			courseID=courseInfo[0]
			print("studentClassID: ",studentClass)
			#print("courseInfo: ",courseInfo)
			#print("courseID: ",courseID)
			response[0]=courseID
			for i in range(1,len(response)):
				#if(esponse[i] != " "):
				if(response[i].isnumeric()):
					response[i]=int(response[i])
				else:
					response[i]=str(response[i])
			#print("casted response: ",response)
			if (hasNotTakenEval(studentClass)): 
				print("sid courseID ",sid, courseID)
				changeEvalStatus(sid,courseID)
				#print("studentClass: ", studentClass )
				#changeEvalStatusByClass(studentClass)
				cur.execute("INSERT into Responses values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(response))
				connect.commit()
				print("Stored Response")
				return True
			else:
				print("Student has already taken eval")
				changeEvalStatus(sid,courseID)
				return False
		else:
			print("Invalid Student ID Number")
			return False
	else:
		print("Response was null")
		return False

#Deletes an response from the database
def deleteResponseRow(rowID):
	print("delete Ran")
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute("DELETE FROM Responses WHERE ResponseID=?", (rowID,))
	connect.commit()

# returnClassResponses(courseID)
# Input: A course ID
# Output: All responses given for that course
def returnClassResponses(courseID):
	connect = sqlite3.connect('evalDB.db')
	cur = connect.cursor()
	cur.execute('SELECT * FROM Responses')
	a=cur.fetchall()
	print("all responses: ",a)
	cur.execute('SELECT * FROM Responses WHERE studentInCourseID=?', (courseID,))
	courseResponses=cur.fetchall()
	print("courseResponses: ",courseResponses)
	if(len(courseResponses)==0):
		print("No Responses Available")
		return False
	else:
		return courseResponses
	#for i in range(len(response)):


#Creates an excel file for all the responses 
#Uses the date, time, and course name for name of file
#Also does calculations on some numbers and creates graphs
def createExcelFile(responses):
	print("Making Excel Sheet")
	
	#list of excel columns used for creating where items need to be placed
	letters=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]
	questionList=[ "Course Name","What year are you at K?","This class is a...","In this course, I gained ​a deeper understanding of the subject​", "In this course, I gained the ability to think critically about course subject matter", "In this course, I gained a new or increased interest in this subject", "In this course, I improved my ability to​ consider varying perspectives or approaches", "In this course, I improved my ability to apply skills required for the course", "In this course, I improved my ability to think independently and creatively", "In this course, I improved my ability to​ think collaboratively", "In this course, I improved my ability to express my ideas effectively", "Please make comments or suggestions:​", "Course goals and requirements were clearly explained", "The course was appropriately challenging", "Course materials (texts, readings, equipment, visuals, etc.) were effective", "Class time was organized and used effectively", "Projects and assignments in this course contributed significantly to my learning", "Students’ ideas and contributions were encouraged", "My work was evaluated fairly", "The instructor gave me timely feedback on my work", "The instructor gave me helpful suggestions for improvement", "The instructor was available during office hours and for appointments", "The teaching techniques in this course were effective in helping me learn (for example, discussions, demonstrations, lectures, group work, audiovisuals, etc.)", "Please make comments or suggestions:", "Service-Learning contributed significantly to my learning", "Labs contributed significantly to my learning", "Please make comments or suggestions:", "Overall, I put considerable effort into this course", "Overall, this course was valuable to my academic and/or personal growth", "Please make comments or suggestions:", "Overall, this instructor’s teaching was", "Overall, this course was", "Please make comments or suggestions:" ]
	now = datetime.now()
	#removes spaces from course name
	courseString=responses[0][2]
	nameList= courseString.split(' ')
	courseName="-".join(nameList)
	dt_string = str(now.strftime("%d-%m-%Y_%H-%M"))
	#creates name of excel file
	fullName=courseName+"_Course_Evals_From_"+dt_string+".xlsx"
	#creates excel sheet
	workbook = xlsxwriter.Workbook("Output/"+fullName)
	worksheet = workbook.add_worksheet()
	#intiates formating
	bold = workbook.add_format({'bold': 1})

	#This loop adds all the questions to file
	for i in range(len(questionList)):
		worksheet.write(20, i, questionList[i])
	#This loop adds all the raw responses to file
	for j in range(len(responses)):
		r=responses[j][2:len(responses[j])]
		for x in range(len(r)):
			if(r[x]==" "):
				continue
			else:
				worksheet.write(j+21, x, r[x])

	size=str(len(responses)+21)

	worksheet.write('C20', 'Mean', bold)
	#Adds all the means of the questions to the sheet in bold 
	for y in range(3,33):
		if (y!=11 and y!=23 and y!=26 and y!=29 and y!=32):
			avgStr="=AVERAGE("+letters[y]+"22:"+letters[y]+size+")"
			worksheet.write(19,y, avgStr, bold)

	#prefoms countifs for each question for each option
	for y in range(3,33):
		if (y!=11 and y!=23 and y!=26 and y!=29 and y!=32):

			countIf1="=COUNTIF("+letters[y]+"22:"+letters[y]+size+",\"1\")"
			countIf2="=COUNTIF("+letters[y]+"22:"+letters[y]+size+",\"2\")"
			countIf3="=COUNTIF("+letters[y]+"22:"+letters[y]+size+",\"3\")"
			countIf4="=COUNTIF("+letters[y]+"22:"+letters[y]+size+",\"4\")"
			countIf5="=COUNTIF("+letters[y]+"22:"+letters[y]+size+",\"5\")"
			countIfBlank="=COUNTBLANK("+letters[y]+"22:"+letters[y]+size+")"
			place1=letters[y]+'1'
			place2=letters[y]+'2'
			place3=letters[y]+'3'
			place4=letters[y]+'4'
			place5=letters[y]+'5'
			place6=letters[y]+'6'

			worksheet.write(place1, countIf1)
			worksheet.write(place2, countIf2)
			worksheet.write(place3, countIf3)
			worksheet.write(place4, countIf4)
			worksheet.write(place5, countIf5)
			worksheet.write(place6, countIfBlank)

	#adds labels 
	worksheet.write('C1', "Strongly Disagree (1)", bold)
	worksheet.write('C2', "Disagree (2)", bold)
	worksheet.write('C3', "Nuetral (3)", bold)
	worksheet.write('C4', "Agree (4)", bold)
	worksheet.write('C5', "Strongly Agree (5)", bold)
	worksheet.write('C6', "Blank", bold)

	#changes column width
	worksheet.set_column(0, 1, 25)
	worksheet.set_column(1, 1, 25)
	worksheet.set_column(2, 1, 25)

	#Creates strings of commands for countifs 
	countIfF="=COUNTIF(B22:B"+size+",\"Freshman\")"
	countIfS="=COUNTIF(B22:B"+size+",\"Sophmore\")"
	countIfJ="=COUNTIF(B22:B"+size+",\"Junior\")"
	countIfSe="=COUNTIF(B22:B"+size+",\"Senior\")"
	countIfO="=COUNTIF(B22:B"+size+",\"Other\")"

	#Inserts countifs for students year
	worksheet.write('B1', countIfF)
	worksheet.write('B2', countIfS)
	worksheet.write('B3', countIfJ)
	worksheet.write('B4', countIfSe)
	worksheet.write('B5', countIfO)
	worksheet.write('A1', "Freshman")
	worksheet.write('A2', "Sophmores")
	worksheet.write('A3', "Juniors")
	worksheet.write('A4', "Seniors")
	worksheet.write('A5', "Other")

	#sets chart name and size 
	chartNames="=Sheet1!$A$1:$A$5"
	chartSize="Sheet1!$B$1:$B$5"
	#Setting up a pie chart
	pieChart = workbook.add_chart({'type': 'pie'})
	pieChart.add_series({'name': "Student Year Breakdown",'categories':chartNames, 'data_labels': {'value': True, 'percentage': True, 'separator': '\n', 'position': 'inside_end'}, 'values': chartSize})
	pieChart.set_size({'width': 720/2.5, 'height': 576/2.5})
	#adds a chart to the sheet
	worksheet.insert_chart('A6', pieChart)

	#Setting up a column chart
	barChart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
	barChart.add_series({'name': '=Sheet1!$C$1', 'values': '=Sheet1!$D$1:$AF$1', 'fill':{'color':'#DC143C'}})
	barChart.add_series({'name': '=Sheet1!$C$2', 'values': '=Sheet1!$D$2:$AF$2', 'fill':{'color':'#FA8072'}})
	barChart.add_series({'name': '=Sheet1!$C$3', 'values': '=Sheet1!$D$3:$AF$3', 'fill':{'color':'#808080'}})
	barChart.add_series({'name': '=Sheet1!$C$4', 'values': '=Sheet1!$D$4:$AF$4', 'fill':{'color':'#87CEEB'}})
	barChart.add_series({'name': '=Sheet1!$C$5', 'values': '=Sheet1!$D$5:$AF$5', 'fill':{'color':'#1E90FF'}})
	barChart.add_series({'name': '=Sheet1!$C$6', 'values': '=Sheet1!$D$6:$AF$6', 'fill':{'color':'#C6C6C6'}})
	#adds a chart to the sheet
	worksheet.insert_chart('AG1', barChart)
	#closes the file
	workbook.close()
	print("Finsihed Making Excel Sheet")

#main()



