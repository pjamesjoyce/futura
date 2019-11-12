import os
import appdirs
import glob

class FuturaStorage():
    def __init__(self):
        self.futura_dir = appdirs.user_data_dir(
            appname='Futura',
            appauthor='Futura'
        )
        if not os.path.isdir(self.futura_dir):
            os.makedirs(self.futura_dir)

        # Databases
        self.data_dir = os.path.join(self.futura_dir, 'databases')
        if not os.path.isdir(self.data_dir):
            os.mkdir(self.data_dir)

        # recipe files
        self.recipe_dir = os.path.join(self.futura_dir, 'recipes')
        if not os.path.isdir(self.recipe_dir):
            os.mkdir(self.recipe_dir)

        # config
        # self.config_file = os.path.join(self.futura_dir, 'lcopt_config.yml')
        # if not os.path.exists(self.config_file):
        #     self.write_default_config()

        # self.config = self.load_config()

    @property
    def databases(self):
        databases = glob.glob(os.path.join(self.data_dir), '*.fdb')
        return databases

storage = FuturaStorage()