from crypt import methods
from flask import Flask, render_template, url_for, request, flash, session, redirect, jsonify, make_response, Blueprint, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null, ForeignKey, func, text, column


app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://javi:javi@localhost:3310/DOCTORAL'
db = SQLAlchemy(app)

class Instructor(db.Model):
    __tablename__ = 'INSTRUCTOR'

    InstructorId = db.Column(db.String(6), primary_key=True)
    FName = db.Column(db.String(15), nullable=False)
    LName = db.Column(db.String(15), nullable=False)
    StartDate = db.Column(db.Date)
    Degree = db.Column(db.String(30))
    Rank = db.Column(db.String(30))
    Type = db.Column(db.String(10))

    def __repr__(self):
        return f"Instructor(InstructorId={self.InstructorId}, FName={self.FName}, LName={self.LName}, StartDate={self.StartDate}, Degree={self.Degree}, Rank={self.Rank}, Type={self.Type})"

class PhdStudent(db.Model):
    __tablename__ = 'PHD_STUDENT'

    StudentId = db.Column(db.String(6), primary_key=True)
    FName = db.Column(db.String(15), nullable=False)
    LNname = db.Column(db.String(15), nullable=False)
    StSem = db.Column(db.String(15))
    StYear = db.Column(db.Integer, nullable=False)
    Supervisor = db.Column(db.String(6), db.ForeignKey('INSTRUCTOR.InstructorId'))

    def __repr__(self):
        return f"PhdStudent(StudentId={self.StudentId}, FName={self.FName}, LNname={self.LNname}, StSem={self.StSem}, StYear={self.StYear}, Supervisor={self.Supervisor})"

class GRA(db.Model):
    __tablename__ = 'GRA'

    StudentId = db.Column(db.String(6), primary_key=True)
    GrantID = db.Column(db.String(4), nullable=False)
    MonthlyPay = db.Column(db.Integer, nullable=False)
    MajaorResearchArea = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"GRA(StudentId={self.StudentId}, GrantID={self.GrantID}, MonthlyPay={self.MonthlyPay}, MajaorResearchArea={self.MajaorResearchArea})"

class MilestonesPassed(db.Model):
    __tablename__ = 'MILESTONESPASSED'

    StudentId = db.Column(db.String(6), db.ForeignKey('PHD_STUDENT.StudentId'), primary_key=True)
    MId = db.Column(db.String(2), primary_key=True)
    PassDate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"MilestonesPassed(StudentId={self.StudentId}, MId={self.MId}, PassDate={self.PassDate})"

class Course(db.Model):
    __tablename__ = 'COURSE'

    CourseID = db.Column(db.String(7), primary_key=True)
    CName = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return f"Course(CourseID={self.CourseID}, CName={self.CName})"

class PhdCommittee(db.Model):
    __tablename__ = 'PHDCOMMITTEE'

    StudentId = db.Column(db.String(6), primary_key=True)
    InstructorId = db.Column(db.String(6), primary_key=True)

    def __repr__(self):
        return f"PhdCommittee(StudentId={self.StudentId}, InstructorId={self.InstructorId})"

class CoursesTaught(db.Model):
    __tablename__ = 'COURSESTAUGHT'

    CourseID = db.Column(db.String(7), primary_key=True)
    InstructorId = db.Column(db.String(6), primary_key=True)

    def __repr__(self):
        return f"CoursesTaught(CourseID={self.CourseID}, InstructorId={self.InstructorId})"

def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    # Other headers can be added here if needed
    return response

@app.route("/input", methods = ['GET', 'POST'])
def input():
    try:
        data = request.get_json()

        InstructorId = data.get('InstructorId')
        FName = data.get('FName')
        LName = data.get('LName')
        StartDate = data.get('StartDate')
        Degree = data.get('Degree')
        Rank = data.get('Rank')
        Type = data.get('Type')

        existing_instructor = Instructor.query.filter_by(InstructorId=InstructorId).first()
        if existing_instructor:
            #return jsonify({'error': 'InstructorId already in use'}), 201
            return jsonify({'message': f'InstructorId already in use'}), 201
        new_instructor = Instructor(
            InstructorId=InstructorId,
            FName=FName,
            LName=LName,
            StartDate=StartDate,
            Degree=Degree,
            Rank=Rank,
            Type=Type
        )

        db.session.add(new_instructor)

        print("first")

        
        try:
            random_course = Course.query.order_by(func.rand()).first()
            print(random_course)
        except Exception as e:
            print("Error:", e)
        new_course_taught = CoursesTaught(
            CourseID=random_course.CourseID,
            InstructorId=InstructorId
        )
        db.session.add(new_course_taught)

        random_student = PhdStudent.query.order_by(func.rand()).first()

        new_committee_member = PhdCommittee(
            StudentId=random_student.StudentId,
            InstructorId=InstructorId
        )
        db.session.add(new_committee_member)

        db.session.commit()

        return jsonify({'message': f'Instructor added successfully to course {random_course.CourseID} and is assigned to student {random_student.StudentId}'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/delete", methods = ['DELETE'])
def delete():
    try:
        student_id = request.args.get('StudentId')
        print(student_id)
        if not student_id:
            return jsonify({'error': 'StudentId is required in query parameters'}), 400
        '''
        try:
            phd_student = db.session.query(PhdStudent).filter_by(StudentId=student_id).first()
            print(phd_student)
        except Exception as e:
            print("Error:", e)
        gra_student = db.session.query(GRA).filter_by(StudentId=student_id).first()
                print(gra_student)

        '''

        check = db.session.query(MilestonesPassed).filter_by(StudentId=student_id).first()
        #print(check==None)
        
        if check == None:
            #print("test")
            gra_student = db.session.query(GRA).filter_by(StudentId=student_id).first()
            #print(gra_student)
            
            if gra_student:
                db.session.delete(gra_student)

                phd_student = db.session.query(PhdStudent).filter_by(StudentId=student_id).first()
                if phd_student:
                    db.session.delete(phd_student)
                    #print("DELETED")
                db.session.commit()
                return jsonify({'message': f'Student with StudentId {student_id} deleted successfully from GRA and PhdStudent tables'}), 200
            else:
                return jsonify({'message': f'Student with StudentId {student_id} not found in GRA table'}), 404
        else:
            return jsonify({'message': f'Student with StudentId {student_id} has passed at least one milestone. Cannot delete.'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.after_request
def after_request_func(response):

    origin = request.headers.get('Origin')
    
    if request.method == 'OPTIONS':
        response = make_response()
        #response.headers.add("Access-Control-Allow-Origin", "*")
        
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, x-csrf-token, Authorization, Origin, Accept')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')

    if origin:
        #DONT ADD have to SET IT like below
        #response.headers.add('Access-Control-Allow-Origin', origin)
        
        response.headers['Access-Control-Allow-Origin'] = origin

    return response
        

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.config['SECRET_KEY'] = 'super_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'  # or another supported method
    app.config['SECURITY_PASSWORD_SALT'] = 'abc'
    app.run(debug=True, port = 9000)