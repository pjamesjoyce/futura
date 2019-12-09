#import wurst as w
import tempfile

from wurst.brightway.extract_database import add_input_info_for_indigenous_exchanges

from . import w
from . import session, futura_action, warn
import brightway2 as bw2
from .utils import *
from .storage import storage
import os
from copy import deepcopy
from bw2io.strategies.generic import link_iterable_by_fields

try:
    import _pickle as pickle
except ImportError:
    print('falling back on pickle')
    import pickle

import zlib

from .proxy import WurstDatabase
from eidl import EcoinventDownloader
import getpass


class FuturaDatabase:

    """
    TODO: Write doctring
    """

    def __init__(self):  # , project_name=None, database_names=None, save_db_file=True):

        self.db = WurstDatabase()
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

    def __repr__(self):
        return "FuturaDatabase with {} items".format(len(self.db))

    @futura_action(session)
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

    #@futura_action(session)
    def extract_excel_data(self, excelfilepath):
        sp = bw2.ExcelImporter(excelfilepath)

        # link the biosphere exchanges
        sp.apply_strategies(verbose=False)

        # make the internal links
        sp.match_database(fields=["name", "unit", "location"])

        # make the links to existing data
        still_unlinked = link_iterable_by_fields(sp.data, self.db, fields=["reference product", "name", "unit", "location"])
        still_unlinked = link_iterable_by_fields(still_unlinked, self.db, fields=["name", "unit", "location"])

        # Change GLO to RoW
        if still_unlinked:
            for x in still_unlinked:
                for exc in x.get('exchanges', []):
                    if not exc.get("input"):
                        if exc['location'] == 'GLO':
                            exc['location'] = 'RoW'

            still_unlinked = link_iterable_by_fields(still_unlinked, self.db, fields=["name", "unit", "location"])

        # Make processes less specific, by snipping off trailing descriptions (e.g. ', at user', ', metallurgical' etc.)
        if still_unlinked:
            attempts = 2
            for i in range(attempts):
                for x in still_unlinked:
                    for exc in x.get('exchanges', []):
                        if not exc.get("input"):
                            if exc['name'].rfind(',') != -1:
                                exc['name'] = exc['name'][:exc['name'].rfind(',')]

                still_unlinked = link_iterable_by_fields(still_unlinked, self.db, fields=["name", "unit", "location"])

        # Try switching despecified items back to GLO
        if still_unlinked:
            for x in still_unlinked:
                for exc in x.get('exchanges', []):
                    if not exc.get("input"):
                        if exc['location'] == 'RoW':
                            exc['location'] = 'GLO'

            still_unlinked = link_iterable_by_fields(still_unlinked, self.db, fields=["name", "unit", "location"])

        if sp.statistics()[2] != 0:
            fp = sp.write_excel()
            print(fp)
            assert sp.statistics()[2] == 0, "Unlinked exchanges"

        fix_products_and_locations_external(sp.data, self.db)

        self.db.extend(sp.data)

    def get_ecoinvent(self, db_name=None, download_path=None, store_download=True, **kwargs):

        """
        Download and import ecoinvent to FuturaDatabase
        Optional kwargs:
            db_name: name to give imported database (string) default is downloaded filename
            download_path: path to download .7z file to (string) default is download to temporary directory (.7z file is deleted after import)
            store_download: store the .7z file for later reuse, default is True, only takes effect if no download_path is provided
            username: ecoinvent username (string)
            password: ecoivnent password (string)
            version: ecoinvent version (string), eg '3.5'
            system_model: ecoinvent system model (string), one of {'cutoff', 'apos', 'consequential'}
        """
        username = kwargs.get('username')
        password = kwargs.get('password')
        version = str(kwargs.get('version'))
        system_model = kwargs.get('system_model')
        write_config = False

        if not username or not password:
            config = storage.config
            ecoinvent = config.get('ecoinvent')
        if not username:
            if ecoinvent:
                username = ecoinvent.get('username')

        if not password:
            if ecoinvent:
                password = ecoinvent.get('password')

        if not username:
            username = input('ecoinvent username: ')
            ecoinvent['username'] = username
            write_config = True

        if not password:
            password = getpass.getpass('ecoinvent password: ')
            ecoinvent['password'] = password
            write_config = True

        if write_config:
            storage.write_config(config)

        with tempfile.TemporaryDirectory() as td:
            if download_path is None:
                if store_download:
                    download_path = storage.ecoinvent_dir
                else:
                    download_path = td

            downloader = EcoinventDownloader(outdir=download_path,
                                             username=username,
                                             password=password,
                                             version=version,
                                             system_model=system_model)
            downloader.run()
            print('Extracting datasets to temporary directory {}'.format(td))
            downloader.extract(target_dir=td)

            if not db_name:
                db_name = "ecoinvent_{}".format(downloader.file_name.replace('.7z', ''))
            datasets_path = os.path.join(td, 'datasets')
            importer = bw2.SingleOutputEcospold2Importer(datasets_path, db_name)

        if 'biosphere3' not in bw2.databases:
            bw2.create_default_biosphere3()

        importer.apply_strategies()
        datasets, exchanges, unlinked = importer.statistics()

        add_input_info_for_indigenous_exchanges(importer.data, [db_name])

        if not unlinked:
            self.db.extend(importer.data)
            self.database_names.append(db_name)

    def write_database(self, project, name, overwrite=False):

        if project not in bw2.projects:
            warn("The project '{}' doesn't exist, it will be created".format(project))

        if bw2.projects.current != project:
            bw2.projects.set_current(project)

        if 'biosphere3' not in bw2.databases:
            bw2.bw2setup()

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









