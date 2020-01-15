#import wurst as w
import tempfile

from wurst.brightway.extract_database import add_input_info_for_indigenous_exchanges

from . import w
from . import warn
#import brightway2 as bw2

from bw2data import projects, databases
from bw2io import ExcelImporter, SingleOutputEcospold2Importer, bw2setup, create_core_migrations, migrations

from .utils import *
from .storage import storage
from .constants import DEFAULT_SETUP_PROJECT
from .ecoinvent import check_database
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
try:
    from eidl import EcoinventDownloader
except ImportError:
    warn('eidl not found')
import getpass


class FuturaDatabase:

    """
    TODO: Write doctring

    :ivar db: database
    :vartype db: :class:`~futura.proxy.WurstDatabase`
    """

    def __init__(self):

        self.db = WurstDatabase()
        self.database_names = []

    def __repr__(self):
        return "FuturaDatabase with {} items".format(len(self.db))

    def extract_bw2_database(self, project_name, database_name):

        if isinstance(database_name, str):
            database_names = [database_name]
        assert project_name in projects, "That project doesn't exist"
        assert isinstance(self.database_names, (list, tuple, set)), "Must pass list of database names"

        self.database_names.extend(database_names)

        projects.set_current(project_name)

        input_db = w.extract_brightway2_databases(database_names)

        fix_unset_technosphere_and_production_exchange_locations(input_db)
        #remove_nones(input_db)

        self.db.extend(input_db)
        print(self.db)

    def extract_excel_data(self, excelfilepath):

        print(excelfilepath)

        sp = ExcelImporter(excelfilepath)

        if not migrations:
            create_core_migrations()

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
                        if exc.get('location') == 'GLO':
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
        self.database_names.append(sp.db_name)

    def get_ecoinvent(self, db_name=None, download_path=None, store_download=True, **kwargs):

        """
        Download and import ecoinvent to FuturaDatabase. Sets :attr:`~db` directly

        Optional kwargs:

        :param db_name: name to give imported database. Default is downloaded filename
        :type db_name: str, optional

        :param download_path: path to download .7z file to default is download to temporary directory
            (.7z file is deleted after import)
        :type download_path: str, optional

        :param store_download: store the .7z file for later reuse, default is True, only takes effect if
            no download_path is provided
        :type store_download: bool, optional

        :param username: ecoinvent username
        :type username: str, optional

        :param password: ecoinvent password
        :type password: str, optional

        :param version: ecoinvent version, eg '3.5'
        :type version: str, optional

        :param system_model: ecoinvent system model, one of {'cutoff', 'apos', 'consequential'}
        :type system_model: str, optional

        :return: None
        :rtype: None
        """
        username = kwargs.get('username')
        password = kwargs.get('password')
        version = str(kwargs.get('version'))
        system_model = kwargs.get('system_model')
        write_config = False

        if version and system_model:
            print("Attempting to find stored version of ecoinvent {} {})".format(version,
                                                                                 system_model))

            check_database_name = "ecoinvent_{}{}".format(system_model,
                                                          str(version).replace('.', ''))

            check = check_database(DEFAULT_SETUP_PROJECT, check_database_name)

            if check:
                print("Found an existing version - extracting that")
                self.extract_bw2_database(DEFAULT_SETUP_PROJECT, check_database_name)
                return

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
            importer = SingleOutputEcospold2Importer(datasets_path, db_name)

        current_project = projects.current

        projects.set_current(DEFAULT_SETUP_PROJECT)

        if 'biosphere3' not in databases:
            bw2setup()

        if not migrations:
            create_core_migrations()

        importer.apply_strategies()
        datasets, exchanges, unlinked = importer.statistics()
        if not unlinked:
            importer.write_database()

        projects.set_current(current_project)

        for ds in importer.data:
            if 'parameters' in ds.keys():
                parameters, parameters_full = convert_parameters_to_wurst_style(ds['parameters'])
                ds['parameters'] = parameters
                ds['parameters full'] = parameters_full

        add_input_info_for_indigenous_exchanges(importer.data, [db_name])

        if not unlinked:
            self.db.extend(importer.data)
            self.database_names.append(db_name)

    def write_database(self, project, name, overwrite=False):

        if project not in projects:
            warn("The project '{}' doesn't exist, it will be created".format(project))

        if projects.current != project:
            projects.set_current(project)

        if 'biosphere3' not in databases:
            bw2setup()

        if name in databases:
            if not overwrite:
                assert 0, 'Database already exists, either use overwrite=True, or use another name'
            else:
                print('Deleting existing database {}'.format(name))
                del databases[name]

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









