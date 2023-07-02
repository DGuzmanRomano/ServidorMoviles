from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import text



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://d:123456@localhost/guard'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Parents(db.Model):
    __tablename__ = 'Parents'
    ParentID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80), nullable=False)
    LastName = db.Column(db.String(80), nullable=False)
    Username = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)

class ParentsSchema(ma.Schema):
    class Meta:
        fields = ('ParentID', 'FirstName', 'LastName', 'Username','Password')

parents_schema = ParentsSchema()
all_parents_schema = ParentsSchema(many=True)

class Kids(db.Model):
    __tablename__ = 'Kids'
    KidID = db.Column(db.Integer, primary_key=True)
    ParentID = db.Column(db.Integer, db.ForeignKey('Parents.ParentID'), nullable=False)
    FirstName = db.Column(db.String(80), nullable=False)
    LastName = db.Column(db.String(80), nullable=False)
    GroupID = db.Column(db.Integer, nullable=False) 

class KidsSchema(ma.Schema):
    class Meta:
        fields = ('KidID', 'ParentID', 'FirstName', 'LastName', 'GroupID')

kids_schema = KidsSchema()
all_kids_schema = KidsSchema(many=True)

class Records(db.Model):
    __tablename__ = 'Records' 
    RecordID = db.Column(db.Integer, primary_key=True)
    KidID = db.Column(db.Integer, db.ForeignKey('Kids.KidID'), nullable=True)
    Date = db.Column(db.Date, nullable=True)
    EnterTime = db.Column(db.Time, nullable=True)
    ExitTime = db.Column(db.Time, nullable=True)
    MealCount = db.Column(db.Integer, nullable=True)
    BathroomCount = db.Column(db.Integer, nullable=True)
    Menu = db.Column(db.String(100), nullable=True)
    Comment = db.Column(db.String(255), nullable=True)
    MealInfo = db.Column(db.String(255), nullable=True)
    ChangeClothes = db.Column(db.Integer, nullable=True)
    Evacuations = db.Column(db.Integer, nullable=True)
    Urinations = db.Column(db.Integer, nullable=True)
    ClassIncident = db.Column(db.String(255), nullable=True)
    MedicIncident = db.Column(db.String(255), nullable=True)

class RecordsSchema(ma.Schema):
    class Meta:
        fields = ('RecordID', 'KidID', 'Date', 'EnterTime', 'ExitTime', 'MealCount', 
                  'BathroomCount', 'Menu', 'Comment', 'MealInfo', 'ChangeClothes', 
                  'Evacuations', 'Urinations', 'ClassIncident', 'MedicIncident')

records_schema = RecordsSchema()
all_records_schema = RecordsSchema(many=True)



class Teachers(db.Model):
    __tablename__ = 'Teachers'
    TeacherID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80), nullable=False)
    LastName = db.Column(db.String(80), nullable=False)
    Username = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)
    
class TeachersSchema(ma.Schema):
    class Meta:
        fields = ('TeacherID', 'FirstName', 'LastName', 'Username', 'Password')

teachers_schema = TeachersSchema()
all_teachers_schema = TeachersSchema(many=True)


class Announcements(db.Model):
    __tablename__ = 'Announcements'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Announcement = db.Column(db.String(500), nullable=False)

class AnnouncementsSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'Announcement')

announcements_schema = AnnouncementsSchema()
all_announcements_schema = AnnouncementsSchema(many=True)




####################################
########ROUTES######################

@app.route('/parent', methods=['POST'])
def add_parent():
    FirstName = request.json['FirstName']
    LastName = request.json['LastName']
    new_parent = Parents(FirstName=FirstName, LastName=LastName)
    db.session.add(new_parent)
    db.session.commit()
    return parents_schema.jsonify(new_parent)

@app.route('/parent', methods=['GET'])
def get_parents():
    all_parents = Parents.query.all()
    result = all_parents_schema.dump(all_parents)
    return jsonify(result)

@app.route('/teacher', methods=['GET'])
def get_teachers():
    all_teachers = Teachers.query.all()
    result = all_teachers_schema.dump(all_teachers)
    return jsonify(result)



@app.route('/kid', methods=['POST'])
def add_kid():
    ParentID = request.json['ParentID']
    FirstName = request.json['FirstName']
    LastName = request.json['LastName']
    GroupID = request.json['GroupID']
    new_kid = Kids(ParentID=ParentID, FirstName=FirstName, LastName=LastName, GroupID=GroupID)
    db.session.add(new_kid)
    db.session.commit()
    return kids_schema.jsonify(new_kid)

@app.route('/kid', methods=['GET'])
def get_kids():
    all_kids = Kids.query.all()
    result = all_kids_schema.dump(all_kids)
    return jsonify(result)

@app.route('/record', methods=['POST'])
def add_record():
    record_data = request.get_json()
    new_record = Records(**record_data)
    db.session.add(new_record)
    db.session.commit()
    return records_schema.jsonify(new_record)

@app.route('/record', methods=['GET'])
def get_records():
    all_records = Records.query.all()
    result = all_records_schema.dump(all_records)
    return jsonify(result)



@app.route('/announcement', methods=['POST'])
def add_announcement():
    announcement = request.json['announcement']
    new_announcement = Announcements(Announcement=announcement)
    db.session.add(new_announcement)
    db.session.commit()
    return announcements_schema.jsonify(new_announcement)

@app.route('/announcement', methods=['GET'])
def get_announcements():
    all_announcements = Announcements.query.all()
    result = all_announcements_schema.dump(all_announcements)
    return jsonify(result)







@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    parent = Parents.query.filter_by(Username=username, Password=password).first()
    if parent:
        return jsonify(success=True, role='parent', id=parent.ParentID)

    teacher = Teachers.query.filter_by(Username=username, Password=password).first()
    if teacher:
        return jsonify(success=True, role='teacher', id=teacher.TeacherID)

    return jsonify(success=False)









if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)

