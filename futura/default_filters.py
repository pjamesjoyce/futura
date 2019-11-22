import wurst as w

coal_location_filter = []
coal_location_filter += [w.equals('database', 'ecoinvent')]
coal_location_filter += [w.equals('unit', 'kilowatt hour')]
coal_location_filter += [w.contains('name', 'hard coal')]
coal_location_filter += [w.doesnt_contain_any('name', ['coal mine', 'co-generation'])]

hard_coal_ccs_filter = []
hard_coal_ccs_filter += [w.equals('database', 'Carma CCS')]
hard_coal_ccs_filter += [w.either(*[w.contains('name', 'Hard coal'), w.contains('name', 'hard coal')])]
hard_coal_ccs_filter += [w.contains('location', 'GLO')]

lignite_location_filter = []
lignite_location_filter += [w.equals('database', 'ecoinvent')]
lignite_location_filter += [w.equals('unit', 'kilowatt hour')]
lignite_location_filter += [w.contains('name', 'lignite')]
lignite_location_filter += [w.doesnt_contain_any('name', ['co-generation'])]

lignite_ccs_filter = []
lignite_ccs_filter += [w.equals('database', 'Carma CCS')]
lignite_ccs_filter += [w.either(*[w.contains('name', 'Lignite'), w.contains('name', 'lignite')])]
lignite_ccs_filter += [w.contains('location', 'GLO')]

natural_gas_location_filter = []
natural_gas_location_filter += [w.equals('database', 'ecoinvent')]
natural_gas_location_filter += [w.equals('unit', 'kilowatt hour')]
natural_gas_location_filter += [w.contains('name', 'natural gas')]
natural_gas_location_filter += [w.doesnt_contain_any('name', ['co-generation', 'import', 'aluminium industry', 'burned', '10MW'])]

natural_gas_ccs_filter = []
natural_gas_ccs_filter += [w.equals('database', 'Carma CCS')]
natural_gas_ccs_filter += [w.either(*[w.contains('name', 'Natural gas'), w.contains('name', 'natural gas'), w.contains('name', 'ATR-H2')])]
natural_gas_ccs_filter += [w.doesnt_contain_any('name', ['Synthetic'])]
natural_gas_ccs_filter += [w.contains('location', 'GLO')]

wood_location_filter = []
wood_location_filter += [w.equals('database', 'ecoinvent')]
wood_location_filter += [w.equals('unit', 'kilowatt hour')]
wood_location_filter += [w.contains('name', 'wood')]
wood_location_filter += [w.doesnt_contain_any('name', ['treatment', 'ethanol', 'pellets', 'label-certified', '2000 kW'])]
wood_location_filter += [w.contains('name', 'state-of-the-art')]

wood_ccs_filter = []
wood_ccs_filter += [w.equals('database', 'Carma CCS')]
wood_ccs_filter += [w.either(*[w.contains('name', 'Wood'), w.contains('name', 'wood')])]
wood_ccs_filter += [w.contains('location', 'GLO')]
