# -*- coding: utf-8 -*-

from PySide2 import QtWidgets, QtCore
import os

from .settings import futura_settings  # , project_settings
from .signals import signals
from .ui.dialogs.progress import UndefinedProgress

from .wrappers import FuturaGuiLoader

from .utils import findMainWindow
from .ui.dialogs.new_recipe import NewRecipeDialog
from .ui.widgets.filter import FilterListerWidget, parse_filter_widget, FilterListerDialog
from .ui.wizards import RegionalisationWizard

from futura.utils import create_filter_from_description
from futura import w
from futura.regionalisation import create_regional_activities
from futura.constants import ASSET_PATH
from futura.technology import add_technology_to_database, fix_ch_only_processes

import yaml


class Controller(object):
    """The Controller is a central object in the Activity Browser. It groups methods that may be required in different
    parts of the AB to access, modify, or delete:
    - settings
    - projects
    - databases
    - calculation setups
    - activities/exchanges
    It is different from bwutils in that it also contains Qt elements such as dialogs.
    - """

    def __init__(self):
        self.connect_signals()  # connect the signals the app requires - this is what the app does
        self.load_settings()  # load settings
        self.db_wizard = None  # create an attribute for the db_wizard

    def connect_signals(self):
        # Note - these need to be set up in the signals file too

        # Recipes

        signals.new_recipe.connect(self.new_recipe)
        signals.load_recipe.connect(self.load_recipe)
        signals.test_filter.connect(self.test_filter)
        signals.regionalisation_wizard.connect(self.regionalisation_wizard)
        signals.export_recipe.connect(self.export_recipe)
        signals.add_technology_file.connect(self.add_technology_file)

    # SETTINGS
    def load_settings(self):
        if futura_settings.settings:
            print("Loading user settings:")
            # self.switch_brightway2_dir_path(dirpath=futura_settings.custom_bw_dir)
            # self.change_project(futura_settings.startup_project)

    # Specific functions to do things go here, within the controller class

    def new_recipe(self):

        new_recipe_dialog = NewRecipeDialog()

        if new_recipe_dialog.exec_():

            print('Creating a new, blank recipe')
            findMainWindow().loader = FuturaGuiLoader()

            name = new_recipe_dialog.name.text()
            ecoinvent_version = new_recipe_dialog.ecoinvent_version.currentText()
            ecoinvent_system_model = new_recipe_dialog.ecoinvent_system_model.currentText()
            description = new_recipe_dialog.description.toPlainText()

            findMainWindow().loader.recipe = {
                'metadata': {
                    'output_database': name,
                    'ecoinvent_version': ecoinvent_version,
                    'ecoinvent_system_model': ecoinvent_system_model,
                    'description': description
                },
            }

            signals.update_recipe.emit()
            signals.show_recipe_actions.emit()

        else:
            print('Cancelling')

    def load_recipe(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None,
                                                            'Choose a recipe file...',
                                                            # os.path.join(os.path.expanduser('~'), 'Documents'),
                                                            r'C:\Users\pjjoyce\Dropbox\00_My_Software',
                                                            "Recipe Files (*.yml *.yaml)")
        print(filename)
        if filename:
            # progress = UndefinedProgress()

            # signals.show_undefined_progress.emit()

            findMainWindow().loader = FuturaGuiLoader(filename, autocreate=True)
            signals.update_recipe.emit()
            signals.show_recipe_actions.emit()

            # signals.close_undefined_progress.emit()

    def test_filter(self):

        x = self.get_filter()

        print(x)

    def get_filter(self):

        filter_dialog = FilterListerDialog()

        if filter_dialog.exec_():
            return parse_filter_widget(filter_dialog.filter_widget)
        else:
            return

    def regionalisation_wizard(self):
        print('Starting the wizard')
        rw = RegionalisationWizard()

        if rw.exec_():
            print('Wizard Complete')
            filter_description = parse_filter_widget(rw.filter_widget)
            print(filter_description)
            this_filter = create_filter_from_description(filter_description)
            db = findMainWindow().loader.database.db
            this_item = w.get_one(db, *this_filter)
            print(this_item)

            location_code_list = [x['code'] for x in rw.location_widget.checked_items]

            create_regional_activities(this_item, location_code_list, db)

            recipe_entry = {
                'function': 'create_regional_activities_from_filter',
                'kwargs': {
                    'new_regions': location_code_list,
                    'base_activity_filter': filter_description,
                }
            }

            if not findMainWindow().loader.recipe.get('regionalisation'):
                findMainWindow().loader.recipe['regionalisation'] = []

            findMainWindow().loader.recipe['regionalisation'].append(recipe_entry)
            print(findMainWindow().loader.recipe)
            signals.update_recipe.emit()

            no_location_filter_description = [x for x in filter_description if x['args'][0] != 'location']
            new_locations_filter_description = [{'filter': 'equals', 'args': ['location', l]} for l in
                                                location_code_list]
            new_locations_filter_description = [{'filter': 'either', 'args': new_locations_filter_description}]
            new_locations_filter_description = no_location_filter_description + new_locations_filter_description
            new_locations_filter = create_filter_from_description(new_locations_filter_description)
            result = list(w.get_many(db, *new_locations_filter))

            print(["{} ({}) [{}]".format(x['name'], x['unit'], x['location']) for x in result])

            message = QtWidgets.QMessageBox()
            message.setText("{} new processes created".format(len(result)))
            message.setInformativeText(
                "\n".join(["{} ({}) [{}]".format(x['name'], x['unit'], x['location']) for x in result]))
            message.exec_()

        else:
            print('Wizard Cancelled')

    def export_recipe(self):
        recipe = findMainWindow().loader.recipe

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(None,
                                                            'Choose a recipe file...',
                                                            # os.path.join(os.path.expanduser('~'), 'Documents'),
                                                            r'C:\Users\pjjoyce\Dropbox\00_My_Software',
                                                            "Recipe Files (*.yml *.yaml)")
        if filename:
            with open(filename, 'w') as f:
                yaml.safe_dump(recipe, f)

            message = QtWidgets.QMessageBox()
            message.setText("Export complete!")
            message.exec_()

    def add_technology_file(self):

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None,
                                                            'Choose a recipe file...',
                                                            # os.path.join(os.path.expanduser('~'), 'Documents'),
                                                            ASSET_PATH,
                                                            "Excel Files (*.xls *.xlsx)")

        if filename:
            default_funcs = [fix_ch_only_processes]

            add_technology_to_database(findMainWindow().loader.database, filename, default_funcs)

            recipe_entry = {'add_technology_to_database':
                                {'technology_file': filename,
                                 'tasks': [
                                     {
                                         'function': 'fix_ch_only_processes',
                                         'args': []
                                     }
                                 ]
                                 }
                            }

            if not findMainWindow().loader.recipe.get('technology'):
                findMainWindow().loader.recipe['technology'] = []

            findMainWindow().loader.recipe['technology'].append(recipe_entry)
            print(findMainWindow().loader.recipe)
            signals.update_recipe.emit()
