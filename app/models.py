from app import mysql

class Student(object):

    def __init__(self, studentID = None, name = None, course_code = None, college_code = None, year = None, gender = None, profile_url = None):
        self.id = studentID
        self.name = name
        self.course_code = course_code
        self.college_code = college_code
        self.year = year
        self.gender = gender
        self.profile_url = profile_url

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO Student(studentID, name, course_code, college_code, year, gender, profile_url) \
                VALUES('{self.id}', '{self.name}', '{self.course_code}', '{self.college_code}', '{self.year}', '{self.gender}', '{self.profile_url}')" 
        cursor.execute(sql)
        mysql.connection.commit()

    def edit(self, id):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE Student SET studentID='{self.id}', name='{self.name}', course_code='{self.course_code}', college_code='{self.college_code}', year='{self.year}' , gender='{self.gender}', profile_url='{self.profile_url}' WHERE studentID='{id}'" 
        cursor.execute(sql)
        mysql.connection.commit()

    @classmethod
    def get(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM Student WHERE studentID = '{id}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    @classmethod
    def search(cls, search):
        cursor = mysql.connection.cursor()
        sql = f"SELECT Student.studentID, Student.name, College.college_name, Course.course_name, Student.year, Student.gender, Student.profile_url FROM Student INNER JOIN Course ON Student.course_code = Course.code INNER JOIN College ON Student.college_code = College.code WHERE studentID LIKE '{search}%' OR name LIKE '{search}%' OR Student.college_code LIKE '{search}%' OR college_name LIKE '{search}%' OR Student.course_code LIKE '{search}%' OR course_name LIKE '{search}%' OR year LIKE '{search}%' OR gender LIKE '{search}%'  ORDER BY name, studentID"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()
        sql = "SELECT Student.studentID, Student.name, College.college_name, Course.course_name, Student.year, Student.gender, Student.profile_url FROM Student INNER JOIN Course ON Student.course_code = Course.code INNER JOIN College ON Student.college_code = College.code  ORDER BY name, studentID"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls,id):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE FROM Student WHERE studentID = '{id}'"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False

    @classmethod
    def courses_from_college(cls, college):
        cursor = mysql.connection.cursor()
        sql = f"SELECT code FROM Course WHERE college_code = '{college}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results 

class College(object):
    
    def __init__(self, college_code= None, college_name = None):
        self.college_code = college_code
        self.college_name = college_name

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO College(code, college_name) \
                VALUES('{self.college_code}','{self.college_name}')" 

        cursor.execute(sql)
        mysql.connection.commit()

    def edit(self, id):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE College SET code='{self.college_code}', college_name='{self.college_name}' WHERE code='{id}'" 
        cursor.execute(sql)
        mysql.connection.commit()

    @classmethod
    def get(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * from College WHERE code = '{id}' "
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * from College ORDER BY code"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
    @classmethod
    def search(cls, search):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * from College WHERE code LIKE '{search}%' OR college_name LIKE '{search}%'"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls,id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT code FROM College"
        cursor.execute(sql)
        holder = cursor.fetchone()
        while id == holder[0]:
            holder = cursor.fetchone()
        holder = holder[0]
        print(type(holder))
        print(holder)
        cursor.fetchall()
        
        sql = f"UPDATE Student SET college_code = '{str(holder)}' WHERE college_code = '{str(id)}'"
        cursor.execute(sql)
        sql = f"UPDATE Course SET college_code = '{str(holder)}' WHERE college_code = '{str(id)}'"
        cursor.execute(sql)
        sql = f"DELETE FROM College WHERE code = '{id}'"
        cursor.execute(sql)
        mysql.connection.commit()
        return

class Course(object):

    def __init__(self, course_code = None, course_name = None, college_code = None):
        self.course_code = course_code
        self.course_name = course_name
        self.college_code = college_code

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO Course(code, course_name, college_code) \
                VALUES('{self.course_code}','{self.course_name}','{self.college_code}')" 

        cursor.execute(sql)
        mysql.connection.commit()

    def edit(self, id):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE Course SET code='{self.course_code}', course_name='{self.course_name}', college_code = '{self.college_code}' WHERE code='{id}'"
        cursor.execute(sql)
        sql = f"UPDATE Student SET college_code='{self.college_code}' WHERE course_code='{self.course_code}'"
        cursor.execute(sql)
        mysql.connection.commit()

    @classmethod
    def get(cls, id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * from Course WHERE code = '{id}' "
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM Course ORDER BY college_code, code"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
    @classmethod
    def search(cls, search):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM Course INNER JOIN College ON Course.college_code = College.code WHERE Course.code LIKE '{search}%' OR College.college_name LIKE '{search}%' OR College.code LIKE '{search}%' OR course_name LIKE '{search}%' ORDER BY College.code, Course.code"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        return result
        

    @classmethod
    def delete(cls, id):
        
        cursor = mysql.connection.cursor()
        sql = f"SELECT code FROM Course"
        cursor.execute(sql)
        holder = cursor.fetchone()
        while id == holder[0]:
            holder = cursor.fetchone()
        holder = holder[0]
        print(type(holder))
        print(holder)
        cursor.fetchall()
        
        sql = f"UPDATE Student SET course_code = '{str(holder)}' WHERE course_code = '{str(id)}'"
        cursor.execute(sql)
        sql = f"DELETE FROM Course WHERE code = '{id}'"
        cursor.execute(sql)
        mysql.connection.commit()
        return
        