from .technology import *
from .regionalisation import *
from .markets import FuturaMarket
from .ecoinvent import check_database
from .constants import ASSET_PATH, DEFAULT_SETUP_PROJECT

from . import w
import os


class FuturaRecipeExecutor:

    def __init__(self, loader):

        self.loader = loader

        self.database_functions = [
            'add_technology_to_database',
            'add_default_CCS_processes',
            'fix_ch_only_processes',
            'add_hard_coal_ccs',
            'add_lignite_ccs',
            'add_natural_gas_ccs',
            'add_wood_ccs',
            'regionalise_multiple_processes'

        ]

        self.db_functions = [
            'create_regional_activities_from_filter'
        ]

        self.market = None

    @property
    def actions(self):
        base_actions = {
            'load':
                {
                    'extract_bw2_database': None,  # self.loader.database.extract_bw2_database,
                    'extract_excel_data': None,  # self.loader.database.extract_excel_data
                    'get_ecoinvent': None
                },
            'add_technology':
                {
                    'add_technology_to_database': add_technology_to_database,
                    'add_default_CCS_processes': add_default_CCS_processes,
                    'fix_ch_only_processes': fix_ch_only_processes,
                    'add_hard_coal_ccs': add_hard_coal_ccs,
                    'add_lignite_ccs': add_lignite_ccs,
                    'add_natural_gas_ccs': add_natural_gas_ccs,
                    'add_wood_ccs': add_wood_ccs,
                },
            'regionalisation':
                {
                    'regionalise_multiple_processes': regionalise_multiple_processes,
                    'create_regional_activities_from_filter': create_regional_activities_from_filter
                },
            'alter_market':
                {
                    'set_market': self.set_market,
                    'add_alternative_exchanges': None,
                    'set_pv': None,
                    'transfer_pv': None,
                    'relink': None
                }
        }

        if self.market:
            base_actions['alter_market']['add_alternative_exchanges'] = self.market.add_alternative_exchanges
            base_actions['alter_market']['set_pv'] = self.market.set_pv
            base_actions['alter_market']['transfer_pv'] = self.market.transfer_pv
            base_actions['alter_market']['relink'] = self.market.relink

        if self.loader:
            base_actions['load']['extract_bw2_database'] = self.database.extract_bw2_database
            base_actions['load']['extract_excel_data'] = self.database.extract_excel_data
            base_actions['load']['get_ecoinvent'] = self.database.get_ecoinvent

        return base_actions

    @property
    def database(self):
        return self.loader.database

    @property
    def db(self):
        return self.database.db

    @property
    def recipe(self):
        return self.loader.recipe

    def execute_recipe(self):

        for message in self.recipe_generator():
            print(message['message'])

    def recipe_generator(self):

        for action in self.recipe['actions']:

            yield {'message': "{} started".format(action['action'])}

            self.execute_recipe_action(action)

            yield {'message': "{} finished".format(action['action'])}

    def set_market(self, market_filter):

        this_market_filter = create_filter_from_description(market_filter)
        this_market = w.get_one(self.database.db, *this_market_filter)
        market = FuturaMarket(this_market, self.database)

        assert isinstance(market, FuturaMarket)
        self.market = market

    def execute_recipe_action(self, recipe_action, **kwargs):

        for task in recipe_action['tasks']:
            if kwargs:
                extra_kwargs = kwargs
            else:
                extra_kwargs = {}

            if task['function'] in self.database_functions:
                extra_kwargs['database'] = self.loader.database

            if task['function'] in self.db_functions:
                extra_kwargs['db'] = self.loader.database.db

            if task['function'] == 'add_technology_to_database':
                technology_file = None

                k = task.get('kwargs')
                a = task.get('args')
                if k:
                    technology_file = k.get('technology_file')
                    if technology_file:
                        del k['technology_file']
                elif a:
                    if len(a) >= 2:
                        technology_file = a.pop(0)

                if "__ASSET_PATH__/" in technology_file:
                    technology_file = technology_file.replace("__ASSET_PATH__/", "")
                    technology_path = os.path.join(ASSET_PATH, technology_file)
                else:
                    technology_path = technology_file

                extra_kwargs['technology_file'] = technology_path

            if task['function'] == 'extract_bw2_database':
                project_name = None
                database_name = None

                k = task.get('kwargs')
                a = task.get('args')
                if k:
                    project_name = k.get('project_name')
                    database_name = k.get('database_name')
                elif a:
                    if len(a) >= 2:
                        project_name = a[0]
                        database_name = a[1]

                assert project_name and database_name, 'Project or database name missing'

                check = check_database(project_name, database_name)

                if not check:
                    print('Falling back on get_ecoinvent')
                    if self.ecoinvent_fallback() == 0:
                        break
                    else:
                        print('Recipe failed - could not load a base database')
                        return

            this_function = self.actions[recipe_action['action']][task['function']]
            this_args = task.get('args', [])
            this_kwargs = task.get('kwargs', {})
            this_kwargs.update(extra_kwargs)

            print("{}({}{})".format(task['function'],
                                    ", ".join(this_args),
                                    ', '.join(["{}={}".format(k, v) for k, v in this_kwargs.items()])
                                    ))

            _ = this_function(*this_args, **this_kwargs)

            print(self.loader)
            print(self.loader.database)

    def ecoinvent_fallback(self):

        print("The database defined in this recipe doesn't exist")
        ecoinvent_version = self.recipe['metadata'].get('ecoinvent_version')
        ecoinvent_system_model = self.recipe['metadata'].get('ecoinvent_system_model')

        if ecoinvent_version and ecoinvent_system_model:
            print("The recipe specifies an ecoinvent version "
                  "(ecoinvent {} {}), attempting to find this now".format(ecoinvent_version,
                                                                          ecoinvent_system_model))
            check_database_name = "ecoinvent_{}{}".format(ecoinvent_system_model,
                                                          str(ecoinvent_version).replace('.', ''))

            check = check_database(DEFAULT_SETUP_PROJECT, check_database_name)

            if check:
                self.database.extract_bw2_database(DEFAULT_SETUP_PROJECT, check_database_name)
            else:
                self.database.get_ecoinvent(db_name=check_database_name,
                                            store_download=True,
                                            version=ecoinvent_version,
                                            system_model=ecoinvent_system_model)
            return 0
        else:
            print('no version of ecoinvent has been specified...')
            return 1
