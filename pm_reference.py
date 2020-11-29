import config
import json

#### Card Pool initialisation ####
number_to_uuid = {}
card_reference = {}
name_to_uuid = {}
uuid_to_number = {}
# This is here that range of sets to initialise should be set.
#sets_to_reference = ['STH', '4ED', 'ALL', 'MIR', 'REV', 'TMP', 'ICE', 'EXO', 'VIS', 'WTH', 'CMR', 'KLR', 'ZNR', 'AKR', '2XM', 'M21', 'IKO', 'THB', 'ELD', 'M20', 'MH1', 'WAR', 'RNA', 'UMA', 'GRN', 'M19', 'DOM', 'RIX', 'XLN']


for setName in sets_to_reference :
  with open(config.ROOT_DIR + 'data/sets/' + setName + '.json') as f:
    data = json.load(f)
    name_to_uuid[setName]= {}
    number_to_uuid[setName]= {}
    card_reference[setName]= {}
    uuid_to_number[setName]= {}
    for item in data['data']['cards']:
        number_to_uuid[setName][item['number']] = item['uuid']
        name_to_uuid[setName][item['name']] = item['uuid']
        uuid_to_number[setName][item['uuid']] = item['number']

        card_reference[setName][item['uuid']] = {'name' : item['name'],
                                                'colorIdentity' : item['colorIdentity'],
                                                'convertedManaCost' : item['convertedManaCost'],
                                                'legalities' : item['legalities'],
                                                'number' : item['number'],
                                                'rarity' : item['rarity'],
                                                'setCode' : item['setCode'],
                                                'subtypes' : item['subtypes'],
                                                'supertypes' : item['supertypes'],
                                                'types' : item['types'],
                                                'uuid' : item['uuid'] }
        try :
            card_reference[setName][item['uuid']]['keywords'] = item['keywords']
        except :
            pass
        try :
            card_reference[setName][item['uuid']]['power'] = item['power']
        except :
            pass
        try :
            card_reference[setName][item['uuid']]['toughness'] = item['toughness']
        except :
            pass           
        try :
            card_reference[setName][item['uuid']]['manaCost'] = item['manaCost']
        except :
            pass
