from routes import app
#from server import SS

#SS.add_all_courses('courses.csv') :
#SS.add_all_users('passwords.csv')
#SS.add_all_enrolments('enrolments.csv')


app.run(debug=True, port=8000)
