import mysql.connector

mysqldb = mysql.connector.connect(host="localhost", user="root", password="root")
cursor = mysqldb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS sis_webapp")
mysqldb.close()


mysqldb = mysql.connector.connect(host="localhost",user="root",password="root", database = "sis_webapp")
cursor = mysqldb.cursor()

# College init
cursor.execute("CREATE TABLE College(code VARCHAR(100), college_name VARCHAR(100), PRIMARY KEY (code))")
mysqldb.commit()

# Course init
cursor.execute("CREATE TABLE Course(code VARCHAR(100), course_name VARCHAR(100), college_code VARCHAR(100), PRIMARY KEY (code), FOREIGN KEY(college_code) REFERENCES College(code) ON DELETE SET NULL ON UPDATE CASCADE)")
mysqldb.commit()

# Student init
cursor.execute("""CREATE TABLE Student(
  studentID CHAR(9),
  name VARCHAR(50) NOT NULL,
  course_code VARCHAR(100),
  college_code VARCHAR(100),
  year VARCHAR(10) NOT NULL,
  gender VARCHAR(6) NOT NULL,
  profile_url VARCHAR(500),
  PRIMARY KEY(studentID),
  FOREIGN KEY(course_code) REFERENCES
  Course(code) ON DELETE SET NULL ON UPDATE CASCADE,
  FOREIGN KEY(college_code) REFERENCES
  College(code) ON DELETE SET NULL ON UPDATE CASCADE
)""")

print("Database initialization done!")