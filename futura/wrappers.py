import wurst as w
import brightway2 as bw2
from .utils import *
from .storage import storage
import os
from copy import deepcopy

try:
    import _pickle as pickle
except:
    print('falling back on pickle')
    import pickle

import zlib

class WurstDatabase:

    """
    TODO: Write doctring
    """

    def __init__(self, project_name, database_names, save_db_file = True):

        self.db = {}
        self.bwdb = {}
        self.project_name = project_name

        if isinstance(database_names, str):
            database_names = [database_names]

        self.database_names = database_names
        self.extract_databases(project_name, database_names)
        if save_db_file:
            try:
                self.save()
            except:
                print('something went wrong')

    def extract_databases(self, project_name, database_names):

        ERROR = "Must pass list of database names"

        assert isinstance(self.database_names, (list, tuple, set)), ERROR


        bw2.projects.set_current(project_name)

        for db in database_names:

            self.bwdb[db] = bw2.Database(db)

        try:
            self.db = self.load()
        except:
            print("Couldn't load anything, building from scratch")


            input_db = w.extract_brightway2_databases(database_names)

            fix_unset_technosphere_and_production_exchange_locations(input_db)
            remove_nones(input_db)

            self.db = input_db

    def write_database(self, name, project=None):

        if project is None:
            project = self.project_name

        if bw2.projects.current != project:
            bw2.projects.set_current(project)

        w.write_brightway2_database(self.db, name)


    def save(self, save_directory=None, save_filename=None):

        if save_directory is None:
            save_directory = storage.data_dir
            print(save_directory)

        if save_filename is None:
            save_filename = "{}--{}.fdb".format(self.project_name, "-".join(self.database_names))

        save_path = os.path.join(save_directory, save_filename)

        with open(save_path, 'wb') as f:
            f.write(zlib.compress(pickle.dumps(self.db)))

        print('Saved to {}'.format(save_path))

    def load(self, load_path=None):

        if load_path is None:
            directory = storage.data_dir
            filename = "{}--{}.fdb".format(self.project_name, "-".join(self.database_names))
            load_path = os.path.join(directory, filename)
            print("Loading fdb file from {}".format(load_path))

        with open(load_path, 'rb') as f:
            loaded_database = pickle.loads(zlib.decompress(f.read()))

        print("Loaded database from {} with {} activities".format(filename, len(loaded_database)))
        return loaded_database









