class CallbackManager:
    def __init__(self):
        self._callbacks = {}

    def associate_key_with_callback(self, key, callback):
        self._callbacks[key] = callback

    def call_callback(self, key):
        """
        returns list
        """
        print(key)
        # note that callback should be a function
        try:
            callback = self._callbacks[key]
        except KeyError:
            pass

        result = callback()
        print(result)
        # FIXME
        return list(result)
