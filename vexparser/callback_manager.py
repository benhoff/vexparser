class CallbackManager:
    def __init__(self):
        self._callbacks = {}

    def associate_key_with_callback(self, key, callback):
        self._callbacks[key] = callback

    def call_callback(self, key):
        """
        returns list
        """
        result = []
        # note that callback should be a function
        try:
            callback = self._callbacks[key]
            # FIXME
            result.append(callback())
        except KeyError:
            pass

        return result
