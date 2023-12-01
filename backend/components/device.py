from components.headers import *

device = Blueprint('device', __name__)

device_types = ['light', 'door_lock', 'sensor', 'switch']

init_val = {
    'light': 0,
    'sensor': randint(20, 30),
    'door_lock': 1,
    'switch': 1
}

@device.route("/install", methods=["POST"])
@need_login
def create():

    db_session = make_session()
    
    data = request.values
    
    device_name = data.get('device_name')
    device_type = data.get('device_type')
    room_id = data.get('room_id')
    device_info = init_val[device_type]
    
    if(device_type == 'sensor'):
        device_info = randint(21,29)
    
    if device_type not in device_types or room_id is None:
        return jsonify({'state': state_code['error']})
    
    db_session.add(Device(device_name=device_name,
                        device_type=device_type,
                        device_info=device_info,
                        room_id=room_id))
    
    querySet = db_session.query(Device).filter(Device.device_name == device_name).order_by(Device.device_id.desc()).all()

    device_id = querySet[0].device_id
        
    db_session.commit()
    db_session.close()

    return jsonify({
        'device_id': device_id,
        'device_name': device_name,
        'device_type': device_type,
        'device_info': device_info,
        'x': 10,
        'y': 10,
        'room_id': room_id,
    })


@device.route("/getall", methods=["POST"])
@need_login
def getAll():

    db_session = make_session()
    room_id = request.values.get('room_id')
    query = db_session.query(Room).filter(Room.room_id == room_id).all()
    
    if query == []:
        return jsonify([{'state': state_code['room_not_exist']}])
    
    devices = []
    for d in db_session.query(Device).filter(Device.room_id == room_id).all():
        devices.append({
            'device_id': d.device_id,
            'device_type': d.device_type,
            'device_info': d.device_info,
            'device_name': d.device_name,
            'x': d.device_pos_x,
            'y': d.device_pos_y
        })

    db_session.close()
    return jsonify(devices)


@device.route("/pos", methods=["POST"])
@need_login
def updatePos():
    db_session = make_session()
    data = request.values
    device_id = data.get('device_id')

    querySet = db_session.query(Device).filter(Device.device_id == device_id).all()

    if querySet == []:
        db_session.close()
        return jsonify({'state': state_code['device_not_exist']})
    else:       
        db_session.query(Device).filter(Device.device_id == device_id).update({'device_pos_x': data.get('x'),'device_pos_y':data.get('y')})
        db_session.commit()
        db_session.close()
        return jsonify({'state': state_code['success']})


@device.route("/update", methods=["POST"])
@need_login
def updateInfo():

    db_session = make_session()
    data = request.values
    device_id = data.get('device_id')

    querySet = db_session.query(Device).filter(Device.device_id == device_id).all()

    if querySet == []:
        db_session.close()
        return jsonify({'state': state_code['device_not_exist']})
    else:
        db_session.query(Device).filter(Device.device_id == device_id).update({'device_info': int(data.get('device_info'))})
        db_session.commit()
        db_session.close()
        return jsonify({'state': state_code['success']})


@device.route("/getname", methods=["POST"])
@need_login
def getName():
    data = request.values
    db_session = make_session()
    
    querySet = db_session.query(Device).filter(Device.device_id == data.get('device_id')).all()

    if querySet != []:
        return query[0].device_name
    else:
        db_session.close()
        return jsonify({'state': state_code['device_not_exist']})


@device.route("/changename", methods=["POST","GET"])
@need_login
def updateName():
    
    db_session = make_session()
    data = request.values
    device_id = data.get('device_id')

    querySet = db_session.query(Device).filter(Device.device_id == device_id).all()
    
    if querySet == []:
        db_session.close()
        return jsonify({'state': state_code['device_not_exist']})
    else:
        db_session.query(Device).filter(Device.device_id == device_id).update({'device_name': data.get('device_name')})
        db_session.commit()
        db_session.close()
        return jsonify({'state': state_code['success']})