from components.headers import *
import random, json

scene = Blueprint('scene', __name__)

@scene.route("/upload", methods=["POST"])
@need_login
def upload():
    file_name = request.values.get('name')
    file_base64 = request.values.get('code').strip().replace("data:image/jpeg;base64,",'')
    
    img_data = base64.b64decode(file_base64)
    
    pic = open('./pics/'+file_name+'.jpg', 'wb')
    pic.write(img_data)
    pic.close()
    
    return jsonify({'state':state_code['success']})


@scene.route("/create", methods=["POST"])
@need_login
def createScene():

    db_session = make_session()
    
    data = request.values
    user = session.get('user')
    scene_name = data.get('scene_name')

    querySet= db_session.query(User).filter(User.user == user).all()

    if querySet == []:
        db_session.close()
        return jsonify({'state': state_code['user_not_exist']})
    
    db_session.add(Scene(scene_name=scene_name, user=user))
    
    querySet = db_session.query(Scene).filter(Scene.user == user).filter(Scene.scene_name == scene_name).order_by(Scene.scene_id.desc()).all()
    
    scene_id = querySet[0].scene_id
    
    db_session.commit()
    db_session.close()

    return jsonify({
        'state': state_code['success'],
        'scene_id': scene_id,
        'scene_name': scene_name
    })
       
    
@scene.route("/getname", methods=["POST"])
@need_login
def getSceneName():
    db_session = make_session()
    data = request.values
    scene_id = data.get('scene_id')
    user = session.get('user')
    
    scenes = db_session.query(Scene).filter(Scene.scene_id == scene_id).all()
    res = []
    
    if scenes == []:
        return jsonify({
            'state':state_code['scene_not_exist']
        })
    
    return jsonify({'scene_id':scene_id,
                    'scene_name':scenes[0].scene_name,
                    'state':state_code['success']
                    })
    

@scene.route("/getall", methods=["POST"])
@need_login
def getAll():

    db_session = make_session()
    user = session.get('user')

    resSet = []
    for scene in db_session.query(Scene).filter(Scene.user == user).all():
        single_scene_info = {
            'scene_id': scene.scene_id,
            'scene_name': scene.scene_name,
            'rooms': []
        }
 
        for room in db_session.query(Room).filter(Room.scene_id == scene.scene_id).all():
            single_scene_info['rooms'].append({'room_id': room.room_id,'room_name': room.room_name})
            
        resSet.append(single_scene_info)
        
    db_session.close()
    
    return jsonify(resSet)


@scene.route("/update", methods=["POST"])
@need_login
def updateName():
    db_session = make_session()
    
    data = request.values
    scene_id = data.get("scene_id")
    scene_name = data.get("scene_name")

    querySet = db_session.query(Scene).filter(Scene.scene_id == scene_id).all()

    if querySet == []:
        db_session.close()
        return jsonify({'state': state_code['scene_not_exist']})

    db_session.query(Scene).filter(Scene.scene_id == scene_id).update({'scene_name': scene_name})
    db_session.commit()
    db_session.close()
    return jsonify({'state': state_code['success']})


@scene.route("/log", methods=["POST"])
@need_login
def writeLog():
    db_session = make_session()

    scene_name = request.values.get("scene_name")
    room_name = request.values.get("room_name")
    device_name = request.values.get("device_name")
    log = request.values.get("log")
    
    db_session.add(
        Log(scene_name=scene_name,room_name=room_name,device_name=device_name,log=log)
    )
    db_session.commit()
    db_session.close()
    
    return jsonify({'state': state_code['success']})


@scene.route("/getlog", methods=["POST"])
@need_login
def getLog():
    db_session = make_session()
    querySet= db_session.query(Log).all()
    res = []
    
    for log in querySet:
        res.append(
            {
                'scene_name':log.scene_name,
                'room_name':log.room_name,
                'device_name':log.device_name,
                'log':log.log
            }
        )
        
    return jsonify(res)

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