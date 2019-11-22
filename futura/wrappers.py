import wurst as w
import brightway2 as bw2
from .utils import *
from .storage import storage
import os
from copy import deepcopy
from bw2io.strategies.generic import link_iterable_by_fields

try:
    import _pickle as pickle
except:
    print('falling back on pickle')
    import pickle

import zlib


class FuturaDatabase:

    """
    TODO: Write doctring
    """

    def __init__(self):  # , project_name=None, database_names=None, save_db_file=True):

        self.db = []
        self.database_names = []

        """
        if not database_names:
            database_names = []

        if isinstance(database_names, str):
            database_names = [database_names]

        self.database_names = database_names

        if database_names:
            self.extract_databases(project_name, database_names)

            if save_db_file:
                # TODO: Get rid of this try except statement
                try:
                    self.save()
                except:
                    print('something went wrong')
        """
    def extract_bw2_database(self, project_name, database_names):

        if isinstance(database_names, str):
            database_names = [database_names]
        assert project_name in bw2.projects, "That project doesn't exist"
        assert isinstance(self.database_names, (list, tuple, set)), "Must pass list of database names"

        self.database_names.extend(database_names)

        bw2.projects.set_current(project_name)

        input_db = w.extract_brightway2_databases(database_names)

        fix_unset_technosphere_and_production_exchange_locations(input_db)
        #remove_nones(input_db)

        self.db.extend(input_db)

    def extract_excel_data(self, excelfilepath):
        sp = bw2.ExcelImporter(excelfilepath)

        # link the biosphere exchanges
        sp.apply_strategies(verbose=False)

        # make the internal links
        sp.match_database(fields=["name", "unit", "location"])

        # make the links to existing data
        link_iterable_by_fields(sp.data, self.db, fields=["reference product", "name", "unit", "location"])
        link_iterable_by_fields(sp.data, self.db, fields=["name", "unit", "location"])

        if sp.statistics()[2] != 0:
            fp = sp.write_excel()
            print(fp)
            assert sp.statistics()[2] == 0, "Unlinked exchanges"

        fix_products_and_locations_external(sp.data, self.db)

        self.db.extend(sp.data)

    def write_database(self, project, name, overwrite=False):

        assert project in bw2.projects, "That project doesn't exist"

        if bw2.projects.current != project:
            bw2.projects.set_current(project)

        if name in bw2.databases:
            if not overwrite:
                assert 0, 'Database already exists, either use overwrite=True, or use another name'
            else:
                print('Deleting existing database {}'.format(name))
                del bw2.databases[name]

        w.write_brightway2_database(self.db, name)

    def save(self, save_directory=None, save_filename=None):

        assert self.database_names, 'Nothing to save yet'

        if save_directory is None:
            save_directory = storage.data_dir
            print("Saving to default directory({})".format(save_directory))

        if save_filename is None:
            save_filename = "{}.fdb".format("-".join(self.database_names))
            print("Saving as default filename({})".format(save_filename))

        save_path = os.path.join(save_directory, save_filename)

        with open(save_path, 'wb') as f:
            f.write(zlib.compress(pickle.dumps(self)))

        print('Saved to {}'.format(save_path))

    def load(self, load_path):

        assert self.db == [], "Can only load data into a blank instance of FuturaDatabase"

        with open(load_path, 'rb') as f:
            assert load_path[-4:] == '.fdb', "Not a valid file path"
            print("Loading fdb file from {}".format(load_path))
            loaded = pickle.loads(zlib.decompress(f.read()))

        self.db = loaded.db
        self.database_names = loaded.database_names
        print("Loaded {} with a total of {} activities".format(", ".join(self.database_names), len(self.db)))









