import config
import json
import os
from tqdm import tqdm
import requests
from urllib.request import urlopen
from config import sets_to_reference, ROOT_DIR, languages_to_reference
from zipfile import ZipFile

def download_JSON(sets_to_reference):
    """Downloads JSON files from MTGAJSON to update data"""
    print("- Downloading data from MTGAJSON -")
    for setname in tqdm(sets_to_reference) :
        r = requests.get('https://mtgjson.com/api/v5/'+ setname +'.json.zip')
        zipfile = ROOT_DIR + 'data/sets/' +setname +".zip"
        with open(zipfile, "wb") as data:
            data.write(r.content)
        with ZipFile(zipfile, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
            zipObj.extractall(path=ROOT_DIR + 'data/sets/')
        ## If file exists, delete it ##
        if os.path.isfile(zipfile):
            os.remove(zipfile)
        else:    ## Show an error ##
            print("Error: %s file not found" % zipfile)

def build_reference(sets_to_reference):
    """Builds a card database from the sets list input.
    Returns : card_reference, name_to_uuid, number_to_uuid, uuid_to_number. """

    number_to_uuid = {}
    card_reference = {}
    name_to_uuid = {}
    uuid_to_number = {}

    print("- Building internal Card Reference -")
    for setName in tqdm(sets_to_reference) :
        # Fix 1 on WIN systems since CON.json is reserved :
        if setName == 'CON':
            setName = 'CON_'
        # End Fix 1
        with open(ROOT_DIR + 'data/sets/' + setName + '.json') as f:
            # Fix 2 on WIN systems since CON.json is reserved :
            if setName == 'CON_':
                setName = 'CON'
            # End Fix 2
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
            # Token version of the set : setname is preceded by 'T'    
            name_to_uuid['T'+setName]= {} 
            number_to_uuid['T'+setName]= {}
            card_reference['T'+setName]= {}
            uuid_to_number['T'+setName]= {}   
            for item in data['data']['tokens']:
                number_to_uuid['T'+setName][item['number']] = item['uuid']
                name_to_uuid['T'+setName][item['name']] = item['uuid']
                uuid_to_number['T'+setName][item['uuid']] = item['number']
                card_reference['T'+setName][item['uuid']] = {'name' : item['name'],
                                                        'colorIdentity' : item['colorIdentity'],
                                                        'convertedManaCost' : 0,
                                                        'number' : item['number'],
                                                        'setCode' : item['setCode'],
                                                        'subtypes' : item['subtypes'],
                                                        'supertypes' : item['supertypes'],
                                                        'types' : item['types'],
                                                        'uuid' : item['uuid'] }
    return (card_reference, name_to_uuid, number_to_uuid, uuid_to_number)        
### End of reference initialisation ####
