import zmq
import vexparser.util as util


class Messaging:
    def __init__(self, parsers=None, context=None, **kwargs):
        """
        kwargs:
            subscription_address needs to be an iterable
            publish_address needs to be a string
        """
        context = context or zmq.Context()
        # inputs are going to be subscriptions
        self.subscription_socket = context.socket(zmq.SUB)
        self.subscription_socket.setsockopt(zmq.SUBSCRIBE, b'')
        for addr in kwargs['subscription_address']:
            self.subscription_socket.connect(addr)

        self.publish_socket = context.socket(zmq.PUB)
        self.publish_socket.connect(kwargs['publish_address'])
        if parsers is None:
            parsers = []

        self.parsers = parsers
        self._memory = {}
        self._counter = 0

    def run(self):
        while True:
            frame = self.subscription_socket.recv_pyobj()
            # add one to the counter 
            self._counter += 1
            if len(frame) == 4:
                msg = frame.pop()
                # TODO: move into the classify parser
                # msg = util.clean_text(msg)
                parse_result = []
                for parser in self.parsers:
                    result = parser.parse(msg)
                    # TODO: do more complex parsing here
                    # currently just get the first result and stop
                    if result:
                        parse_result.extend(result)
                        break

                for result in parse_result:
                    past_count = self._memory.get(result, 0)
                    # check to see if this was responded to recently and
                    # not respond if so
                    count_difference = self._counter - past_count
                    if self._counter - past_count > 8 or past_count == 0:
                        frame = ['vex', 'MSG', 'Vex', result]
                        self.publish_socket.send_pyobj(frame)
                        self._memory[result] = self._counter
