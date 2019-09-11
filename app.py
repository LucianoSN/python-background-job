import uuid
import threading
import time
import requests
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# CONFIG # ******************************************

config_server = 'http://127.0.0.1:5000'


# DATA # ******************************************

queue = []

database = [
    'STORED - b5149678-b646-4e03-8b14-10da2996e0e0',
    'STORED - 0e9423a0-e2a5-4fed-a369-54e111e419d8',
    'STORED - de4eefca-9c9c-4e0c-a8ac-75e436598425',
    'STORED - dcaaa146-97df-4e02-b150-b18dd7dbc737',
    'STORED - b6f28a7d-0cd3-4c7b-9848-dae95dc3cdd8',
    'STORED - 3f8bf543-a28b-4279-bc8f-d1c7e7a0d719',
    'STORED - 2b6ead0d-79b4-452d-b652-3a093f9e1974',
    'STORED - cdc671fd-0003-462c-b134-dad336c4a862',
    'STORED - 05dc72da-e3ea-42ff-9996-d0f4282990f9',
    'STORED - f7f07b34-b0ad-46c1-ac89-e06f034e7782',
    'STORED - e75ff5b1-5f00-4296-9b92-d9310561c808'
]


# TASK # ******************************************

@app.before_first_request
def activate_job():
    def run_job():
        while True:
            print("--- Run recurring task ---")

            if len(queue) > 0:
                for item in queue:
                    print('EXEC: {}'.format(item))
                    time.sleep(5)
                    queue.remove(item)

            time.sleep(1)

    thread = threading.Thread(target=run_job)
    thread.start()


# BOOTSTRAP THREAD # ******************************************

def load_database():
    if len(database) > 0:
        for item in database:
            queue.append(item)


def background_job():
    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.get('{}/online'.format(config_server))
                if r.status_code == 200:
                    load_database()
                    not_started = False
            except:
                print('Waiting server start')

            time.sleep(2)

    thread = threading.Thread(target=start_loop)
    thread.start()


# PROCESS QUEUE # ******************************************


class ProcessQueue(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('action', type=str, help='Describe action')

    @staticmethod
    def get():
        return {'queues': queue}

    @staticmethod
    def post():
        args = ProcessQueue.parser.parse_args()

        queue.append('{} - {}'.format(args['action'], uuid.uuid4()))
        return {'queues': queue}


# ROUTES # ******************************************

@app.route("/online")
def running():
    return "Server is running!"


api.add_resource(ProcessQueue, '/queue')

# MAIN # ******************************************

if __name__ == '__main__':
    background_job()
    app.run(debug=True, threaded=True)
