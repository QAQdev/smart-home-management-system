from os import urandom
from flask import Flask
from components.user import user
from components.scene import scene
from components.room import room
from components.device import device

app = Flask(__name__)
app.secret_key = urandom(32)

app.register_blueprint(user, url_prefix='/accounts')
app.register_blueprint(scene, url_prefix='/scene')
app.register_blueprint(device, url_prefix='/device')
app.register_blueprint(room, url_prefix='/room')

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000, 
        host="0.0.0.0"
    )