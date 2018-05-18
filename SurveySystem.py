from abc import ABCMeta, abstractmethod
import csv
import datetime

from sqlalchemy import *
from sqlalchemy.orm import *

from declarative import *

class SurveySystem:

	def add_all_courses(self, courses_file):
		with open(courses_file, 'r') as courses_in:
				for row in list(csv.reader(courses_in)):
					course_name = row[0] + ' ' + row[1]
					new_course = Course(course_name=course_name)
					new_survey = Survey(course=course_name, state="to_create",time="infinity")
					try:
						self.session.add(new_course)
						self.session.add(new_survey)
						self.session.commit()
						print(course_name)
					except:
						#print("This course has already been added")
						pass

	def add_all_users(self, users_file):
		with open(users_file, 'r') as entry_in:
				for row in list(csv.reader(entry_in)):
					zid = row[0]
					password = row[1]
					role = row[2]
					new_entry = User(id=zid, password=password, role=role)
					try:
						self.session.add(new_entry)
						self.session.commit()
					except:
						#print("This user has already been created")
						pass

	def add_user(self, zid, password, role):
		if (not (role == 'admin' or role == 'staff' or role == 'student')):
			return
		if (not (isinstance(zid, int)) and not zid == 'admin'):
			# print('zid not valid non-integer')
			return
		elif (isinstance(zid, int) and not ((zid >= 50 and zid <= 999))):
			# print('zid not valid integer')
			return
		else:
			new_user = User(id=zid, password=password, role=role)
			try:
				self.session.add(new_user)
				self.session.commit()
			except:
				#print("This particular enrolment has already been created")
				pass

	def add_all_enrolments(self, enrolments_file):
		with open(enrolments_file, 'r') as enrolment_in:
				for row in list(csv.reader(enrolment_in)):
					zid = row[0]
					course_name = row[1] + ' ' + row[2]
					new_enrolment = Enrolment(id=zid, course=course_name, is_survey_completed=0)
					try:
						self.session.add(new_enrolment)
						self.session.commit()
						# print(zid, course_name)
					except:
						self.session.rollback()
						#print("This particular enrolment has already been created")
						pass

	def enrol_user(self, zid, course_name):
		if (not isinstance(zid, int)):
			# print('zid not valid non-integer')
			return
		elif (not (zid >= 50 and zid <= 1219)):
			# print('zid not valid integer')
			return
		else:
			new_enrolment = Enrolment(id=zid, course=course_name, is_survey_completed=0)

			try:
				self.session.add(new_enrolment)
				self.session.commit()
			except:
				#print("This particular enrolment has already been created")
				pass




	def get_surveys_for(self, user):
		print(user)
		if self.session.query(User).filter(User.id==user).first().role == "admin":
			all_courses = self.session.query(Survey).all()
			for course in all_courses:
				current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
				end_date = self.session.query(Survey).filter(Survey.course==course.course).first().time
				if current_time > end_date:
					self.session.query(Survey).filter(Survey.course==course.course).first().state = "closed"
			return all_courses
		else:
			courses = self.session.query(Enrolment).filter(Enrolment.id==user).all()
			ready_courses = []
			closed_courses = []
			for course in courses:
				if self.session.query(User).filter(User.id==user).first().role == "staff":
					current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
					end_date = self.session.query(Survey).filter(Survey.course==course.course).first().time
					print ("I'm here")
					print(end_date)
					print(current_time)
					if current_time > end_date:
						self.session.query(Survey).filter(Survey.course==course.course).first().state = "closed"
					if self.session.query(Survey).filter(Survey.course==course.course).first().state == "review":
						#print(course.course)
						ready_courses.append(course)
					if self.session.query(Survey).filter(Survey.course==course.course).first().state == "closed":
						#print(course.course)
						closed_courses.append(course)
				if self.session.query(User).filter(User.id==user).first().role == "student":
					current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
					end_date = self.session.query(Survey).filter(Survey.course==course.course).first().time
					if current_time > end_date:
						self.session.query(Survey).filter(Survey.course==course.course).first().state = "closed"
					if self.session.query(Survey).filter(Survey.course==course.course).first().state == "open":
						#print(course.course)
						ready_courses.append(course)
					if self.session.query(Survey).filter(Survey.course==course.course).first().state == "closed":
						#print(course.course)
						closed_courses.append(course)
				if self.session.query(User).filter(User.id==user).first().role == "guest":
					current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
					end_date = self.session.query(Survey).filter(Survey.course==course.course).first().time
					if current_time > end_date:
						self.session.query(Survey).filter(Survey.course==course.course).first().state = "closed"
					if self.session.query(Survey).filter(Survey.course==course.course).first().state == "open":
						#print(course.course)
						ready_courses.append(course)
					if self.session.query(Survey).filter(Survey.course==course.course).first().state == "closed":
						#print(course.course)
						closed_courses.append(course)
			return ready_courses, closed_courses #returns list of Survey objects

	def get_questions_from_pool(self):
		question_pool = self.session.query(Question).all()
		return question_pool


	def get_questions_from_survey(self, survey):
		survey_questions = []
		for question in self.session.query(QuestionToSurvey).filter(QuestionToSurvey.survey==survey):  #find all questions under a survey in QuestionToSurvey
			for specific_question in self.session.query(Question).filter(Question.question_text==question.question_text):  #find question in Question table to get options and requirement
				survey_questions.append(specific_question)
		return survey_questions


	def get_results(self, survey):
		questions = self.session.query(QuestionToSurvey).filter(QuestionToSurvey.survey==survey).all() #get a list of all the questions in the survey
		q_and_a = []
		i = 0
		for question in questions:
			questionOBJ = self.session.query(Question).filter(Question.question_text==question.question_text).first()
			#should get the Question object so that type of question can be determined
			all_responses = self.session.query(Answer).filter(and_(Answer.survey==survey, Answer.question==question.question_text)).all()  #query table of answers for reponses statisfying two conditions
			q = [] #this list will store index 0 as question and answers in the following indices
			q.insert(0, questionOBJ)
			q_and_a.insert(i, q)
			if questionOBJ.type == "fr":
				responses = []
				for answer in all_responses:
					responses.append(answer)
				q.append(responses)
			elif questionOBJ.type == "mc":
				option_occurrences = {}
				for item in self.default_options:
					option_occurrences[item] = 0
					for answer in all_responses:
						if answer.answer_text == item:
							option_occurrences[item] += 1
				q.append(option_occurrences)
			i += 1
		return q_and_a

	def get_results_data(self, results):  #convert into syntax that the Google Charts API can interpret
		all_questions = []  #list of all questions
		for question in results:
			single_question = []  #list with question_text, question type and all options/responses
			single_question.append(question[0].question_text)
			single_question.append(question[0].type)
			if question[0].type == "mc":
				all_options = [] #list of just the options
				for m in question[1]:
					option = [] #small list of the option_text and number of responses for an option
					option.append(m)
					option.append(question[1][m])
					#print(option)
					all_options.append(option)
				single_question.append(all_options[:])
				all_questions.append(single_question[:])
			elif question[0].type == "fr":
				responses = []  #list of responses
				for response in question[1]:
					print(response.answer_text)
					responses.append(response.answer_text)
				single_question.append(responses[:]) #append the list of text responses
				all_questions.append(single_question[:])
		print(all_questions)
		return all_questions

	def get_enrolment_for(self, course, id):
		enrolment = self.session.query(Enrolment).filter(and_(Enrolment.id==id, Enrolment.course==course)).first()
		print(enrolment.id)
		print(enrolment.course)
		return enrolment

	def survey_is_completed(self, enrolment):
		enrolment.is_survey_completed = 1


	def add_guest_user(self, user_id, password):
		new_user = User(id=user_id, password=password, role="unreg")
		try:
			self.session.add(new_user)
			self.session.commit()
		except:
			#print("This guest user has already been persisted")
			pass

	def add_guest_enrolment(self, user_id, course):
		new_enrol = Enrolment(id=user_id, course=course, is_survey_completed=0)
		try:
			self.session.add(new_enrol)
			self.session.commit()
		except:
			#print("This guest enrolment has already been persisted")
			pass

	def get_all_guest(self):
		all_reg = []
		guest_user = self.session.query(User).filter(User.role=="unreg").all()
		for user in guest_user:
			guest_enrol = self.session.query(Enrolment).filter(Enrolment.id==user.id).first()
			all_reg.append(guest_enrol)
		return all_reg

	def authorise_reg(self, id):
		self.session.query(User).filter(User.id==id).first().role = "guest"
		self.session.commit()

	def add_question_to_pool(self, question, type, requirement, deleted):
		if type=="mc":
			try:
				added = self.session.query(Question).filter(and_(Question.question_text==question, Question.type=="mc")).first()
				print(added)
				if added == None:
					mc = MCQuestion(question_text=question, type=type, requirement=requirement, deleted=deleted, options=str(self.default_options))
					self.session.add(mc)
					self.session.commit()
					return True
				else:
					print("Question has already been added to the pool")
					return False
			except:
				print("Committed")
				print("Question has already been added to the pool")
				self.session.rollback()
				return False
		elif type=="fr":
			try:
				added = self.session.query(Question).filter(and_(Question.question_text==question, Question.type=="fr")).first()
				if added == None:
					fr = FRQuestion(question_text=question, type=type, requirement=requirement, deleted=deleted)
					self.session.add(fr)
					self.session.commit()
					return True
				else:
					print("Question has already been added to the pool")
					return False
			except:
				print("Question has already been added to the pool")
				# self.session.rollback()
				return False


	def add_questions_to_survey(self, questions, survey):
		#should check if argument is None or list of questions is empty
		for question in questions:
			new_qts = QuestionToSurvey(question_text=question, survey=survey)
			try:
				self.session.add(new_qts)
				self.session.commit()
			except:
				#print("This question has already been added to the survey.") #should pass this info to the user
				pass

	def save_response(self, question, answer, survey):
		new_row = Answer(question=question, answer_text=answer, survey=survey)
		self.session.add(new_row)
		self.session.commit()

	def delete_question_from_pool(self, questions):
		for question in questions:
			#selected = self.session.query(Question).filter(Question.question_text==question).first().deleted = 1
			question = question.split(':')
			type = question[0]
			question.pop(0)
			question = ':'.join(question)
			selected = self.session.query(Question).filter(and_(Question.question_text==question, Question.type==type)).first().deleted = 1
			self.session.commit()

	def delete_questions_from_survey(self, questions, survey):
		pass

	def change_time(self, end_date, survey):
		self.session.query(Survey).filter(Survey.course==survey).first().time = end_date
		self.session.commit()

	def change_state(self, new_state, survey):
		self.session.query(Survey).filter(Survey.course==survey).first().state = new_state
		self.session.commit()

	def __init__(self, session):
		self.session = session
		self.default_options = ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"]
