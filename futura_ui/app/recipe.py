try:
    from .wrappers import FuturaGuiLoader
except ImportError:
    from futura_ui.app.wrappers import FuturaGuiLoader

from futura.technology import *
from futura.regionalisation import *
from futura.markets import FuturaMarket


class FuturaRecipeExecutor:

    def __init__(self, loader=None):

        if not loader:
            print('no loader provided')
            self.loader = FuturaGuiLoader()
        else:
            self.loader = loader

        self.actions = {
            'load':
                {
                    'extract_bw2_database': self.loader.database.extract_bw2_database,
                    'extract_excel_data': self.loader.database.extract_excel_data
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
                    'add_alternative_exchanges': None,
                    'set_pv': None,
                    'transfer_pv': None,
                    'relink': None
                }
        }

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

    def set_market(self, market):
        assert isinstance(market, FuturaMarket)
        self.market = market

        self.actions['alter_market'] = {
            'add_alternative_exchanges': self.market.add_alternative_exchanges,
            'set_pv': self.market.set_pv,
            'transfer_pv': self.market.transfer_pv,
            'relink': self.market.relink
        }

    def execute_recipe_action(self, recipe_action):

        for task in recipe_action['tasks']:
            extra_kwargs = {}

            if task['function'] in self.database_functions:
                extra_kwargs['database'] = self.loader.database

            if task['function'] in self.db_functions:
                extra_kwargs['db'] = self.loader.database.db

            this_function = self.actions[recipe_action['action']][task['function']]
            this_args = task.get('args', [])
            this_kwargs = task.get('kwargs', {})
            this_kwargs.update(extra_kwargs)

            print("{}({}, {})".format(task['function'],
                                      ", ".join(this_args),
                                      ', '.join(["{}={}".format(k, v) for k, v in this_kwargs.items()])
                                      ))

            _ = this_function(*this_args, **this_kwargs)
