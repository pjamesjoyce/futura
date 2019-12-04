import yaml
import jinja2

from futura.markets import FuturaMarket
from futura.utils import create_filter_from_description
from .wrappers import FuturaDatabase
from . import technology
from .constants import ASSET_PATH
# import wurst as w
from . import w
from .regionalisation import create_regional_activities, create_regional_activities_from_filter
from . import session
from .ecoinvent import check_database
import os.path
import brightway2 as bw2

class FuturaLoader:

    def __init__(self, recipe_filepath=None, autocreate=True):

        self.recipe = {}
        self.database = None

        if recipe_filepath:
            self.recipe = self.load_recipe(recipe_filepath)
        else:
            autocreate = None

        if autocreate:
            self.run()

    @staticmethod
    def load_recipe(filename):

        with open(filename, "r") as f:
            template = jinja2.Template(f.read())

        t_data = template.render()
        data = yaml.load(t_data, yaml.Loader)

        return data

    def parse_load_section(self):

        assert 'load' in self.recipe.keys(), "No load section to parse"

        possible_functions = [
            'extract_bw2_database',
            'extract_excel_data'
        ]

        fd = FuturaDatabase()

        for f in self.recipe['load']:
            for k, v in f.items():

                assert k in possible_functions, "{} is not a valid load function".format(k)

                if k == 'extract_bw2_database':
                    if not check_database(v['project_name'], v['database_names'][0]):

                        print("The database defined in this recipe doesn't exist")
                        ecoinvent_version = self.recipe['metadata'].get('ecoinvent_version')
                        ecoinvent_system_model = self.recipe['metadata'].get('ecoinvent_system_model')

                        if ecoinvent_version and ecoinvent_system_model:
                            print("The recipe specifies an ecoinvent version "
                                  "(ecoinvent {} {}), attempting to download this now".format(ecoinvent_version,
                                                                                              ecoinvent_system_model))
                            fd.get_ecoinvent(db_name=v['database_names'][0],
                                             store_download=True,
                                             version=ecoinvent_version,
                                             system_model=ecoinvent_system_model)
                    else:
                        fd.extract_bw2_database(**v)

                elif k == 'extract_excel_data':
                    fd.extract_excel_data(**v)

        return fd

    def parse_technology_section(self):

        assert 'technology' in self.recipe.keys(), "No technology section to parse"

        possible_functions = [
            'add_technology_to_database',
            'add_default_CCS_processes',
        ]

        for f in self.recipe['technology']:
            for k, v in f.items():

                assert k in possible_functions, "{} is not a valid technology function".format(k)

                if k == 'add_technology_to_database':

                    possible_subfunctions = [
                        'create_regional_activities'
                    ]
                    actual_functions = []
                    for func in v['tasks']:
                        if func['function'] in possible_subfunctions:
                            if func['function'] == 'create_regional_activities':
                                this_item = {'function': create_regional_activities,
                                             'args': func.get('args', []),
                                             'kwargs': func.get('kwargs', {})}

                                actual_functions.append(this_item)

                        elif func['function'] in dir(technology):
                            args = [self.database]
                            args.extend(func.get('args', []))
                            this_item = {'function': getattr(technology, func['function']),
                                         'args': args,
                                         'kwargs': func.get('kwargs', {})}
                            actual_functions.append(this_item)

                    if "__ASSET_PATH__/" in v['technology_file']:
                        technology_file = v['technology_file'].replace("__ASSET_PATH__/", "")
                        technology_path = os.path.join(ASSET_PATH, technology_file)
                    else:
                        technology_path = v['technology_file']

                    self.database.extract_excel_data(technology_path)

                    for item in actual_functions:
                        _ = item['function'](*item['args'], **item['kwargs'])

                elif k == 'add_default_CCS_processes':
                    technology.add_default_CCS_processes(self.database)

    def parse_regionalisation_section(self):

        assert 'regionalisation' in self.recipe.keys(), "No regionalisation section to parse"

        function_dict = {
            'regionalise_multiple_processes': technology.regionalise_multiple_processes,
            'create_regional_activities': create_regional_activities,
            'create_regional_activities_from_filter': create_regional_activities_from_filter
        }

        for f in self.recipe['regionalisation']:

            assert f['function'] in function_dict.keys()

            function = function_dict[f['function']]

            args = f.get('args', [])
            kwargs = f.get('kwargs', {})

            if f['function'] in ['create_regional_activities', 'create_regional_activities_from_filter']:
                kwargs['db'] = self.database.db
            elif f['function'] == 'regionalise_multiple_processes':
                kwargs['database'] = self.database

            function(*args, **kwargs)

    def parse_market_section(self):

        assert 'markets' in self.recipe.keys(), "No markets section to parse"

        possible_functions = [
            'alter_market',
        ]

        for f in self.recipe['markets']:
            for k, v in f.items():

                assert k in possible_functions, "{} is not a valid market function".format(k)

                if k == 'alter_market':
                    market_filter = create_filter_from_description(v['market_filter'])
                    market = w.get_one(self.database.db, *market_filter)
                    fm = FuturaMarket(market, self.database)

                    for task in v['tasks']:

                        message = "Applying {}".format(task['function'])

                        if task['args']:
                            message += " with arguments {}".format(", ".join([str(x) for x in task['args']]))

                        if 'kwargs' in task.keys():
                            kwargs = task['kwargs']
                            message += " and keyword arguments {}".format(
                                ", ".join(["{}:{}".format(k, v) for k, v in kwargs.items()])
                            )
                        else:
                            kwargs = {}

                        print(message)
                        func = getattr(fm, task['function'])
                        func(*task['args'], **kwargs)

    def run(self):

        self.database = self.parse_load_section()

        if 'technology' in self.recipe.keys():
            self.parse_technology_section()

        if 'regionalisation' in self.recipe.keys():
            self.parse_regionalisation_section()

        if 'markets' in self.recipe.keys():
            self.parse_market_section()

    def write_database(self, project=None, database=None, overwrite=True):
        assert isinstance(self.database, FuturaDatabase)
        assert 'metadata' in self.recipe.keys()
        if not project:
            assert 'base_project' in self.recipe['metadata'].keys()
            project = self.recipe['metadata']['base_project']
        if not database:
            assert 'output_database' in self.recipe['metadata'].keys()
            database = self.recipe['metadata']['output_database']

        self.database.write_database(project, database, overwrite)
