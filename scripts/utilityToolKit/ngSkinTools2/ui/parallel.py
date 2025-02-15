from threading import Thread

from maya import utils

from ngSkinTools2.api.python_compatibility import Object


class ParallelTask(Object):
    def __init__(self):
        self.__run_handlers = []
        self.__done_handlers = []

    def add_run_handler(self, handler):
        self.__run_handlers.append(handler)

    def add_done_handler(self, handler):
        self.__done_handlers.append(handler)

    def start(self, async_exec=True):
        def done():
            for i in self.__done_handlers:
                i(self)

        def thread():
            for i in self.__run_handlers:
                i(self)
            if async_exec:
                utils.executeDeferred(done)
            else:
                done()

        self.current_thread = Thread(target=thread)
        if async_exec:
            self.current_thread.start()
        else:
            self.current_thread.run()

    def wait(self):
        self.current_thread.join()
