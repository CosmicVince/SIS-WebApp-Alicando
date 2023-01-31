from flask import Blueprint, render_template, session, redirect, request, abort, flash, jsonify
from app.users.forms import StudentForm, CollegeForm, CourseForm
import app.models as models




routes = Blueprint('routes', __name__)

@routes.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@routes.route('/add_student/<college>')
def dynamic_dropdown(college):
    courses = models.Student.courses_from_college(college)

    course_list = []

    for course in courses:
        courseObj = {}
        courseObj['name'] = course
        course_list.append(courseObj)

    return jsonify({'courses': course_list})

    

@routes.route('/')
def landing_page():
    students = models.Student.all()
    return render_template("student_table.html", students=students)

@routes.route('/add_student', methods=['POST', 'GET'])
def add_student():

    form = StudentForm(request.form)

    colleges = []
    courses = []
    for item in models.College.all():
        colleges.append(item[0])

    form.college_code.choices = colleges

    for item in models.Student.courses_from_college(form.college_code.choices[0]):
        courses.append(item[0])

    form.course_code.choices = courses

    if request.method == 'POST':
        if form.profile_url.data == "":
            flash("Error: Please fill in all of the required info.")
            return render_template('add_student.html', form=form)
        if form.validate_on_submit():
            try:
                student = models.Student(studentID = form.idnum.data, name = form.name.data, college_code = form.college_code.data, \
                course_code = form.course_code.data, year = form.year_level.data, gender = form.gender.data, profile_url = form.profile_url.data)
                student.add()
                flash("Student added.")
                return redirect('/')
            except:
                flash("Duplicate Info. Please try again.")
                return render_template('add_student.html', form=form)
        else:
            flash("Please enter the correct information.")
            return render_template('add_student.html', form=form)
    else:
        return render_template('add_student.html', form=form)

@routes.route('/edit_student', methods=['POST', 'GET'])
def edit_student():

    id = request.args["student_id"]

    if request.method == 'POST':
        form = StudentForm(request.form)

        if form.validate_on_submit():
            try:
                student = models.Student(studentID = form.idnum.data, name = form.name.data, college_code = form.college_code.data, \
                course_code = form.course_code.data, year = form.year_level.data, gender = form.gender.data, profile_url = form.profile_url.data)
                student.edit(id)
                flash("Edit Successful.")
                print(session)
                return redirect('/')
            except:
                flash("Duplicate ID. Please try again.")
        else:
            flash("Please enter the correct information.")
            
    # if get 
    user_edit = models.Student.get(id)

    form = StudentForm(request.form, college_code=user_edit[3], course_code=user_edit[2])

    colleges = []
    courses = []
    for item in models.College.all():
        colleges.append(item[0])
    for item in models.Student.courses_from_college(form.college_code.data):
        courses.append(item[0])

    form.college_code.choices = colleges
    form.course_code.choices = courses
    
    formlist = [form.idnum, form.name, form.course_code, form.college_code, form.year_level, form.gender, form.profile_url]
    x = 0
    for item in formlist:
        item.data = user_edit[x]
        x += 1

    return render_template('edit_student.html', form=form)


@routes.route('/delete_student', methods=['POST', 'GET'])
def delete_student():
    id = request.args["student_id"]
    models.Student.delete(id)
    flash('Student has been successfully deleted.')
    return redirect("/")


# -- Course

@routes.route('/course_table')
def course_table():
    courses = models.Course.all()
    return render_template("course_table.html", courses=courses)

@routes.route('/add_course', methods=['POST', 'GET'])
def add_course():
    form = CourseForm(request.form)

    colleges = []
    for item in models.College.all():
        colleges.append(item[0])

    form.college_code.choices = colleges

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                course = models.Course(course_code=form.course_code.data, course_name=form.course_name.data, college_code=form.college_code.data)
                course.add()
                flash("Course added.")
                return redirect('/course_table')
            except:
                flash("Duplicate ID. Please try again.")
                return render_template('add_course.html', form=form)
        else:
            flash("Please enter the correct information.")
            return render_template('add_course.html', form=form)
    else:
        return render_template('add_course.html', form=form)

@routes.route('/edit_course', methods=['POST', 'GET'])
def edit_course():
    id = request.args["course_id"]

    if request.method == 'POST':
        form = CourseForm(request.form)

        if form.validate_on_submit():
            try:
                course = models.Course(course_code=form.course_code.data, course_name=form.course_name.data, college_code=form.college_code.data)
                course.edit(id)
                flash("Edit Successful.")
                print(session)
                return redirect('/course_table')
            except:
                flash("Duplicate ID. Please try again.")
                colleges = []

                for item in models.College.all():
                    colleges.append(item[0])

                form.college_code.choices = colleges
                return render_template('edit_course.html', form=form)
        else:
            flash("Please enter the correct information.")
            colleges = []

            for item in models.College.all():
                colleges.append(item[0])

            form.college_code.choices = colleges
            return render_template('edit_course.html', form=form)
    # if get
    else:
        
        course_edit = models.Course.get(id)

        form = CourseForm(request.form, college_code=course_edit[2])

        colleges = []

        for item in models.College.all():
            colleges.append(item[0])

        form.college_code.choices = colleges
        
        formlist = [form.course_code, form.course_name, form.college_code]
        x = 0
        for item in formlist:
            item.data = course_edit[x]
            x += 1
 
        return render_template('edit_course.html', form=form)

@routes.route('/delete_course', methods=['POST', 'GET'])
def delete_course():
    id = request.args["course_id"]
    print(id)
    models.Course.delete(id)
    flash('Course has been successfully deleted.')
    return redirect("/course_table")

# --- College Routes

@routes.route('/college_table')
def college_table():
    colleges = models.College.all()
    return render_template("college_table.html", colleges=colleges)


@routes.route('/add_college', methods=['POST', 'GET'])
def add_college():
    form = CollegeForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                college = models.College(college_code=form.college_code.data, college_name=form.college_name.data)
                college.add()
                flash("College added.")
                return redirect('/college_table')
            except:
                flash("Duplicate ID. Please try again.")
                return render_template('add_college.html', form=form)
        else:
            flash("Please enter the correct information.")
            return render_template('add_college.html', form=form)
    else:
        return render_template('add_college.html', form=form)

@routes.route('/edit_college', methods=['POST', 'GET'])
def edit_college():
    id = request.args["college_id"]

    if request.method == 'POST':
        form = CollegeForm(request.form)

        if form.validate_on_submit():
            try:
                college = models.College(college_code=form.college_code.data, college_name=form.college_name.data)
                college.edit(id)
                flash("Edit Successful.")
                print(session)
                return redirect('/college_table')
            except:
                flash("Duplicate ID. Please try again.")
                return render_template('edit_college.html', form=form)
        else:
            flash("Please enter the correct information.")
            return render_template('edit_college.html', form=form)
    # if get
    else:
        
        college_edit = models.College.get(id)

        form = CollegeForm(request.form)
        
        formlist = [form.college_code, form.college_name]
        x = 0
        for item in formlist:
            item.data = college_edit[x]
            print(item.data)
            x += 1
 
        return render_template('edit_college.html', form=form)


@routes.route('/delete_college', methods=['POST', 'GET'])
def delete_college():
    id = request.args["college_id"]
    models.College.delete(id)
    flash('College has been successfully deleted.')
    return redirect("/college_table")


# --- Search Routes

@routes.route("/search", methods=['POST', 'GET'])
def search():
    print("Hi")
    # if request.method == "POST":
    print("proc")
    text = request.args['searchText']
    print(text)
    if text != '':
        students = models.Student.search(text)
    else:
        students = models.Student.all()
    print(students)
    return render_template('student_table_gen.html', students=students)

@routes.route("/search_course", methods=['POST', 'GET'])
def search_course():
    print("Hi")
    # if request.method == "POST":
    print("proc")
    text = request.args['searchText']
    print(text)
    if text != '':
        courses = models.Course.search(text)
    else:
        courses = models.Course.all()
    print(courses)
    return render_template('course_table_gen.html', courses=courses)

@routes.route("/search_college", methods=['POST', 'GET'])
def search_college():
    print("Hi")
    # if request.method == "POST":
    print("proc")
    text = request.args['searchText']
    print(text)
    if text != '':
        colleges = models.College.search(text)
    else:
        colleges = models.College.all()
    return render_template('college_table_gen.html', colleges=colleges)