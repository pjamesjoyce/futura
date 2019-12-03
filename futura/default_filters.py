#import wurst as w
from . import w
from .utils import create_filter_from_description

coal_location_filter_description = []
coal_location_filter_description += [{'filter': 'exclude', 'args': [
    {'filter': 'equals', 'args': ['database', 'Carma CCS']}
]}]
coal_location_filter_description += [{'filter': 'equals', 'args': ['unit', 'kilowatt hour']}]
coal_location_filter_description += [{'filter': 'contains', 'args': ['name', 'hard coal']}]
coal_location_filter_description += [{'filter': 'doesnt_contain_any', 'args': ['name', ['coal mine', 'co-generation']]}]

coal_location_filter = create_filter_from_description(coal_location_filter_description)

hard_coal_ccs_filter_description = []
hard_coal_ccs_filter_description += [{'filter': 'equals', 'args': ['database', 'Carma CCS']}]
hard_coal_ccs_filter_description += [{'filter': 'either', 'args': [
    {'filter': 'contains', 'args': ['name', 'Hard coal']},
    {'filter': 'contains', 'args': ['name', 'hard coal']}]
    }]
hard_coal_ccs_filter_description += [{'filter': 'equals', 'args': ['location', 'GLO']}]

hard_coal_ccs_filter = create_filter_from_description(hard_coal_ccs_filter_description)

lignite_location_filter_description = []
lignite_location_filter_description += [{'filter': 'exclude', 'args': [
    {'filter': 'equals', 'args': ['database', 'Carma CCS']}
]}]
lignite_location_filter_description += [{'filter': 'equals', 'args': ['unit', 'kilowatt hour']}]
lignite_location_filter_description += [{'filter': 'contains', 'args': ['name', 'lignite']}]
lignite_location_filter_description += [{'filter': 'doesnt_contain_any', 'args': ['name', ['co-generation']]}]

lignite_location_filter = create_filter_from_description(lignite_location_filter_description)

lignite_ccs_filter_description = []
lignite_ccs_filter_description += [{'filter': 'equals', 'args': ['database', 'Carma CCS']}]
lignite_ccs_filter_description += [{'filter': 'either', 'args':[
    {'filter': 'contains', 'args': ['name', 'Lignite']},
    {'filter': 'contains', 'args': ['name', 'lignite']}]
    }]
lignite_ccs_filter_description += [{'filter': 'equals', 'args': ['location', 'GLO']}]

lignite_ccs_filter = create_filter_from_description(lignite_ccs_filter_description)

natural_gas_location_filter_description = []
natural_gas_location_filter_description += [{'filter': 'exclude', 'args': [
    {'filter': 'equals', 'args': ['database', 'Carma CCS']}
]}]
natural_gas_location_filter_description += [{'filter': 'equals', 'args': ['unit', 'kilowatt hour']}]
natural_gas_location_filter_description += [{'filter': 'contains', 'args': ['name', 'natural gas']}]
natural_gas_location_filter_description += [{'filter': 'doesnt_contain_any', 'args': ['name', ['co-generation', 'import', 'aluminium industry', 'burned', '10MW']]}]

natural_gas_location_filter = create_filter_from_description(natural_gas_location_filter_description)

natural_gas_ccs_filter_description = []
natural_gas_ccs_filter_description += [{'filter': 'equals', 'args': ['database', 'Carma CCS']}]
natural_gas_ccs_filter_description += [{'filter': 'either', 'args': [
    {'filter': 'contains', 'args': ['name', 'natural gas']},
    {'filter': 'contains', 'args': ['name', 'Natural gas']},
    {'filter': 'contains', 'args': ['name', 'ATR-H2']}
    ]}]
natural_gas_ccs_filter_description += [{'filter': 'equals', 'args': ['location', 'GLO']}]

natural_gas_ccs_filter = create_filter_from_description(natural_gas_ccs_filter_description)

wood_location_filter_description = []
wood_location_filter_description += [{'filter': 'exclude', 'args': [
    {'filter': 'equals', 'args': ['database', 'Carma CCS']}
]}]
wood_location_filter_description += [{'filter': 'equals', 'args': ['unit', 'kilowatt hour']}]
wood_location_filter_description += [{'filter': 'contains', 'args': ['name', 'wood']}]
wood_location_filter_description += [{'filter': 'doesnt_contain_any', 'args': ['name', ['treatment', 'ethanol', 'pellets', 'label-certified', '2000 kW']]}]
wood_location_filter_description += [{'filter': 'contains', 'args': ['name', 'state-of-the-art']}]

wood_location_filter = create_filter_from_description(wood_location_filter_description)

wood_ccs_filter_description = []
wood_ccs_filter_description += [{'filter': 'equals', 'args': ['database', 'Carma CCS']}]
wood_ccs_filter_description += [{'filter': 'either', 'args': [
    {'filter': 'contains', 'args': ['name', 'wood']},
    {'filter': 'contains', 'args': ['name', 'Wood']}
    ]}]
wood_ccs_filter_description += [{'filter': 'equals', 'args': ['location', 'GLO']}]

wood_ccs_filter = create_filter_from_description(wood_ccs_filter_description)
