# -*- coding: utf-8 -*-

from PySide2 import QtWidgets
import os

from .signals import signals

from .wrappers import FuturaGuiLoader

from .utils import findMainWindow
from .ui.dialogs import BaseDatabaseDialog, NewRecipeDialog, EcoinventLoginDialog, BrightwayDialog
from .ui.widgets.filter import parse_filter_widget, FilterListerDialog
from .ui.wizards import RegionalisationWizard, MarketsWizard

from futura.utils import create_filter_from_description
from futura import w
from futura.constants import ASSET_PATH
from futura.technology import add_technology_to_database, fix_ch_only_processes
from futura.recipe import FuturaRecipeExecutor
from futura.proxy import WurstProcess
from futura.storage import storage
import yaml

from copy import deepcopy
import shutil

from .threads import GeneratorThread

from bw2data import projects

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
        self.thread = None

    def connect_signals(self):
        # Note - these need to be set up in the signals file too

        # Recipes

        signals.new_recipe.connect(self.new_recipe)
        signals.load_recipe.connect(self.load_recipe)
        signals.test_filter.connect(self.test_filter)
        signals.regionalisation_wizard.connect(self.regionalisation_wizard)
        signals.export_recipe.connect(self.export_recipe)
        signals.add_technology_file.connect(self.add_technology_file)
        signals.markets_wizard.connect(self.markets_wizard)
        signals.add_base_database.connect(self.add_base_database_dialog)
        signals.export_to_brightway.connect(self.export_to_brightway)

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

            conversion_dict = {
                'Allocation at the point of substitution (APOS)': 'apos',
                'Consequential': 'consequential'
            }

            if ecoinvent_version == '3.6':
                conversion_dict['Cut-off'] = 'cut-off'
            else:
                conversion_dict['Cut-off'] = 'cutoff'

            ecoinvent_system_model = conversion_dict[new_recipe_dialog.ecoinvent_system_model.currentText()]

            findMainWindow().loader.recipe = {
                'metadata': {
                    'output_database': name,
                    'ecoinvent_version': ecoinvent_version,
                    'ecoinvent_system_model': ecoinvent_system_model,
                    'description': description
                },
                'actions': []
            }

            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Load ecoinvent?")
            message.setText(
                "Would you like to add the ecoinvent {} {} database to the recipe now?".format(
                    ecoinvent_version,
                    ecoinvent_system_model
                )
            )
            message.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            message.setDefaultButton(QtWidgets.QMessageBox.No)

            if message.exec_() == QtWidgets.QMessageBox.Yes:
                print("loading ecoinvent {} {}".format(ecoinvent_version, ecoinvent_system_model))

                check, username, password = self.check_ecoinvent_details()

                if check:
                    self.add_base_database(ecoinvent_version, ecoinvent_system_model,
                                           username=username, password=password)

                else:
                    QtWidgets.QMessageBox('Check your ecoinvent login details')

            else:

                signals.update_recipe.emit()
                signals.show_recipe_actions.emit()
                signals.reset_status_message.emit()

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
            print(findMainWindow().loader)
            print(findMainWindow().loader.database)
            #signals.update_recipe.emit()
            #signals.show_recipe_actions.emit()

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

            this_item_set = [WurstProcess(x) for x in w.get_many(db, *this_filter)]

            #this_item = w.get_one(db, *this_filter)
            #print(this_item)

            location_code_list = [x['code'] for x in rw.location_widget.checked_items]

            if len(this_item_set) == 1:

                recipe_entry = {
                    'action': 'regionalisation',
                    'tasks': [
                        {
                            'function': 'create_regional_activities_from_filter',
                            'kwargs': {
                                'new_regions': location_code_list,
                                'base_activity_filter': filter_description,
                            }
                        }
                    ]
                }

            else:

                recipe_entry = {
                    'action': 'regionalisation',
                    'tasks': [
                        {
                            'function': 'regionalise_multiple_processes',
                            'kwargs': {
                                'locations': location_code_list,
                                'base_activity_filter': filter_description,
                            }
                        }
                    ]
                }

            loader = findMainWindow().loader
            executor = FuturaRecipeExecutor(findMainWindow().loader)
            executor.execute_recipe_action(recipe_entry)
            loader.recipe['actions'].append(recipe_entry)

            signals.update_recipe.emit()

            # create_regional_activities(this_item, location_code_list, db)

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
            signals.reset_status_message.emit()

        else:
            print('Wizard Cancelled')

    def export_recipe(self):

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(None,
                                                            'Choose a recipe file...',
                                                            # os.path.join(os.path.expanduser('~'), 'Documents'),
                                                            r'C:\Users\pjjoyce\Dropbox\00_My_Software',
                                                            "Recipe Files (*.yml *.yaml)")
        if filename:

            signals.start_status_progress.emit(0)
            signals.change_status_message.emit('Exporting recipe...')

            QtWidgets.QApplication.processEvents()

            loader = findMainWindow().loader
            recipe = loader.recipe

            cp = deepcopy(recipe)

            move_files = []

            for action in cp['actions']:
                for task in action['tasks']:
                    k = task.get('kwargs')
                    if k:
                        if 'database' in k.keys():
                            del k['database']
                        if 'db' in k.keys():
                            del k['db']

                    if task['function'] == 'add_technology_to_database':
                        technology_path = task.get('kwargs').get('technology_file')
                        if technology_path:
                            split_path, split_name = os.path.split(technology_path)
                            if split_path == '':
                                if loader.recipe_filepath:
                                    print('assuming recipe_path')
                                    split_path, _ = os.path.split(loader.recipe_filepath)
                                elif loader.load_path:
                                    print('assuming loader_path')
                                    split_path, _ = os.path.split(loader.load_path)
                                else:
                                    print('no path to move the file')
                            move_files.append((split_path, split_name))
                            task['kwargs']['technology_file'] = split_name

            message_text = ""
            with open(filename, 'w') as f:
                yaml.safe_dump(cp, f)

            if move_files:
                base_folder, _ = os.path.split(filename)
                for f in move_files:
                    try:
                        shutil.copy(os.path.join(f[0], f[1]), os.path.join(base_folder, f[1]))
                        message_text += "{} moved to export folder\n".format(f[1])
                    except FileNotFoundError:
                        pass
            signals.hide_status_progress.emit()
            signals.reset_status_message.emit()
            message = QtWidgets.QMessageBox()
            message.setText("Export complete!" + "\n{}".format(message_text))
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

            recipe_entry = {
                'action': 'add_technology',
                'tasks': [
                    {
                        'function': 'add_technology_to_database',
                        'kwargs': {
                            'technology_file': filename
                        }
                    },
                    {
                        'function': 'fix_ch_only_processes',
                    }
                ]
            }

            if not findMainWindow().loader.recipe.get('actions'):
                findMainWindow().loader.recipe['actions'] = []

            findMainWindow().loader.recipe['actions'].append(recipe_entry)
            print(findMainWindow().loader.recipe)
            signals.update_recipe.emit()
            signals.reset_status_message.emit()

    def markets_wizard(self):

        print('Starting the wizard')
        mw = MarketsWizard()

        if mw.exec_():
            print(mw.final_recipe_section)
            loader = findMainWindow().loader
            executor = FuturaRecipeExecutor(findMainWindow().loader)
            executor.execute_recipe_action(mw.final_recipe_section)
            loader.recipe['actions'].append(mw.final_recipe_section)

            signals.update_recipe.emit()
            signals.reset_status_message.emit()

            print('Wizard Complete')

    def add_base_database_dialog(self):
        dialog = BaseDatabaseDialog()

        if dialog.exec_():
            version = dialog.ecoinvent_version.currentText()

            conversion_dict = {
                'Allocation at the point of substitution (APOS)': 'apos',
                'Consequential': 'consequential'
            }

            if version == '3.6':
                conversion_dict['Cut-off'] = 'cut-off'
            else:
                conversion_dict['Cut-off'] = 'cutoff'

            system_model = conversion_dict[dialog.ecoinvent_system_model.currentText()]

            check, username, password = self.check_ecoinvent_details()

            if check:

                self.add_base_database(version, system_model, username=username, password=password)

            else:
                QtWidgets.QMessageBox('Check your ecoinvent login details')

    def add_base_database(self, version, system_model, **kwargs):

            recipe_entry = {
                'action': 'load',
                'tasks': [
                    {
                        'function': 'get_ecoinvent',
                        'kwargs': {
                            'version': version,
                            'system_model': system_model
                        }
                    },
                ]
            }

            signals.start_status_progress.emit(0)
            signals.change_status_message.emit('Loading ecoinvent {} {}...'.format(version, system_model))

            loader = findMainWindow().loader
            executor = FuturaRecipeExecutor(findMainWindow().loader)

            def run():
                QtWidgets.QApplication.processEvents()
                yield 'starting'
                executor.execute_recipe_action(recipe_entry, **kwargs)
                yield 'finishing'
                loader.recipe['actions'].append(recipe_entry)
                signals.hide_status_progress.emit()
                signals.update_recipe.emit()
                signals.reset_status_message.emit()
                signals.show_recipe_actions.emit()

            self.thread = GeneratorThread(run, 2)
            QtWidgets.QApplication.processEvents()
            self.thread.start()

    def check_ecoinvent_details(self):

        config = storage.config
        username = None
        password = None
        ecoinvent = config.get('ecoinvent')

        if ecoinvent:
            username = ecoinvent.get('username')

        if ecoinvent:
            password = ecoinvent.get('password')

        if username and password:
            return True, username, password
        else:
            # dialog goes here
            dialog = EcoinventLoginDialog()

            if dialog.exec_():

                username = dialog.usernameLineEdit.text()
                password = dialog.passwordLineEdit.text()
                write_config = dialog.saveCheckBox.isChecked()

                # check if the login details work here

                if write_config:
                    config['ecoinvent']['username'] = username
                    config['ecoinvent']['password'] = password

                    storage.write_config(config)

                return True, username, password

            else:
                return False, None, None

    def export_to_brightway(self):
        loader = findMainWindow().loader

        recipe = loader.recipe

        base_project = recipe['metadata'].get('base_project')
        output_database = recipe['metadata'].get('output_database')

        brightway_dialog = BrightwayDialog()
        project_list = [p.name for p in sorted(projects)]

        brightway_dialog.existingComboBox.addItems(project_list)

        if base_project:
            if base_project in sorted(project_list):
                brightway_dialog.existingComboBox.setCurrentText(base_project)
                brightway_dialog.existingRadioButton.setChecked(True)
            else:
                brightway_dialog.newLineEdit.setText(base_project)
                brightway_dialog.newRadioButton.setChecked(True)

        if output_database:
            brightway_dialog.databaseLineEdit.setText(output_database)

        if brightway_dialog.exec_():
            if brightway_dialog.existingRadioButton.isChecked():
                project = brightway_dialog.existingComboBox.currentText()
            elif brightway_dialog.newRadioButton.isChecked():
                project = brightway_dialog.newLineEdit.text()
            else:
                print('something is wrong')
                return

            database = brightway_dialog.databaseLineEdit.text()

            signals.change_status_message.emit('Exporting to Brightway...')
            signals.start_status_progress.emit(0)

            def done():
                message = QtWidgets.QMessageBox()
                message.setText('Done!')
                message.exec_()

            #temp_message_signal = QtCore.Signal()
            signals.temp_message_signal.connect(done)

            def run():
                QtWidgets.QApplication.processEvents()
                yield 'starting'
                loader.database.write_database(project, database, True)
                yield 'done'

                signals.reset_status_message.emit()
                signals.hide_status_progress.emit()
                signals.hide_status_progress.emit()
                signals.temp_message_signal.emit()

            self.thread = GeneratorThread(run)
            self.thread.start()


