import uuid
import threading
import time
import requests
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# CONFIG # ******************************************

config_server = 'http://127.0.0.1:5000/'


# DATA # ******************************************

data = []


# TASK # ******************************************

@app.before_first_request
def activate_job():
    def run_job():
        while True:
            print("--- Run recurring task ---")

            if len(data) > 0:
                for item in data:
                    print('EXEC: {}'.format(item))
                    time.sleep(5)
                    data.remove(item)

            time.sleep(1)

    thread = threading.Thread(target=run_job)
    thread.start()


# BOOTSTRAP THREAD # ******************************************

def background_job():
    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.get(config_server)
                if r.status_code == 200:
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
        return {'queues': data}

    @staticmethod
    def post():
        args = ProcessQueue.parser.parse_args()

        data.append('{} - {}'.format(args['action'], uuid.uuid4()))
        return {'queues': data}


# ROUTES # ******************************************

@app.route("/")
def running():
    return "Server is running!"


api.add_resource(ProcessQueue, '/queue')

# MAIN # ******************************************

if __name__ == '__main__':
    background_job()
    app.run(debug=True, threaded=True)
