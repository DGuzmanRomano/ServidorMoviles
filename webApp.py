from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://d:qazwsx123456@localhost/strings'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class String(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, value):
        self.value = value

class StringSchema(ma.Schema):
    class Meta:
        fields = ('id', 'value')

string_schema = StringSchema()
strings_schema = StringSchema(many=True)

@app.route('/string', methods=['POST'])
def add_string():
    value = request.json['value']
    new_string = String(value)
    db.session.add(new_string)
    db.session.commit()
    return string_schema.jsonify(new_string)

@app.route('/string', methods=['GET'])
def get_strings():
    all_strings = String.query.all()
    result = strings_schema.dump(all_strings)
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)