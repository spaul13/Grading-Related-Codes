import pandas, csv

grade = {}
#folder where graded files are stored
parent = "gradedfiles/"
#add files here after regrading
csvfileList = ['HW0_masterGrades_8sep.csv', 'HW0_masterGrades_9sep.csv', 'HW0_masterGrades_10sep.csv', 'HW0_masterGrades_10sep_2.csv']
finaloutputcsvFile = 'output-grades.csv'


def gitidgradeMapping(csvFile):
	df = pandas.read_csv(csvFile)

	for i in range(len(df)):
		if df['GitHub Username'][i] in grade:
			grade[df['GitHub Username'][i]].append(float(df['hw0'][i]))
		else:
			grade[df['GitHub Username'][i]] = [float(df['hw0'][i])]

#populate the git-vs-grade mapping with all possible grades for same gitID
for csvfile in csvfileList:
	gitidgradeMapping(parent + csvfile)

usergradeMap, usernameMap = {}, {}
#take the maximum one for each gitID after all grading
for i in grade.keys():
	if len(grade[i])>1:
		usergradeMap[i] = max(grade[i])
		#checks two nonzero grades
		#checking inconsistency		
		#if ((grade[i][0]==0) and (grade[i][1]==0)):
		#	print(i, grade[i][0], grade[i][1])
	else:
		usergradeMap[i] = grade[i][0]


df = pandas.read_csv('ECE 264 GitHub info — Fall 2021 (Responses) - Form Responses 1.csv')
print(df.keys())
for i in range(len(df)):
	print(df['Purdue username'][i])
	if "@purdue.edu" not in df['Purdue username'][i]:
		usernameMap[df['Github username'][i]] = str(df['Purdue username'][i]).lower() + "@purdue.edu"
	else:
		usernameMap[df['Github username'][i]] = str(df['Purdue username'][i]).lower()



df = pandas.read_csv('Fall 2021 ECE 264 - Merge_GradesExport_2021-09-09-16-19.csv')
usernameidMap = {}
for i in range(len(df)):
	usernameidMap[df["Email"][i]] = df["OrgDefinedId"][i]

comment = "Git Id for this user name either not submitted or submitted incorrectly, so 5 marks deducted for that"
counter, counter1, counter2 = 0, 0, 0
data = []


for i in usergradeMap.keys():
	if usergradeMap[i] <= 0.0:
		usergradeMap[i] = 0.0
	#if checks if gitID is not available or incorrect
	if i not in list(usernameMap.keys()):
		if usergradeMap[i]>=5:
			print(i, "NS", usergradeMap[i]-5,comment)
		else:
			print(i, "NS", usergradeMap[i])
		counter+=1
	else:		
		try:		
			print("%s,%s,%f" %(usernameidMap[usernameMap[i]], usernameMap[i], usergradeMap[i]))
			data.append([usernameidMap[usernameMap[i]], usernameMap[i], usergradeMap[i], '#'])
			counter2+=1
		except:#if no longer registered 
			#print(usernameMap[i] + " not found")
			counter1+=1
print(counter,counter1, counter2)

#writing to csv file that can be pushed to Brightspace
header = ["OrgDefinedId", "Email", "Homework 0 Points Grade <Numeric MaxPoints:100>", "End-of-Line Indicator"]
with open(finaloutputcsvFile, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    #write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)





