from PySide2.QtGui import QStandardItemModel, QStandardItem

from copy import copy
from futura.utils import create_filter_from_description
from futura import w
from ..utils import findMainWindow


class FuturaRecipePrettifier:
    def __init__(self, loader):
        self.masks = {
            'extract_bw2_database': 'Extract Brightway2 Database\n'
                                    'Project: {project_name}\n'
                                    'Database: {database_name}',
            'extract_BW2Package': 'Extract data from BW2Package file\n'
                                  'Filepath: {packagefilepath}',
            'extract_excel_data': 'Extract data from Excel file\n'
                                  'File: {excelfilepath}',
            'get_ecoinvent': 'Load base ecoinvent database\n'
                             'Version: {version}\n'
                             'System model: {system_model}',
            'add_technology_to_database': 'Add technology to database\n'
                                          'File: {technology_file}',
            'add_default_CCS_processes': 'Add all default CCS technologies to all producing regions',
            'fix_ch_only_processes': 'Fix processes with only Swiss versions',
            'add_hard_coal_ccs': 'Add hard coal CCS to all producing regions',
            'add_lignite_ccs': 'Add lignite CCS to all producing regions',
            'add_natural_gas_ccs': 'Add natural gas CCS to all producing regions',
            'add_wood_ccs': 'Add wood CCS to all producing regions',
            'regionalise_multiple_processes': 'Regionalise multiple processes\n'
                                              'Base processes:\n'
                                              '{base_activity_filter}\n'
                                              'Locations: {locations}',
            'create_regional_activities_from_filter': 'Create regional activities\n'
                                                      'Base process: {base_activity_filter}\n'
                                                      'Locations: {new_regions}',
            'set_market': 'Set market to alter\n'
                          'Market: {market_filter}',
            'add_alternative_exchanges': 'Add alternative exchanges to market',
            'set_pv': 'Set the production volume of {process_name} = {new_pv}',
            'transfer_pv': 'Transfer {amount:.0f}{unit} of the production volume of {from_name} to {to_name}',
            'relink': 'Relink market'
        }
        self.loader = loader

    def format(self, recipe_item):
        function = recipe_item['function']
        original_kwargs = recipe_item.get('kwargs', {})
        copy_kwargs = copy(original_kwargs)

        for k, v in copy_kwargs.items():
            if "_filter" in k:
                print(k)
                this_filter = create_filter_from_description(v)
                these_items = list(w.get_many(self.loader.database.db, *this_filter))
                string = '\n'.join(['{name} ({unit}) [{location}]'.format(**x) for x in these_items])
                copy_kwargs[k] = string
            elif isinstance(v, list):
                print("{} is a list".format(v))
                if k not in ['database', 'db']:
                    copy_kwargs[k] = ', '.join(v)

        if function == 'transfer_pv':
            if 'factor' in copy_kwargs.keys():
                copy_kwargs['amount'] = copy_kwargs['factor'] * 100
                copy_kwargs['unit'] = "%"
            else:
                copy_kwargs['unit'] = ""

        mask = self.masks[function]
        return mask.format(**copy_kwargs)


sections = {
    'load': 'Load',
    'add_technology': 'Technologies',
    'regionalisation': 'Regionalisation',
    'alter_market': 'Markets'
}


class RecipeModel(QStandardItemModel):
    def __init__(self):
        super(RecipeModel, self).__init__()
        self.setColumnCount(1)
        self.parentItem = self.invisibleRootItem()

    def parse_recipe(self, recipe):

        self.clear()
        self.setColumnCount(1)
        #self.setHorizontalHeaderLabels(['item','detail'])
        self.setHorizontalHeaderLabels(['Action'])
        self.parentItem = self.invisibleRootItem()

        parentItem = self.parentItem

        for m, v in recipe.get('metadata', {}).items():
            item = QStandardItem('{}: {}'.format(m, v))
            parentItem.appendRow(item)

        fp = FuturaRecipePrettifier(findMainWindow().loader)

        for action in recipe.get('actions', []):
            item = QStandardItem(sections[action['action']])
            parentItem.appendRow(item)
            for task in action['tasks']:
                this_task = QStandardItem(fp.format(task))
                item.appendRow(this_task)


        # def parse(this_dict, parent):
        #     for k, v in this_dict.items():
        #         if isinstance(v, dict):
        #             item = QStandardItem(str(k))
        #             parent.appendRow([item])
        #             parse(v, item)
        #
        #         elif isinstance(v, list):
        #             this_item = QStandardItem(str(k))
        #             parent.appendRow([this_item])
        #
        #             for x in v:
        #                 if isinstance(x, dict):
        #                     parse(x, this_item)
        #                 else:
        #                     item = QStandardItem(str(k))
        #                     item_detail = QStandardItem(str(v))
        #                     this_item.appendRow([item, item_detail])
        #         else:
        #             item = QStandardItem(str(k))
        #             item_detail = QStandardItem(str(v))
        #             parent.appendRow([item, item_detail])
        #
        # parse(recipe, parentItem)
