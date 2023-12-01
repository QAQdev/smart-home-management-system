from components.headers import *
import random, json

user = Blueprint('user', __name__)

@user.route("/signup", methods=["POST"])
def register():

    db_session = make_session()
    
    data = request.values

    user = data.get('user')
    password = data.get('password')
    phone = data.get('phone')

    query = db_session.query(User).filter(User.user == user).all()

    if query != []:
        db_session.close()
        return jsonify({'state': state_code['user_exists']})

    query = db_session.query(User).filter(User.phone == phone).all()

    if query != []:
        db_session.close()
        return jsonify({'state': state_code['phone_exists']})
    else:
        db_session.add(User(user=user, password=password, phone=phone))
        db_session.commit()
        db_session.close()
        session['user'] = user
        return jsonify({'state': state_code['success']})


@user.route("/signin", methods=["POST"])
def signIn():

    db_session = make_session()

    data = request.values
    username = data.get('user')
    password = data.get('password')

    query = db_session.query(User).filter(User.user == username).all()

    if not query:
        db_session.close()
        return jsonify({'state': state_code['user_not_exist']})
    
    query = db_session.query(User).filter(User.password == password).all()
    
    if not query:
        db_session.close()
        return jsonify({'state':state_code['error']})
    
    db_session.close()
    session['user'] = username
    return jsonify({'state': state_code['success'], 'phone':query[0].phone})
    

@user.route("/modify", methods=["POST"])
@need_login
def modify():
    db_session = make_session()

    data = request.values
    username = session.get('user')
    new_pwd = data.get('password')

    query = db_session.query(User).filter(User.user == username).all()

    if query == []:
        db_session.close()
        return jsonify({'state': state_code['user_not_exist']})

    if new_pwd == query[0].password:
        db_session.close()
        return jsonify({'state': state_code['same_password']})
    else:
        db_session.query(User).filter(User.user == username).update({'password': new_pwd})
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