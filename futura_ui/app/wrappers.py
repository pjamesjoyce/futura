from futura.loader import FuturaLoader
from futura.wrappers import FuturaDatabase
from futura.recipe import FuturaRecipeExecutor

from .signals import signals
from .ui.dialogs.progress import DefinedProgress
from .utils import findMainWindow
from PySide2.QtWidgets import QProgressDialog, QFileDialog
from PySide2.QtCore import Qt
from .threads import FunctionThread, GeneratorThread

class FuturaGuiLoader(FuturaLoader):

    def __init__(self, *args, **kwargs):

        self.thread = None

        super(FuturaGuiLoader, self).__init__(*args, **kwargs)

        self.database = FuturaDatabase()

        self.connect_signals()

        # print('this is a FuturaGuiLoader')
        #
        # self.thread = GeneratorThread(self.run_generator)

        #self.progress = QProgressDialog('Load', 'cancel', 0, 50, findMainWindow().centralWidget())

    def run(self):

        steps = len(self.recipe.get('actions', [])) * 2
        print("{} steps in recipe".format(steps))

        executor = FuturaRecipeExecutor(self)

        self.thread = GeneratorThread(executor.recipe_generator, steps)

        print('starting thread')

        signals.change_status_message.emit('Loading Recipe Data...')

        progress = QProgressDialog('Loading Recipe Data...', None, 0, steps, findMainWindow().centralWidget())
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle('Loading...')
        progress.show()
        signals.thread_progress.connect(progress.setValue)
        signals.thread_progress.emit(1)
        self.thread.start()
        print('thread started...')

    def save_dialog(self):

        filename, _ = QFileDialog.getSaveFileName(None,
                                                  'Save...',
                                                  # os.path.join(os.path.expanduser('~'), 'Documents'),
                                                  r'C:\Users\pjjoyce\Dropbox\00_My_Software',
                                                  "Futura Loader Files (*.fl)")
        if filename:
            self.save(filename)

    def load_dialog(self):

        print('load_dialog has been called')

        filename, _ = QFileDialog.getOpenFileName(None,
                                                  'Open Futura file...',
                                                  # os.path.join(os.path.expanduser('~'), 'Documents'),
                                                  r'C:\Users\pjjoyce\Dropbox\00_My_Software',
                                                  "Futura Loader Files (*.fl)")
        if filename:
            self.load(filename)

            signals.update_recipe.emit()
            signals.show_recipe_actions.emit()

    # TODO: Delete this!
    def load_base(self):
        filename = r"C:\Users\pjjoyce\Dropbox\00_My_Software\base.fl"
        self.load(filename)

        signals.update_recipe.emit()
        signals.show_recipe_actions.emit()



    def print_progress(self, progress):
        print("##### PROGRESS UPDATE #####\n\n{} steps completed \n\n###############################".format(progress))

    def connect_signals(self):
        signals.thread_progress.connect(self.print_progress)
        signals.save_loader.connect(self.save_dialog)
        signals.load_loader.connect(self.load_dialog)
        signals.load_base.connect(self.load_base) # TODO: Delete this
