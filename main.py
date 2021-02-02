from config import sets_to_reference, ROOT_DIR, languages_to_reference
from openpyxl import Workbook
from pm_collections import collections, look_for_card_in_collections
from pm_card import card
from pm_reference import build_reference, download_JSON
from consolemenu import *
from consolemenu.items import *
import inspect
import json



if __name__ == "__main__":
    
    def init():
        reference = (card_reference, name_to_uuid, number_to_uuid, uuid_to_number) = build_reference(sets_to_reference)  

    def input_and_download():
        setname = input("Set to import: ")
        download_JSON([setname])

    menu = ConsoleMenu("Py Mint", "Management of MTG Cards collection and decks")

    function_download = FunctionItem("Download new sets description", input_and_download)
    function_init = FunctionItem("Parses the sets descriptions", init) # ["Set to import : "])

    menu.append_item(function_download)
    menu.append_item(function_init)
    menu.show()