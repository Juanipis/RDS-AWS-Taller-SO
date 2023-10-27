from pydantic_settings import BaseSettings
import psycopg2

from app.models.student import Student

class RDSCredentiasl(BaseSettings):
    rds_host: str
    rds_port: int
    rds_user: str
    rds_password: str
    rds_region: str = 'us-east-1'
    rds_db_name: str

class RDSController:
    def __init__(self, rds_credentials=RDSCredentiasl()):
        self.credentials = rds_credentials
        self.conn = psycopg2.connect(
            host=self.credentials.rds_host,
            port=self.credentials.rds_port,
            user=self.credentials.rds_user,
            password=self.credentials.rds_password,
            dbname=self.credentials.rds_db_name
        )
        self.cursor = self.conn.cursor()
        self.start_table()

    def start_table(self):
        self.cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'students'
            );
        """)
        if not self.cursor.fetchone()[0]:
            # Si no existe, crearla
            self.cursor.execute("""
                CREATE TABLE students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    age INTEGER NOT NULL,
                    grade INTEGER NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
            """)
        else:
            self.cursor.execute("""
                DELETE FROM students;
            """)
            self.conn.commit()
        
    def insert_student(self, student):
        self.cursor.execute(f"""
            INSERT INTO students (name, age, grade, email, password)
            VALUES ('{student.name}', {student.age}, {student.grade}, '{student.email}', '{student.password}');
        """)
        self.conn.commit()
        return f"Student {student.name} inserted in database"

    def get_student_email(self, email)->Student:
        self.cursor.execute(f"""
            SELECT * FROM students WHERE email = '{email}';
        """)
        student = self.cursor.fetchone()
        if student:
            return Student(id=student[0], name=student[1], age=student[2], grade=student[3], email=student[4], password=student[5])
        else:
            return Student(id=-1,name='', age=0, grade=0, email='', password='')

rds_controller = RDSController()