import threading
import time
import requests

from flask import Flask
from flask_restful import Api

from MailQueue import MailQueue
from UserQueue import UserQueue

app = Flask(__name__)
api = Api(app)

# CONFIG # ******************************************

config_server = 'http://127.0.0.1:5000'


# DATA MAIL # ******************************************

queue_mail = []

database_mail = [
    '[STORED] - MAIL - b5149678-b646-4e03-8b14-10da2996e0e0',
    '[STORED] - MAIL - 0e9423a0-e2a5-4fed-a369-54e111e419d8',
    '[STORED] - MAIL - de4eefca-9c9c-4e0c-a8ac-75e436598425',
    '[STORED] - MAIL - dcaaa146-97df-4e02-b150-b18dd7dbc737',
    '[STORED] - MAIL - b6f28a7d-0cd3-4c7b-9848-dae95dc3cdd8',
    '[STORED] - MAIL - 3f8bf543-a28b-4279-bc8f-d1c7e7a0d719',
    '[STORED] - MAIL - 2b6ead0d-79b4-452d-b652-3a093f9e1974',
    '[STORED] - MAIL - cdc671fd-0003-462c-b134-dad336c4a862',
    '[STORED] - MAIL - 05dc72da-e3ea-42ff-9996-d0f4282990f9',
    '[STORED] - MAIL - f7f07b34-b0ad-46c1-ac89-e06f034e7782',
    '[STORED] - MAIL - e75ff5b1-5f00-4296-9b92-d9310561c808'
]


# DATA MAIL # ******************************************

queue_user = []

database_user = [
    '[STORED] - USER - x6849678-b646-4e03-8b14-10da2996ePnh',
    '[STORED] - USER - yl0423a0-e2a5-4fed-a369-54e111e41gdd',
]


# TASK # ******************************************

@app.before_first_request
def activate_job():
    def run_job(queue, owner, sec=3):
        while True:
            print('--- Run recurring [{}] task ---'.format(owner))

            if len(queue) > 0:
                for item in queue:
                    print('EXEC: {}'.format(item))
                    time.sleep(sec)
                    queue.remove(item)

            time.sleep(1)

    thread_mail = threading.Thread(name='mail_job', target=run_job, args=(queue_mail, 'mail', 3))
    thread_user = threading.Thread(name='user_job', target=run_job, args=(queue_user, 'user', 5))
    thread_mail.start()
    thread_user.start()


# BOOTSTRAP THREAD # ******************************************

def background_job():
    def load_database(database, queue):
        if len(database) > 0:
            for item in database:
                queue.append(item)

    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.get('{}/online'.format(config_server))
                if r.status_code == 200:
                    load_database(database_mail, queue_mail)
                    load_database(database_user, queue_user)
                    not_started = False
            except:
                print('Waiting server start')

            time.sleep(2)

    thread = threading.Thread(target=start_loop)
    thread.start()


# ROUTES # ******************************************

@app.route("/online")
def running():
    return "Server is running!"


api.add_resource(MailQueue, '/mail/queue', resource_class_kwargs={'queue': queue_mail})
api.add_resource(UserQueue, '/user/queue', resource_class_kwargs={'queue': queue_user})

# MAIN # ******************************************

if __name__ == '__main__':
    background_job()
    app.run(debug=True, threaded=True)
