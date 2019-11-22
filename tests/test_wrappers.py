from .brightway_fixtures import test_bw2_database
from futura.wrappers import FuturaDatabase


def test_futuradatabase():
    fdb = FuturaDatabase()
    assert isinstance(fdb, FuturaDatabase)


def test_simple_import(test_bw2_database):
    expected = [
        {
            'classifications': [42],
            'code': '1',
            'comment': 'Yep',
            'database': 'food',
            'exchanges': [{'name': 'dinner',
                           'amount': 0.5,
                           'loc': 0.5,
                           'location': 'CH',
                           'product': None,
                           'production volume': 13,
                           'type': 'technosphere',
                           'uncertainty type': 0,
                           'unit': 'kg'},
                          {'name': 'an emission',
                           'amount': 0.05,
                           'categories': ['things'],
                           'input': ('biosphere', '1'),
                           'location': None,
                           'product': 'find me!',
                           'production volume': None,
                           'type': 'biosphere',
                           'uncertainty type': 4,
                           'unit': 'kg'}],
            'location': 'CA',
            'name': 'lunch',
            'reference product': 'stuff',
            'unit': 'kg',
            'parameters': {'losses_gross_net': 0.01},
            'parameters full': [{
                'amount': 0.01,
                'name': 'losses_gross_net'
            }],
        }, {
            'classifications': [],
            'code': '2',
            'comment': '',
            'database': 'food',
            'exchanges': [{'name': 'lunch',
                           'amount': 0.25,
                           'location': 'CA',
                           'product': 'stuff',
                           'production volume': None,
                           'type': 'technosphere',
                           'uncertainty type': 0,
                           'unit': 'kg'},
                          {'name': 'another emission',
                           'amount': 0.15,
                           'categories': ['things'],
                           'input': ('biosphere', '2'),
                           'location': None,
                           'product': None,
                           'production volume': None,
                           'type': 'biosphere',
                           'uncertainty type': 0,
                           'unit': 'kg'}],
            'location': 'CH',
            'name': 'dinner',
            'reference product': None,
            'unit': 'kg',
            'parameters': {'rara': 13},
            'parameters full': [{
                'name': 'rara',
                'amount': 13,
                'something': 'else',
            }]
        }
    ]

    fdb = FuturaDatabase()
    fdb.extract_bw2_database('default', 'food')

    assert sorted(fdb.db, key=lambda x: x['code']) == sorted(expected, key=lambda x: x['code'])

# def test_full_ecoinvent_import():
#     """
#     TODO: Find a better way to do this
#     :return:
#     """
#     fdb = FuturaDatabase()
#     fdb.extract_bw2_database('Prospective_LCA_1', 'ecoinvent')
#     assert len(fdb.db) == 13831
