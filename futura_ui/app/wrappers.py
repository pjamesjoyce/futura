from PySide2.QtCore import QTimer, SIGNAL, SLOT

from futura.recipe_parser import FuturaLoader
from futura.wrappers import FuturaDatabase
from .signals import signals
from .ui.dialogs.progress import DefinedProgress
from .utils import findMainWindow
from PySide2.QtWidgets import QProgressDialog
from PySide2.QtCore import Qt
from .threads import FunctionThread, GeneratorThread


class FuturaGuiLoader(FuturaLoader):

    def __init__(self, *args, **kwargs):
        print('this is a FuturaGuiLoader')

        self.thread = GeneratorThread(self.run_generator, 4)

        super(FuturaGuiLoader, self).__init__(*args, **kwargs)

        self.database = FuturaDatabase()

        self.connect_signals()

        # print('this is a FuturaGuiLoader')
        #
        # self.thread = GeneratorThread(self.run_generator)

        #self.progress = QProgressDialog('Load', 'cancel', 0, 50, findMainWindow().centralWidget())

    def run_generator(self):
        yield 0

        self.database = self.parse_load_section()
        yield 1

        if 'technology' in self.recipe.keys():
            self.parse_technology_section()
        yield 2

        if 'markets' in self.recipe.keys():
            self.parse_market_section()
        yield 3

    def run(self):
        print('starting thread')
        signals.change_status_message.emit('Loading Recipe Data...')

        progress = QProgressDialog('Loading Recipe Data...', None, 0, 4, findMainWindow().centralWidget())
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle('Loading...')
        signals.thread_progress.connect(progress.setValue)
        self.thread.start()
        print('thread started...')

    def print_progress(self, progress):
        print("##### PROGRESS UPDATE #####\n\n{} steps completed \n\n###############################".format(progress))

    def connect_signals(self):
        signals.thread_progress.connect(self.print_progress)
