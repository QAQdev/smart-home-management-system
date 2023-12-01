import functools
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import session
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

username = 'root'
password = '12345'
port = '3306'
database = 'bs_manage'

DB_URI = 'mysql+pymysql://%s:%s@localhost:%s/%s' % (username, password, port, database)

db_engine = create_engine(DB_URI, encoding='utf-8')

state_code = {
    'success': 0,
    'error': 1,
    'user_exists': 2,
    'user_not_exist': 3,
    'phone_exists': 4,
    'same_password': 5,
    'scene_not_exist': 6,
    'need_login': 7,
    'room_not_exist': 8,
    'device_create_error': 10,
    'device_not_exist': 12,
}

def make_session():
    return sessionmaker(bind=db_engine)()

def need_login(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            return function(*args, **kwargs)
        else:
            return {"state": state_code["need_login"]}
    return wrapper

# class Device(db.Model):
#     __tablename__ = 'device'

#     device_id = db.Column(db.Integer, primary_key=True)
#     device_name = db.Column(db.String(128))
#     device_info = db.Column(db.String(128))
#     device_pos_x = db.Column(db.Float(asdecimal=True), nullable=False, server_default=db.FetchedValue())
#     device_pos_y = db.Column(db.Float(asdecimal=True), nullable=False, server_default=db.FetchedValue())
#     room_id = db.Column(db.ForeignKey('room.room_id'), nullable=False, index=True)
#     device_type = db.Column(db.Enum('light', 'door_lock', 'sensor', 'switch'), nullable=False)

#     room = db.relationship('Room', primaryjoin='Device.room_id == Room.room_id', backref='devices')



# class Room(db.Model):
#     __tablename__ = 'room'

#     room_name = db.Column(db.String(128))
#     room_id = db.Column(db.Integer, primary_key=True)
#     scene_id = db.Column(db.ForeignKey('scene.scene_id'), nullable=False, index=True)

#     scene = db.relationship('Scene', primaryjoin='Room.scene_id == Scene.scene_id', backref='rooms')



# class Scene(db.Model):
#     __tablename__ = 'scene'

#     scene_name = db.Column(db.String(128))
#     scene_id = db.Column(db.Integer, primary_key=True)
#     user = db.Column(db.ForeignKey('user.user'), nullable=False, index=True)

#     user1 = db.relationship('User', primaryjoin='Scene.user == User.user', backref='scenes')



# class User(db.Model):
#     __tablename__ = 'user'

#     user = db.Column(db.String(128), primary_key=True)
#     password = db.Column(db.String(128), nullable=False)
#     phone = db.Column(db.String(128), nullable=False, unique=True)


# class Log(db.Model):
#     __tablename__ = 'log'

#     scene_name = db.Column(db.String(50), primary_key=True, nullable=False)
#     room_name = db.Column(db.String(50), primary_key=True, nullable=False)
#     device_name = db.Column(db.String(50), primary_key=True, nullable=False)
#     log = db.Column(db.String(200), primary_key=True, nullable=False)