import json
from config import sets_to_reference, ROOT_DIR, languages_to_reference
import json
import os.path
import pm_card

number_to_uuid = {}
uuid_to_number = {} 
name_to_uuid = {}
name_to_number= {}
for setName in sets_to_reference :
  with open(ROOT_DIR + 'data/sets/' + setName + '.json') as f:
    data = json.load(f)
    number_to_uuid[setName]= {}
    name_to_uuid[setName]= {}
    uuid_to_number[setName]= {}
    name_to_number[setName]= {}
    for item in data['data']['cards']:
        number_to_uuid[setName][item['number']] = item['uuid']
        name_to_uuid[setName][item['name']] = item['uuid']
        uuid_to_number[setName][item['uuid']] = item['number']
        name_to_number[setName][item['name']] = item['number']
        for languageData in item['foreignData']:
            if languageData['language'] == 'Spanish' and 'ES' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
            elif languageData['language'] == 'French' and 'FR' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
            elif languageData['language'] == 'German' and 'DE' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
            elif languageData['language'] == 'Italian' and 'IT' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
            elif languageData['language'] == 'Portuguese' and 'PT' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
            elif languageData['language'] == 'Japanese' and 'JP' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
            elif languageData['language'] == 'Korean' and 'KO' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
            elif languageData['language'] == 'Russian' and 'RU' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']
            elif languageData['language'] == 'Chinese' and 'ZH' in languages_to_reference:
                name_to_uuid[setName][languageData['name']] = item['uuid']

def trigram_edition_code_test( string_in ):
    return (len(string_in) == 3 and string_in.upper().isupper() and string_in in sets_to_reference)

def is_number_test( string_in ):
    return (string_in.isdigit()) 

def is_number_of_cards_test( string_in):
    return(string_in[0] == '*')

def is_a_condition_of_card_test(string_in):
    return(string_in in ['MT', 'NM', 'EX', 'GD', 'LP', 'PL', 'PO'])

def is_a_variation_of_card_test(string_in):
    return(string_in in ['Alt', 'Ext', 'Foil', 'Proxy'])

def is_a_language_test(string_in):
    return(string_in in ['EN', 'ES', 'FR', 'DE', 'IT', 'PT', 'JP', 'KO', 'RU', 'ZH' ])

# def define_card_from_set_and_number(set_name, card_number, card_condition, card_language, card_modifications):
#     """
#     docstring
#     """
#     card_uuid = number_to_uuid[set_name][card_number]
#     return(pm_card.card(card_uuid, card_condition, card_language, card_modifications))

class collections :
    def __init__(self, name):
        self.name = name
        if not os.path.isfile(ROOT_DIR + 'data/collections/' + self.name + '.json') :
            self.File = open(ROOT_DIR + 'data/collections/' + self.name + '.json', 'x')
            self.File.close()
            self.content = {}
            for setCode in sets_to_reference:
                self.content[setCode] = []
        else:
            self.File = open(ROOT_DIR + 'data/collections/' + self.name + '.json', 'r')
            self.content = json.load(self.File)
            self.File.close()

    def read(self, name):
        """
        docstring
        """
        self.name = name
        self.File = open(ROOT_DIR + 'data/collections/' + self.name, 'r')
        self.content = json.load(self.File)
        self.File.close()
        return(self.content)

    def save(self, name):
        """
        docstring
        """
        self.File = open(ROOT_DIR + 'data/collections/' + self.name + '.json', 'w')
        self.File.write(json.dumps(self.content))
        self.File.close()
        return(True)

    def add_card_with(self, card, setCode = None):
        """
        docstring
        """
        card=card

        if setCode:
            try :
                if (self.content[setCode]) != []:
                    self.content[setCode].append([card.set, card.name, card.condition, card.language, card.modifications])
                else :
                    self.content[setCode] = [[card.set, card.name, card.condition, card.language, card.modifications]]
            except KeyError:
                self.content[setCode] = [[card.set, card.name, card.condition, card.language, card.modifications]]
        else:
            pass

    def remove_card_with_(self, card, setCode):
        """
        docstring
        """
        self.content[setCode].remove(card)
        pass

    def move_card_from_self_to_destination_replace_with_proxy(self, card, setCode, destination):
        """
        docstring
        """
        card_set = card.set
        card_name = card.name
        card_condition = card.condition
        card_language = card.language
        modifications = card.modifications

        proxy_card = pm_card.card(card_set, card_name, card_condition, card_language, ['Proxy',{'destination' : destination.name}])
        transferred_card = pm_card.card(card_set, card_name, card_condition, card_language, modifications)
        try :
            self.add_card_with(proxy_card, setCode)
        except :
            print("error1")
        try :
            destination.add_card_with(transferred_card, setCode)
        except :
            print('error2')
            self.remove_card_with_(proxy_card, setCode)
            self.add_card_with(transferred_card, setCode)

    def from_parsed_source(self, source_file, card_reference=None):
        """
        docstring
        """
        with open(ROOT_DIR + 'data/input/' + source_file + '.txt', 'r') as f:
            edition_code = False
            parsed_cards = []
            line_args = []
            default_card_condition = 'NM'
            default_card_language = 'FR'
            for line in f:
                line = line.rstrip()
                #print(line)
                card_condition = default_card_condition
                card_language = default_card_language
                card_variation = None
                number_of_cards = 1
                card = False
                if trigram_edition_code_test(line):
                    edition_code = line
                    print('>>' + edition_code)
                elif is_a_language_test(line):
                    card_language = line
                    default_card_language = line
                else :
                    line_args = line.split(' ')
                    # len_args = len(line_args)
                    if trigram_edition_code_test(line_args[0]):
                        edition_code = line_args[0]
                        line_args = line_args[1:]
                    if is_number_test(line_args[0]):
                        card_number = str(int(line_args[0]))
                        card = True
                        line_args = line_args[1:]
                    for i in range(len(line_args)):        
                        if is_a_variation_of_card_test(line_args[-i]):
                            card_variation = line_args[-i]
                            del line_args[-i]
                    for i in range(len(line_args)):        
                        if is_a_condition_of_card_test(line_args[-i]):
                            card_condition = line_args[-i]
                            del line_args[-i]
                    for i in range(len(line_args)):
                        if is_number_of_cards_test(line_args[-i]):
                            number_of_cards = int(line_args[-i][1:])
                            del line_args[-i]
                    for i in range(len(line_args)):
                        if is_a_language_test(line_args[-i]):
                            card_language = line_args[-i]
                            del line_args[-i] 
                if card : # Case where card was described with a number in a set
                    print('- set ' + edition_code +' =/= card #'+ card_number + ' / ' + card_language)
                    try :
                        card_uuid = number_to_uuid[edition_code][card_number]
                    except KeyError:
                        print ('Set Key Error - Maybe set {setName} data was not downloaded from https://mtgjson.com/api/v5/{setName}.json ?'.format(edition_code,edition_code))
                    metadata = []
                    if card_variation :
                        metadata.append(card_variation)
                    card_name = card_reference[edition_code][card_uuid]['name']
                    new_card = pm_card.card(edition_code, card_name, card_condition, card_language, metadata)
                    for i in range(number_of_cards):
                        self.add_card_with(new_card, edition_code)
                        print("  " + card_reference[edition_code][card_uuid]['name'] + ' : ' + 'https://scryfall.com/card/' + edition_code.lower() +'/' + str(card_reference[edition_code][card_uuid]['number']))
                        if card_language == 'EN':
                            print("  https://www.cardmarket.com/fr/Magic/Products/Search?searchString=" + card_reference[edition_code][card_uuid]['name'].replace(' ', '-') )
                        else :
                            try :
                                print("  https://www.cardmarket.com/fr/Magic/Products/Search?searchString=" + card_reference[edition_code][card_uuid]['foreignName'][card_language].replace(' ', '-') )
                            except :
                                print("  Card Name Replacement error for foreign langage " + card_language )
                        parsed_cards.append( ["" + card_reference[edition_code][card_uuid]['name'], "https://scryfall.com/card/" + edition_code.lower() +"/" + str(card_reference[edition_code][card_uuid]['number'])])
                elif not trigram_edition_code_test(line):   # Case where card, if there is one, was not described with a number in a set
                    card_name = ' '.join(line_args)
                    if len(card_name) > 0:
                        card = True
                    if card :
                        print('- set ' + edition_code +' / carte '+ card_name + ' / ' + card_language)
                        card_uuid = name_to_uuid[edition_code][card_name]
                        card_number = uuid_to_number[edition_code][card_uuid]
                        metadata = []
                        if card_variation :
                            metadata.append(card_variation)  
                        new_card = pm_card.card(edition_code, card_name, card_condition, card_language, metadata)
                        for i in range(number_of_cards):
                            self.add_card_with(new_card, edition_code)
                            print("  " + card_name + ' : ' + 'https://scryfall.com/card/' + edition_code.lower() +'/' + card_number )
                            if card_language == 'EN':
                                print("  https://www.cardmarket.com/fr/Magic/Products/Search?searchString=" + card_name.replace(' ', '-') )
                            else :
                                try :
                                    print("  https://www.cardmarket.com/fr/Magic/Products/Search?searchString=" + card_reference[edition_code][card_uuid]['foreignName'][card_language].replace(' ', '-') )     
                                except KeyError:
                                    print("  https://www.cardmarket.com/fr/Magic/Products/Search?searchString=" + card_name.replace(' ', '-') )     
                            metadata = [card_language, card_condition]
                            if card_variation :
                                metadata.append(card_variation)
                            parsed_cards.append( ["" + card_reference[edition_code][card_uuid]['name'], "https://scryfall.com/card/" + edition_code.lower() +"/" + card_name.lower().replace(' ', '-')] )    
        return(parsed_cards)

    
    def list_cards(self,card_reference):
        """
        docstring
        """
        print("- " + self.name + " :")
        sets = self.content.keys()
        for set_name in sets :
            for card in self.content[set_name]:
                card_uuid = card[0]
                card_condition = card[1]
                card_language  = card[2]
                card_modifiers = card[3]
                card_info_from_ref = card_reference[set_name][card_uuid]
                if card_language == 'EN' :
                    card_name = card_info_from_ref['name']
                else :
                    try :
                        card_name = card_info_from_ref['foreignName'][card_language]
                    except :
                        print(card_name)
                card_rarity = card_info_from_ref['rarity']
                card_colorIdentity = card_info_from_ref['colorIdentity']
                card_convertedManaCost = card_info_from_ref['convertedManaCost']
                card_number = card_info_from_ref['number']
                print(" {card_name} [{set_name} - {card_number}] : {card_rarity} {card_modifiers} - {card_condition} condition, {card_language} - {card_convertedManaCost} cmc - {card_colorIdentity} ".format(
                                                                                                                    card_name = card_name,
                                                                                                                    set_name = set_name,
                                                                                                                    card_number = card_number,
                                                                                                                    card_rarity = card_rarity,
                                                                                                                    card_modifiers = ', '.join(card_modifiers),
                                                                                                                    card_condition = card_condition,
                                                                                                                    card_language = card_language,
                                                                                                                    card_convertedManaCost = str(int(card_convertedManaCost)),
                                                                                                                    card_colorIdentity = card_colorIdentity ))

    def list_cards_deckstats_format(self,card_reference):
        """
        docstring
        """
        print(">> " + self.name + " collection :\n")
        sets = self.content.keys()
        number_of_cards = 0
        for set_name in sets :
            for card in self.content[set_name]:
                number_of_cards += 1
        print(str(number_of_cards) + " cards.\n")
        for set_name in sets :
            for card in self.content[set_name]:
                card_uuid = name_to_uuid[set_name][card[1]]
                card_language  = card[3]
                card_info_from_ref = card_reference[set_name][card_uuid]
                error = False
                card_name = card_info_from_ref['name']
                print("1 {card_name}".format(card_name = card_name ))

    def list_cards(self,card_reference):
        """
        docstring
        """
        print(">> " + self.name + " collection :\n")
        sets = self.content.keys()
        number_of_cards = 0
        for set_name in sets :
            for card in self.content[set_name]:
                number_of_cards += 1
        print(str(number_of_cards) + " cards.\n")
        for set_name in sets :
            for card in self.content[set_name]:
                card_uuid = name_to_uuid[set_name][card[1]]
                card_language  = card[3]
                card_info_from_ref = card_reference[set_name][card_uuid]
                error = False
                if card_language == 'EN' :
                    card_name = card_info_from_ref['name']
                else :
                    try :
                        card_name = card_info_from_ref['foreignName'][card_language]
                    except :
                        #print("Error on " + card_name)
                        error = True
                if not error:
                    print("1 {card_name}".format(card_name = card_name ))

    def look_for_card(self,cardname, cardset = None, resultset = None):
        """
        """
        if not resultset:
            resultset = []
        print('.Looking in '+ self.name)
        if cardset:
            for card in self.content[cardset]:
                if card[1] == cardname :
                    resultset.append([self.name,card])
        else :
            for cardset in self.content.keys():
                for card in self.content[cardset]:
                    if card[1] == cardname :
                        resultset.append([self.name,card])
        return(resultset)

def look_for_card_in_collections(cardname, collections, cardset = None):
    """
    """
    resultset = None
    for collection in collections:
        resultset = collection.look_for_card(cardname, cardset, resultset)
    return(resultset)

