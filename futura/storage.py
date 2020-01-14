import os
import appdirs
import glob
import yaml
from .constants import DEFAULT_CONFIG


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

        # ecoinvent versions
        self.ecoinvent_dir = os.path.join(self.futura_dir, 'ecoinvent')
        if not os.path.isdir(self.ecoinvent_dir):
            os.mkdir(self.ecoinvent_dir)


        # config
        self.config_file = os.path.join(self.futura_dir, 'futura_config.yml')
        if not os.path.exists(self.config_file):
            self.write_default_config()

    @property
    def databases(self):
        futura_databases = glob.glob(os.path.join(self.data_dir), '*.fdb')
        return futura_databases

    @property
    def ecoinvent_versions(self):
        versions = glob.glob(os.path.join(self.data_dir), '*.7z')
        return versions

    @property
    def config(self):
        with open(self.config_file, 'r') as cf:
            config = yaml.safe_load(cf)
        if config is None:
            self.write_default_config()
            config = DEFAULT_CONFIG
        return config

    def write_default_config(self):
        self.write_config(DEFAULT_CONFIG)

    def write_config(self, config):
        with open(self.config_file, 'w') as cfg:
            yaml.safe_dump(config, cfg, default_flow_style=False)

storage = FuturaStorage()