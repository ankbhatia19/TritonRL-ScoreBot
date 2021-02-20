import os
import io
import time
import json
import urllib
import math 
import selenium
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def initialize_browser(download_dir_path = './playercards/'):
    # Selenium Webdriver Initialization
    # chromedriver = r'C:\webdriver\chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    start_directory = os.getcwd()

    # Set up the playercard folder, if it doesnt exist, create one. 
    filepath = start_directory + '\\' + 'playercards' + '\\'
    formatted_fp = filepath.replace('\\', '/')
    prefs = {"download.default_directory": formatted_fp}
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(3) # seconds
    browser.set_page_load_timeout(30)
    browser.maximize_window() 
    browser.get('https://www.fifarosters.com/create-card')

    playercard_dir = './playercards/'
    if not os.path.exists(playercard_dir): 
        print('Creating local playercards directory')
        os.mkdir(playercard_dir) 

    return browser

def generate_playercard(dataframe, browser, player = 'goofy'):
    
    print('Generating {0}\'s playercard'.format(player))

    def sleepy(sec):
        time.sleep(sec)
        return

    # Waiting for page to load
    print('waiting for page to load')

    # ALL XPATHS NEEDED #
    official_cards = '//*[@id="card_selector_btn"]'
    # 5 categories of playercards to cateogrize player distribution
    tiered_playercards = {
        'bronze':'//*[@id="card_selector_modal_21"]/div/div/div[2]/div/div[4]/a',
        'silver':'//*[@id="card_selector_modal_21"]/div/div/div[2]/div/div[5]/a',
        'gold':'//*[@id="card_selector_modal_21"]/div/div/div[2]/div/div[6]/a',
        'champ':'//*[@id="card_selector_modal_21"]/div/div/div[2]/div/div[35]/a', 
        'legend':'//*[@id="card_selector_modal_21"]/div/div/div[2]/div/div[24]/a'
    }
    # Upload player desired image
    upload_img = '//*[@id="form-image-type-upload"]'
    choose_file = '//*[@id="form-card-upload-image"]'
    # Player Information
    input_name = '//*[@id="form-card-name"]'
    overall_rating = '//*[@id="form-card-rating"]'
    position = '//*[@id="form-card-position"]'
    club_field = '//*[@id="form-card-club-text"]'
    nation_rank = '//*[@id="form-card-nation-text"]'
    #Attributes
    offense = '//*[@id="form-card-attr1-text"]'
    ostat = '//*[@id="form-card-attr1"]'
    aggression = '//*[@id="form-card-attr2-text"]'
    astat = '//*[@id="form-card-attr2"]'
    winrate = '//*[@id="form-card-attr3-text"]'
    wstat = '//*[@id="form-card-attr3"]'
    defense = '//*[@id="form-card-attr4-text"]'
    dstat = '//*[@id="form-card-attr4"]'
    speed = '//*[@id="form-card-attr5-text"]'
    sstat = '//*[@id="form-card-attr5"]'
    ranking = '//*[@id="form-card-attr6-text"]'
    rstat = '//*[@id="form-card-attr6"]'
    # Formatting and download
    thin_letters = '//*[@id="createCardForm"]/div[18]/div/div/div/label[2]'
    download = '//*[@id="main_row"]/div[2]/div/div/button'

    # Pictures of the ranks found in rocket league
    rank_images = {
        'Supersonic Legend': 'https://cdn.discordapp.com/attachments/805954757704417360/805957358152187924/SSL_smol.png',
        'Grand Champion III': 'https://cdn.discordapp.com/attachments/805954757704417360/805957462124658688/GC3.png',
        'Grand Champion II': 'https://cdn.discordapp.com/attachments/805954757704417360/805957458328551505/GC2.png',
        'Grand Champion I': 'https://cdn.discordapp.com/attachments/805954757704417360/805957454037909534/GC1.png',
        'Champion III': 'https://cdn.discordapp.com/attachments/805954757704417360/805959195794997268/C3.png',
        'Champion II': 'https://cdn.discordapp.com/attachments/805954757704417360/805958920018591754/C2.png',
        'Champion I': 'https://cdn.discordapp.com/attachments/805954757704417360/805958913454768149/C1.png',
        'Diamond III': 'https://cdn.discordapp.com/attachments/805954757704417360/805959243307417622/D2.png',
        'Diamond II': 'https://cdn.discordapp.com/attachments/805954757704417360/805959240132067328/D1.png',
        'Diamond I': 'https://cdn.discordapp.com/attachments/805954757704417360/805959240132067328/D1.png',
        'Platinum III': 'https://cdn.discordapp.com/attachments/805954757704417360/805959311276376124/P3.png',
        'Platinum II': 'https://cdn.discordapp.com/attachments/805954757704417360/805959307153375242/P1.png',
        'Platinum I': 'https://cdn.discordapp.com/attachments/805954757704417360/805959307153375242/P1.png',
        'Gold III': 'https://cdn.discordapp.com/attachments/805954757704417360/805959370226794506/G3.png',
        'Gold II': 'https://cdn.discordapp.com/attachments/805954757704417360/805959370226794506/G2.png',
        'Gold I': 'https://cdn.discordapp.com/attachments/805954757704417360/805959368348532786/G1.png',
        'Silver III': 'https://cdn.discordapp.com/attachments/805954757704417360/805959373742145556/S3.png',
        'Silver II': 'https://cdn.discordapp.com/attachments/805954757704417360/805959373742145556/S2.png',
        'Silver I': 'https://cdn.discordapp.com/attachments/805954757704417360/805959373742145556/S1.png',
        'Bronze III': 'https://cdn.discordapp.com/attachments/805954757704417360/805959365206212638/B3.png',
        'Bronze II': 'https://cdn.discordapp.com/attachments/805954757704417360/805959362941550613/B2.png',
        'Bronze I': 'https://cdn.discordapp.com/attachments/805954757704417360/805959360575963166/B1.png'
    }

    # Default Images 
    default_rank = 'https://cdn.discordapp.com/attachments/766119517503619097/805555338807345162/white-question-mark-emoji-removebg-preview.png' # Default Unknown Rank
    default_logo = 'https://cdn.discordapp.com/attachments/764281194631397416/772652236249104384/tritonrl_logo-removebg-preview_1.png' # Triton Rocket League Logo
    default_img = 'c:\\Users\\dmarc\\OneDrive\\Documents\\Github\\Personal Projects\\TritonRL-ScoreBot\\default_imgs\\default_player_avatar.png' # Locked Character Avatar

    # Season Statistics
    dataset = 'output/playercard_stats.csv'
    df = pd.read_csv(dataset, index_col=0)
    df = df.fillna('N/A')
    dd = df.to_dict('index')
    
    # FIFA playercard generation 
    club = default_logo
    nation_key = str(dd[player]['rank'])
    # Check to see if nation key is 'N/A', if it isnt 'N/A', get image fp from the dictionary.
    if nation_key != 'N/A':
        nation = rank_images[nation_key]
    else:
        nation = default_rank

    avatar_key = dd[player]['img_filepath']
    # Check to see if avatar key is 'N/A', if it isnt 'N/A', get image fp from the dictionary.
    if avatar_key != 'N/A':
        avatar = avatar_key
        avatar_flag = False
    else:
        avatar = default_img
        avatar_flag = True

    card_name = dd[player]['playercard_name']
    # Check to see if player updated their playercard name, otherwise use their ballchasing name. 
    # This will also be the name of the playercard file after it is saved locally. 
    if card_name != 'N/A':
        card_name = card_name
    else:
        card_name = player

    # Now we have if they used !update_name, then the file will be saved as their specified name
    # Otherwise, the file is saved under their ballchasing name. In order to access it, they need to use 
    # the '!update_name' command

    position_ovr = 'OVR'
    rating = str(int(dd[player]['Overall']))
    off_stat = str(int(dd[player]['Offense']))
    def_stat = str(int(dd[player]['Defense']))
    agg_stat = str(int(dd[player]['Aggression']))
    spd_stat = str(int(dd[player]['Speed']))
    win_stat = str(int(dd[player]['win rate']*100))
    rank_stat = str(int(dd[player]['ranking']))

    # Let the webpage load
    # Delete the ad
    browser.find_element_by_xpath('//*[@id="ezmobfooter"]/span').click()
    # Select the correct card for the player
    browser.find_element_by_xpath('//*[@id="card_selector_btn"]').click()
    
    sleepy(1)
    if int(rank_stat) <= 5:
        tier = tiered_playercards['legend']
    if int(rank_stat) > 5 and int(rank_stat) <= 15:
        tier = tiered_playercards['champ']
    if int(rank_stat) > 15 and int(rank_stat) <=25:
        tier = tiered_playercards['gold']
    if int(rank_stat) > 25 and int(rank_stat) <= 35:
        tier = tiered_playercards['silver']
    if int(rank_stat) > 35 and int(rank_stat) <= 50:
        tier = tiered_playercards['bronze']
    
    browser.find_element_by_xpath(tier).click()

    # sleepy(2)

    # Upload the players image
    browser.find_element_by_xpath('//*[@id="form-image-type-upload"]').click()
    browser.find_element_by_xpath(choose_file).clear()
    browser.find_element_by_xpath(choose_file).send_keys(avatar)
    # sleepy(2)

    # Scale the players image
    if avatar_flag == True: 
        browser.find_element_by_xpath('//*[@id="form-card-upload-size"]').click()
        browser.find_element_by_xpath('//*[@id="form-card-upload-size"]').clear()
        browser.find_element_by_xpath('//*[@id="form-card-upload-size"]').send_keys('90')

    # Sends text to the field corresponding to player name
    browser.find_element_by_xpath(input_name).clear()
    browser.find_element_by_xpath(input_name).send_keys(card_name)

    # Enter the players overall rating
    browser.find_element_by_xpath(overall_rating).clear()
    browser.find_element_by_xpath(overall_rating).send_keys(rating)

    # Enter the players position (subsituted with overall text)
    browser.find_element_by_xpath(position).clear()
    browser.find_element_by_xpath(position).send_keys(position_ovr)

    # Enter the players home club
    browser.find_element_by_xpath(club_field).clear()
    browser.find_element_by_xpath(club_field).send_keys(club)

    # Enter the players max rank during this tournament duration
    browser.find_element_by_xpath(nation_rank).clear()
    browser.find_element_by_xpath(nation_rank).send_keys(nation)

    
    # Clear and populate attribute fields
    browser.find_element_by_xpath(offense).clear()
    browser.find_element_by_xpath(defense).clear()
    browser.find_element_by_xpath(aggression).clear()
    browser.find_element_by_xpath(speed).clear()
    browser.find_element_by_xpath(winrate).clear()
    browser.find_element_by_xpath(ranking).clear()
    browser.find_element_by_xpath(ostat).clear()
    browser.find_element_by_xpath(dstat).clear()
    browser.find_element_by_xpath(astat).clear()
    browser.find_element_by_xpath(sstat).clear()
    browser.find_element_by_xpath(wstat).clear()
    browser.find_element_by_xpath(rstat).clear()
    browser.find_element_by_xpath(offense).send_keys('OFF')
    browser.find_element_by_xpath(aggression).send_keys('AGG')
    browser.find_element_by_xpath(winrate).send_keys('W%')
    browser.find_element_by_xpath(defense).send_keys('DEF')
    browser.find_element_by_xpath(speed).send_keys('SPD')
    browser.find_element_by_xpath(ranking).send_keys('Rank')
    browser.find_element_by_xpath(ostat).send_keys(off_stat)
    browser.find_element_by_xpath(astat).send_keys(agg_stat)
    browser.find_element_by_xpath(wstat).send_keys(win_stat)
    browser.find_element_by_xpath(dstat).send_keys(def_stat)
    browser.find_element_by_xpath(sstat).send_keys(spd_stat)
    browser.find_element_by_xpath(rstat).send_keys(rank_stat)

    # Formatting and Download
    browser.find_element_by_xpath('//*[@id="createCardForm"]/div[18]/div/div/div/label[2]').click()
    browser.find_element_by_xpath('//*[@id="main_row"]/div[2]/div/div/button').click()
    
    # browser.close()

    return 'Done'

