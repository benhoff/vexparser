class MarkParser:
    def __init__(self, mark='!'):
        self.mark = mark
        self.callback_managers = []

    def add_callback_manager(self, manager):
        self.callback_managers.append(manager)

    def remove_callback_manager(self, manager):
        self.callback_managers.remove(manager)

    def is_marked(self, text: str):
        if text[0] == self.mark:
            return True

        return False

    def parse(self, text: str):
        results = []
        if self.is_marked(text):
            # get rid of any whitespace
            command = text.lstrip()
            command = command.replace(self.mark, '')
            command = command.strip()

            for manager in self.callback_managers:
                results.extend(manager.call_callback(command))

        return results
