import re
from os import environ
import sys

from cardcreator import render_card
from resources.exceptions import *
from resources.player import Player

'''
PATTERN is in the form '[Name,Position,Club,Country,Overall,PAC,DRI,SHO,DEF,PAS,PHY,CARD_CODE,LANGUAGE_CODE]'
- there is an optional space allowed after each comma in the list
- LANGUAGE_CODE is optional
Examples:
1) re will match [Messi,RW,241,AR,94,92,95,88,24,86,62,IF_GOLD]
2) re will match [Messi, RW, 241, AR, 94, 92, 95, 88, 24, 86, 62, IF_GOLD]
3) re will match [Messi, RW, 241, AR, 94, 92, 95, 88, 24, 86, 62, IF_GOLD, ES]
'''
    
p = re.compile(
    r'\[[a-zA-Z ]{1,30},[ ]?'
    r'[a-zA-Z]{2,4},[ ]?\d{1,10},[ ]?[a-zA-Z]{1,3},[ ]?'
    r'\d{1,2},[ ]?'
    r'\d{1,2},[ ]?\d{1,2},[ ]?'
    r'\d{1,2},[ ]?\d{1,2},[ ]?'
    r'\d{1,2},[ ]?\d{1,2},[ ]?'
    r'[a-zA-Z_]{1,20}'
    r'(,[ ]?[a-zA-Z]{2})?\]',
    re.IGNORECASE | re.VERBOSE)

args_p = re.compile(r'([-]{2}[A-Za-z]+)+')

def create(input, user, imagePath):

    params = re.search(p, input)
    
    if not params:
        return

    parameters = params.group()[1:-1].split(',')

    name = parameters[0].strip()
    position = parameters[1].strip()
    club = parameters[2].strip()
    country = parameters[3].strip()
    overall = parameters[4].strip()
    pac = parameters[5].strip()
    dri = parameters[6].strip()
    sho = parameters[7].strip()
    deff = parameters[8].strip()
    pas = parameters[9].strip()
    phy = parameters[10].strip()
    card_code = parameters[11].strip()

    # attempt to get the optional language code
    try:
        lang_code = parameters[12].strip().upper()
    except IndexError:
        lang_code = 'EN'

    if imagePath:
        image_url = imagePath
    else:
        image_url = None

    dynamic_fl = False
    #Initializes player and renders card
    try:
        player = Player(name, position, club, country, overall, pac, dri, sho, deff, pas, phy, lang_code)
        path_to_card_img = render_card(player, card_code, image_url, dynamic_fl, user)
    except FileNotFoundError as err:
        return
    except InvalidCardCodeError:
        return
    except InvalidCountryCodeError:
        return
    except InvalidClubNumberError:
        return
    except InvalidPositionError:
        return
    except InvalidLanguageError:
        return

    return path_to_card_img
