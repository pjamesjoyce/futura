import yaml
import jinja2

from futura.markets import FuturaMarket
from futura.utils import create_filter_from_description
from .wrappers import FuturaDatabase
from . import technology
from .constants import ASSET_PATH
#import wurst as w
from . import w

import os.path

class FuturaLoader:

    def __init__(self, recipe_filepath, autocreate=True):

        self.recipe = self.load_recipe(recipe_filepath)
        self.database = None

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

        wd = FuturaDatabase()

        for f in self.recipe['load']:
            for k, v in f.items():

                assert k in possible_functions, "{} is not a valid load function".format(k)

                if k == 'extract_bw2_database':
                    wd.extract_bw2_database(**v)

                elif k == 'extract_excel_data':
                    wd.extract_excel_data(**v)

        return wd

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
                    actual_functions = []
                    for func in v['funcs']:
                        actual_functions.append(getattr(technology, func))

                    if "__ASSET_PATH__/" in v['technology_file']:
                        technology_file = v['technology_file'].replace("__ASSET_PATH__/", "")
                        technology_path = os.path.join(ASSET_PATH, technology_file)
                    else:
                        technology_path = v['technology_file']

                    technology.add_technology_to_database(self.database, technology_path, actual_functions)

                elif k == 'add_default_CCS_processes':
                    technology.add_default_CCS_processes(self.database)

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
