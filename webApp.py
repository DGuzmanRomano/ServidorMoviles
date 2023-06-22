from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://d:123456@localhost/guard'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Parents(db.Model):
    ParentID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80), nullable=False)
    LastName = db.Column(db.String(80), nullable=False)

class ParentsSchema(ma.Schema):
    class Meta:
        fields = ('ParentID', 'FirstName', 'LastName')

parents_schema = ParentsSchema()
all_parents_schema = ParentsSchema(many=True)

class Kids(db.Model):
    KidID = db.Column(db.Integer, primary_key=True)
    ParentID = db.Column(db.Integer, db.ForeignKey('parents.ParentID'), nullable=False)
    FirstName = db.Column(db.String(80), nullable=False)
    LastName = db.Column(db.String(80), nullable=False)
    GroupID = db.Column(db.Integer, nullable=False)  # you can also make this a ForeignKey if the groups table exists

class KidsSchema(ma.Schema):
    class Meta:
        fields = ('KidID', 'ParentID', 'FirstName', 'LastName', 'GroupID')

kids_schema = KidsSchema()
all_kids_schema = KidsSchema(many=True)

class Records(db.Model):
    RecordID = db.Column(db.Integer, primary_key=True)
    KidID = db.Column(db.Integer, db.ForeignKey('kids.KidID'), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    EnterTime = db.Column(db.Time, nullable=False)
    ExitTime = db.Column(db.Time, nullable=False)
    MealCount = db.Column(db.Integer, nullable=False)
    BathroomCount = db.Column(db.Integer, nullable=False)
    Menu = db.Column(db.String(100), nullable=False)

class RecordsSchema(ma.Schema):
    class Meta:
        fields = ('RecordID', 'KidID', 'Date', 'EnterTime', 'ExitTime', 'MealCount', 'BathroomCount', 'Menu')

records_schema = RecordsSchema()
all_records_schema = RecordsSchema(many=True)

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

# Add similar routes for Kids and Records tables

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
    KidID = request.json['KidID']
    Date = request.json['Date']
    EnterTime = request.json['EnterTime']
    ExitTime = request.json['ExitTime']
    MealCount = request.json['MealCount']
    BathroomCount = request.json['BathroomCount']
    Menu = request.json['Menu']
    new_record = Records(KidID=KidID, Date=Date, EnterTime=EnterTime, ExitTime=ExitTime, MealCount=MealCount, BathroomCount=BathroomCount, Menu=Menu)
    db.session.add(new_record)
    db.session.commit()
    return records_schema.jsonify(new_record)

@app.route('/record', methods=['GET'])
def get_records():
    all_records = Records.query.all()
    result = all_records_schema.dump(all_records)
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

