import json
from config import sets_to_reference, ROOT_DIR, languages_to_reference
from openpyxl import Workbook
from pm_collections import collections, look_for_card_in_collections
from pm_card import card
import inspect

#### Card Pool initialisation ####
number_to_uuid = {}
card_reference = {}
name_to_uuid = {}
uuid_to_number = {}

for setName in sets_to_reference :
  with open(ROOT_DIR + 'data/sets/' + setName + '.json') as f:
    data = json.load(f)
    name_to_uuid[setName]= {}
    number_to_uuid[setName]= {}
    card_reference[setName]= {}
    uuid_to_number[setName]= {}

    for item in data['data']['cards']:
        #print(item)
        number_to_uuid[setName][item['number']] = item['uuid']
        name_to_uuid[setName][item['name']] = item['uuid']
        uuid_to_number[setName][item['uuid']] = item['number']
        foreignName = {}
        for languageData in item['foreignData']:
            if languageData['language'] == 'Spanish' and 'ES' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
                language = 'ES'
                foreignName[language] = languageData['name']
            elif languageData['language'] == 'French' and 'FR' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
                language = 'FR'
                foreignName[language] = languageData['name']
            elif languageData['language'] == 'German' and 'DE' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
                language = 'DE'
                foreignName[language] = languageData['name']
            elif languageData['language'] == 'Italian' and 'IT' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
                language = 'IT'
                foreignName[language] = languageData['name']
            elif languageData['language'] == 'Portuguese' and 'PT' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
                language = 'PT'
                foreignName[language] = languageData['name']
            elif languageData['language'] == 'Japanese' and 'JP' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
                language = 'JP'
                foreignName[language] = languageData['name']
            elif languageData['language'] == 'Korean' and 'KO' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
                language = 'KO'
                foreignName[language] = languageData['name']
            elif languageData['language'] == 'Russian' and 'RU' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
                language = 'RU'
                foreignName[language] = languageData['name']
            elif languageData['language'] == 'Chinese' and 'ZH' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
                language = 'ZH'
                foreignName[language] = languageData['name']
        card_reference[setName][item['uuid']] = {'name' : item['name'],
                                                'colorIdentity' : item['colorIdentity'],
                                                'convertedManaCost' : item['convertedManaCost'],
                                                'legalities' : item['legalities'],
                                                'foreignName' : foreignName,
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
#### End of reference initialisation ####

# Tests begin here                                      

decks_to_add = ['MysticIntellect_C19.json']

#test_collec = collections('test')
#parsed_cards = test_collec.from_parsed_source('additions', card_reference)
#parsed_cards = test_collec.from_parsed_source('deck_comm_legends', card_reference)
#test_collec.save('test.json')

Teshar_deck = collections('Teshar')
parsed_cards = Teshar_deck.from_parsed_source('Teshar', card_reference)
# Test Output to excel
workbook = Workbook()
sheet = workbook.active
for i,card in enumerate(parsed_cards):
    sheet.cell(row=i+1, column=1).value = card[0]
    sheet.cell(row=i+1, column=2).value = card[1]
workbook.save(filename="Teshar.xlsx")

#test_collec.list_cards(card_reference)

# test card movements with token creation :
# test_collec.save('test.json')
# card_to_move = define_card_from_set_and_number('TMP', '290', 'NM', 'EN', [])
# test_collec2 = collections('test2')
# test_collec.move_card_from_self_to_destination_replace_with_proxy(card_to_move, 'TMP', test_collec2) # Hack to be removed after
# test_collec.save('test.json')
# test_collec2.save('test2.json')

Teshar_deck.save('Teshar.json')
#Teshar_deck.list_cards_edhrec_format(card_reference)

print(" ------------------------------------------")
print(" Test of research of cards in collections :")
objects = dir()
collections = [ eval(x) for x in objects if isinstance(eval(x), collections)] #inspect.isclass(x) == inspect.isclass(Teshar_deck) ]
res = look_for_card_in_collections("Teshar, Ancestor's Apostle", collections)
if len(res) > 0 :
    print ('.Found results:')
    for element in res :
        print (" - deck'{name}' : card from {setname}, condition {condition}, in {language}".format(name = element[0],
                                                                                                setname = element[1][0],
                                                                                                condition = element[1][2],
                                                                                                language = element[1][3]))
