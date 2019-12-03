# from pathlib import Path
# from futura.sectors import *
# from futura.wrappers import FuturaDatabase
import os

ASSET_PATH = os.path.join(os.path.dirname(__file__), 'assets')
CCS_FILE = 'lci-Carma-CCS-base-GLO2.xlsx'
FULL_CCS_FILE = os.path.join(ASSET_PATH, CCS_FILE)

DEFAULT_CONFIG = {
    'ecoinvent': {
        'username': None,
        'password': None,
    }
}

# ELECTRICITY_TREE = [build_tree(bw_glo_elec, filters=electricity_markets)]
# CEMENT_TREE = [build_tree(bw_cement_europe, filters=cement_filter),
#                build_tree(bw_cement_US, filters=cement_filter),]
#
#
# TREE_DATA = {'Electricity': ELECTRICITY_TREE,
#              'Cement': CEMENT_TREE,
#              'Aluminium': {},
#              'Steel': {},
#              'Lithium': {},
#              'Glass': {}
#              }
