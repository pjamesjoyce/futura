import yaml
import jinja2

from futura.storage import storage
from .wrappers import FuturaDatabase

from .recipe import FuturaRecipeExecutor

import os.path

try:
    import _pickle as pickle
except ImportError:
    print('falling back on pickle')
    import pickle

import zlib


class FuturaSaver:
    """
    TODO: Write doctring
    """

    def __init__(self, loader):

        self.recipe = loader.recipe
        self.database = loader.database


class FuturaLoader:

    """
    The FuturaLoader class sits at the centre of Futura and (via the FuturaDatabase, FuturaSaver and FuturaExecutor
    classes) allows you to load, run and save recipes for creating new databases. It also stores the current database
    and can be saved to disk itself and reloaded for quickly picking up where you left off.

    :param recipe_filepath: Optionally pass a filepath to open an existing recipe. If left blank a blank recipe is
        created
    :type recipe_filepath: str, optional
    :param autocreate: Automatically run the recipe when it is loaded. Default is `True`
    :type autocreate: bool, optional

    :ivar recipe: Dictionary representation of the current recipe. Can be set by :func:`load_recipe`
    :vartype recipe: dict

    :ivar database: A :class:`~futura.wrappers.FuturaDatabase` representing the current working database
    :vartype database: :class:`~futura.wrappers.FuturaDatabase`

    :ivar executor: A :class:`~futura.wrappers.FuturaRecipeExecutor` object which is invoked to run the current recipe
    :vartype executor: :class:`~futura.recipe.FuturaRecipeExecutor`

    :ivar recipe_filepath: Path of the loaded recipe. Set if/when a recipe is loaded
    :vartype recipe_filepath: str

    :ivar load_path: Path of the loaded .fl file. Set if/when an .fl file is loaded
    :vartype load_path: str
    """

    def __init__(self, recipe_filepath=None, autocreate=True):

        self.recipe = {}
        self.database = FuturaDatabase()

        self.executor = None

        self.recipe_filepath = recipe_filepath
        self.load_path = None

        if self.recipe_filepath:
            self.recipe = self.load_recipe(self.recipe_filepath)
        else:
            autocreate = None

        if autocreate:
            self.run()

    def load_recipe(self, filename):

        """
        Docstring: This is load_recipe - I need to write a docstring

        :return: Parsed recipe as a dict
        :rtype: dict
        """

        self.recipe_filepath = filename

        with open(filename, "r") as f:
            template = jinja2.Template(f.read())

        t_data = template.render()
        data = yaml.load(t_data, yaml.Loader)

        return data

    def run(self):

        executor = FuturaRecipeExecutor(self)
        executor.execute_recipe()
        # executor = None

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

    def save(self, save_path=None):

        if save_path is None:
            save_directory = storage.data_dir
            print("Saving to default directory({})".format(save_directory))
            save_filename = "{}.fl".format("-".join(self.database.database_names))
            print("Saving as default filename({})".format(save_filename))
            save_path = os.path.join(save_directory, save_filename)

        with open(save_path, 'wb') as f:
            f.write(zlib.compress(pickle.dumps(FuturaSaver(self))))

        print('Saved to {}'.format(save_path))

    def load(self, load_path):

        self.load_path = load_path

        with open(load_path, 'rb') as f:
            assert load_path[-3:] == '.fl', "Not a valid file path"
            print("Loading fl file from {}".format(load_path))
            loaded = pickle.loads(zlib.decompress(f.read()))

        self.database = loaded.database
        self.recipe = loaded.recipe
        print("Loaded {} with a total of {} activities".format(", ".join(self.database.database_names),
                                                               len(self.database.db)))
