from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators, RadioField, HiddenField
import app.models as models


class StudentForm(FlaskForm):
    idnum = StringField('ID Number', [validators.InputRequired(), validators.DataRequired(), validators.Regexp('^\d{4}-\d{4}$')])
    name = StringField('Name', [validators.InputRequired(), validators.Length(min=5, max=90)])
    college_code = SelectField('College', choices=[""], validators=[validators.InputRequired()], validate_choice=False)
    course_code = SelectField('Course', choices=[""], validators=[validators.InputRequired()], validate_choice=False)
    year_level = SelectField('Year Level', choices=['1st Year','2nd Year','3rd Year','4th Year','5th Year','Irregular'], validators=[validators.InputRequired()], validate_choice=False)
    gender = RadioField('Gender', [validators.InputRequired()], choices = ['Male', 'Female'])
    profile_url = HiddenField('profile_url', [validators.DataRequired()], render_kw = {'id': 'profile_url'})

class CourseForm(FlaskForm):
    course_code = StringField ('Course Code', [validators.DataRequired()])
    course_name = StringField('Course Name', [validators.DataRequired()])
    college_code = SelectField('College Code', choices=[""], validators=[validators.DataRequired()], validate_choice=False)


class CollegeForm(FlaskForm):
    college_code = StringField ('College Code', [validators.DataRequired()])
    college_name = StringField('College Name', [validators.DataRequired()])
