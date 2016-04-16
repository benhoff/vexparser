import zmq


class Messaging:
    def __init__(self, parser, context=None, **kwargs):
        """
        kwargs:
            subscription_address needs to be an iterable
            publish_address needs to be a string
        """
        self.parser = parser
        context = context or zmq.Context()
        # inputs are going to be subscriptions
        self.subscription_socket = context.socket(zmq.SUB)
        self.subscription_socket.setsockopt(zmq.SUBSCRIBE, b'')
        for addr in kwargs['subscription_address']:
            self.subscription_socket.connect(addr)

        self.publish_socket = context.socket(zmq.PUB)
        self.publish_socket.bind(kwargs['publish_address'])

    def run(self):
        while True:
            frame = self.subscription_socket.recv_pyobj()
            if len(frame) == 4:
                msg = frame.pop()

            parse_result = self.parser.parse(msg)
            for result in parse_result:
                frame = ['vex', 'MSG', 'vex', result]
                self.publish_socket.send_pyobj(frame)
