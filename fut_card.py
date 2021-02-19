import re
from os import environ
import sys

from cardcreator import render_card
from src.playercard_generation.style.exceptions import *
from src.playercard_generation.style.player import Player

# Default Images 
default_rank = 'https://cdn.discordapp.com/attachments/766119517503619097/805555338807345162/white-question-mark-emoji-removebg-preview.png' # Default Unknown Rank
default_logo = 'https://cdn.discordapp.com/attachments/764281194631397416/772652236249104384/tritonrl_logo-removebg-preview_1.png' # Triton Rocket League Logo
default_img = 'c:\\Users\\dmarc\\OneDrive\\Documents\\Github\\Personal Projects\\TritonRL-ScoreBot\\assets\\default_imgs\\default_player_avatar.png' # Locked Character Avatar

def create(player_information, player_name):
    dynamic_fl = False
    # Now we have if they used !update_name, then the file will be saved as their specified name
    # Otherwise, the file is saved under their ballchasing name. In order to access it, they need to use 
    # the '!update_name' command
    card_name = player_information['playercard_name']
    position_ovr = 'OVR'
    r = int(player_information['Overall'])
    rating = str(r)
    off_stat = str(int(player_information['Offense']))
    def_stat = str(int(player_information['Defense']))
    agg_stat = str(int(player_information['Aggression']))
    spd_stat = str(int(player_information['Speed']))
    win_stat = str(int(player_information['win rate']*100))
    rank_stat = str(int(player_information['index']))

    #choose card type based off of overall
    if r > 90:
        card_code = "Freeze"
    elif r > 80:
        card_code = "Headliners"
    elif r > 70:
        card_code = "Gold"
    elif r > 60:
        card_code = "Silver"
    else:
        card_code = "Bronze"

    # Check to see if player updated their playercard name, otherwise use their ballchasing name. 
    # This will also be the name of the playercard file after it is saved locally. 
    if card_name != 'N/A':
        card_name = card_name
    else:
        card_name = player_name

    # Check to see if nation key (rank) is 'N/A', if it isnt 'N/A', get image fp from the dictionary.
    player_rank = str(player_information['rank'])
    if player_rank != 'N/A':
        rank_img = player_rank
    else:
        rank_img = default_rank

    # Check to see if avatar key is 'N/A', if it isnt 'N/A', get image fp from the dictionary.
    avatar_key = player_information['img_filepath']
    if avatar_key != 'N/A':
        avatar = avatar_key
    else:
        avatar = r'.assets\default_imgs\default_player_avatar.png'

    # attempt to get the optional language code later on
    lang_code = 'EN'

    try:
        player = Player(
            card_name, 'OVR', rank_img, 'TRL', 
            rating, off_stat, def_stat, agg_stat, spd_stat, win_stat, 
            rank_stat, lang_code
            )
        path_to_card_img = render_card(
            player, card_code, avatar, dynamic_fl, player_name # avatar is used for image_url argument
            )

    except FileNotFoundError as err:
        print('File not found')
        return
    except InvalidCardCodeError:
        print('invalid card code')
        return
    except InvalidCountryCodeError:
        print('invalid country code')
        return
    except InvalidClubNumberError:
        print('invalid club error')
        return
    except InvalidPositionError:
        print('invalid position error')
        return
    except InvalidLanguageError:
        print('invalid language error')
        return

    return path_to_card_img





# '''
# PATTERN is in the form '[Name,Position,Club,Country,Overall,PAC,DRI,SHO,DEF,PAS,PHY,CARD_CODE,LANGUAGE_CODE]'
# - there is an optional space allowed after each comma in the list
# - LANGUAGE_CODE is optional
# Examples:
# 1) re will match [Messi,RW,241,AR,94,92,95,88,24,86,62,IF_GOLD]
# 2) re will match [Messi, RW, 241, AR, 94, 92, 95, 88, 24, 86, 62, IF_GOLD]
# 3) re will match [Messi, RW, 241, AR, 94, 92, 95, 88, 24, 86, 62, IF_GOLD, ES]
# '''
    
# p = re.compile(
#     r'\[[a-zA-Z ]{1,30},[ ]?'
#     r'[a-zA-Z]{2,4},[ ]?\d{1,10},[ ]?[a-zA-Z]{1,3},[ ]?'
#     r'\d{1,2},[ ]?'
#     r'\d{1,2},[ ]?\d{1,2},[ ]?'
#     r'\d{1,2},[ ]?\d{1,2},[ ]?'
#     r'\d{1,2},[ ]?\d{1,2},[ ]?'
#     r'[a-zA-Z_]{1,20}'
#     r'(,[ ]?[a-zA-Z]{2})?\]',
#     re.IGNORECASE | re.VERBOSE)

# args_p = re.compile(r'([-]{2}[A-Za-z]+)+')

# def create(input, user, imagePath):

#     params = re.search(p, input)
    
#     if not params:
#         return

#     parameters = params.group()[1:-1].split(',')

#     name = parameters[0].strip()
#     position = parameters[1].strip()
#     club = parameters[2].strip()
#     country = parameters[3].strip()
#     overall = parameters[4].strip()
#     pac = parameters[5].strip()
#     dri = parameters[6].strip()
#     sho = parameters[7].strip()
#     deff = parameters[8].strip()
#     pas = parameters[9].strip()
#     phy = parameters[10].strip()
#     card_code = parameters[11].strip()

#     # attempt to get the optional language code
#     try:
#         lang_code = parameters[12].strip().upper()
#     except IndexError:
#         lang_code = 'EN'

#     if imagePath:
#         image_url = imagePath
#     else:
#         image_url = None

#     dynamic_fl = False
#     #Initializes player and renders card
#     try:
#         player = Player(name, position, club, country, overall, pac, dri, sho, deff, pas, phy, lang_code)
#         path_to_card_img = render_card(player, card_code, image_url, dynamic_fl, user)
        
#     except FileNotFoundError as err:
#         return
#     except InvalidCardCodeError:
#         return
#     except InvalidCountryCodeError:
#         return
#     except InvalidClubNumberError:
#         return
#     except InvalidPositionError:
#         return
#     except InvalidLanguageError:
#         return

#     return path_to_card_img
