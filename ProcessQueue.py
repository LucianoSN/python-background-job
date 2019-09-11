import uuid

from flask_restful import Resource, reqparse


class ProcessQueue(Resource):
    def __init__(self, **kwargs):
        self.queue = kwargs['queue']

    parser = reqparse.RequestParser()
    parser.add_argument('action', type=str, help='Describe action')

    def get(self):
        return {'queues': self.queue}

    def post(self):
        args = ProcessQueue.parser.parse_args()

        self.queue.append('{} - {}'.format(args['action'], uuid.uuid4()))
        return {'queues': self.queue}
