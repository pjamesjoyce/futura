import pytest
from bw2data.tests import bw2test
from bw2data import Database, projects
import os
from futura.loader import FuturaLoader

TEST_ASSET_PATH = os.path.join(os.path.dirname(__file__), 'assets')
TEST_FILENAME = 'test.fl'

#@pytest.fixture(scope='module')
@bw2test
def test_write_bw2_database(loader):

    db_len = len(loader.database.db)

    loader.write_database(project='TESTPROJECT', database='TESTDATABASE')

    assert len(Database('TESTDATABASE')) == db_len

    assert projects.current == 'TESTPROJECT'


def test_save(loader):

    filepath = os.path.join(TEST_ASSET_PATH, TEST_FILENAME)

    loader.save(filepath)

    assert os.path.isfile(filepath)


def test_load(loader):

    filepath = os.path.join(TEST_ASSET_PATH, TEST_FILENAME)

    new_loader = FuturaLoader()

    new_loader.load(filepath)

    assert len(new_loader.database.db) == len(loader.database.db)

