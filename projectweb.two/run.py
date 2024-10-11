import eventlet
eventlet.monkey_patch()

from modules import app,db,socketio



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app,port=3000,debug=True)

