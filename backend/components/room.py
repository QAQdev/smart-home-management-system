from components.headers import *
import random, json

room = Blueprint('room', __name__)

@room.route("/create", methods=["POST"])
@need_login
def createRoom():

    db_session = make_session()
    data = request.values
    room_name = data.get('room_name')
    scene_id = data.get('scene_id')

    query = db_session.query(Scene).filter(Scene.scene_id == scene_id).all()

    if query == []:
        db_session.close()
        return jsonify({'state': state_code['scene_not_exist']})
    else:
        db_session.add(Room(room_name=room_name, scene_id=scene_id))

        query = db_session.query(Room).filter(Room.scene_id == scene_id).filter(Room.room_name == room_name).order_by(Room.room_id.desc()).all()

        room_id = query[0].room_id

        db_session.commit()
        db_session.close()

        return jsonify({
            'state': state_code['success'],
            'room_id': room_id,
            'room_name': room_name
        })


@room.route("/getname", methods=["POST"])
@need_login
def getRoomName():
    db_session = make_session()
    
    query = db_session.query(Room).filter(Room.room_id == request.values.get('room_id')).all()
    
    if query != []:
        db_session.close()
        return jsonify({'room_name':query[0].room_name})
    else:
        db_session.close()
        return jsonify({'state':state_code['room_not_exist']})


@room.route("/getall", methods=["POST"])
@need_login
def getAll():

    db_session = make_session()
    data = request.values
    
    query = db_session.query(Room).filter(Room.scene_id == data.get('scene_id')).all()

    rooms = []
    for r in query:
        rooms.append({'room_id': r.room_id, 'room_name': r.room_name})

    db_session.close()
    return jsonify(rooms)


@room.route("/update", methods=["POST"])
@need_login
def updateName():
    db_session = make_session()

    data = request.values
    room_id = data.get("room_id")

    query = db_session.query(Room).filter(Room.room_id == room_id).all()

    if query == []:
        db_session.close()
        return jsonify({'state': state_code['room_not_exist']})
    else:
        db_session.query(Room).filter(Room.room_id == room_id).update({'room_name': data.get("room_name")})
        db_session.commit()
        db_session.close()
        return jsonify({'state': state_code['success']})
    
    
def random_arr(num):
    arr = []
    count = 0
    while count < num:
        rand = random.randint(0,19)
        if rand not in arr:
            arr.append(rand)
            count += 1
    return arr

def get_article():
    plant = request.values.get('keyword')
    result_arr = []
    with open('./src/hot.json', encoding='utf-8') as hot_file:
        result = json.load(hot_file)
        hot = result.get('hot')
        for plant_obj in hot:
            if plant_obj.get('name') == plant:
                rand_arr = random_arr(8)
                for key in range(len(plant_obj['article'])):
                    flag = False
                    for i in plant_obj['article'][key]:
                        if i == 'num' and plant_obj['article'][key].get(i) in rand_arr:
                            flag = True
                        elif flag == True:
                            obj = {"title":i, "url":plant_obj['article'][key].get(i)}
                            result_arr.append(obj)
                return jsonify({'state': state_code['success'],'result': result_arr})
            
    return jsonify({'state':state_code['error']})