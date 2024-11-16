from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SECRET_KEY'] = '42069'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

#JWT (dimasukin ke Authorization Bearer Token Postman)
def token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token tidak diinput dengan benar'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

#route hosting
@app.route('/')
def home():
    return jsonify({'message': 'Selamat! Anda berhasil masuk API, semangat testing'})

#route regis
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User berhasil dibuat', 'id': new_user.id})

#route login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Username atau password invalid'}), 401
    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.now(datetime.timezone.utc)
 + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

#route akses database semua user, token dulu
@app.route('/users', methods=['GET'])
@token
def getallusers(current_user):
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'username': user.username}
        output.append(user_data)
    return jsonify({'users': output})

#hapus user tapi pake token
@app.route('/delete/<int:id>', methods=['DELETE'])
@token
def delete(current_user, id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'User tidak ditemukan'}), 404
    username = user.username
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User dengan ID {id}, dengan nama {username} berhasil dihapus'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
