from PySide2.QtCore import QThread
from.signals import signals


class FunctionThread(QThread):

    def __init__(self, function):
        # QThread.__init__(self)
        super(FunctionThread, self).__init__()

        self.function = function

    def __del__(self):
        self.wait()

    def run(self):
        self.function()


class GeneratorThread(QThread):

    def __init__(self, function, iterations=None, onstatusbar=False):
        # QThread.__init__(self)
        super(GeneratorThread, self).__init__()

        self.function = function
        if iterations:
            self.iterations = iterations
        else:
            self.iterations = 0

        self.onstatusbar = onstatusbar

    def __del__(self):
        try:
            self.wait()
        except:
            pass

    def run(self):
        if self.onstatusbar:
            signals.start_status_progress.emit(self.iterations)

        for n, i in enumerate(self.function()):

            if self.onstatusbar:
                signals.update_status_progress.emit(n+1)

            signals.thread_progress.emit(n+1)

        if self.onstatusbar:
            signals.hide_status_progress.emit()

        signals.reset_status_message.emit()
