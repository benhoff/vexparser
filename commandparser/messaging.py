import zmq
import commandparser.util as util


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
        self._memory = {}
        self._counter = 0

    def run(self):
        while True:
            frame = self.subscription_socket.recv_pyobj()
            # add one to the counter 
            self._counter += 1
            if len(frame) == 4:
                msg = frame.pop()
                msg = util.clean_text(msg)
                parse_result = self.parser.parse(msg)
                # give the chat gui a chance to respond
                for result in parse_result:
                    past_count = self._memory.get(result, 0)
                    # check to see if this was responded to recently and
                    # not respond if so
                    count_difference = self._counter - past_count
                    if self._counter - past_count > 10 or past_count == 0:
                        frame = ['listener', 'MSG', 'vex', result]
                        self.publish_socket.send_pyobj(frame)
                        self._memory[result] = self._counter
