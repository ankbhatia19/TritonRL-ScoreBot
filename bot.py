# Discord Rocket League Replay Management Bot
# Author: David Marcus Thierry

# Date: October 18, 2020 - Current 

import os 
import re
import json
import discord
from discord import Embed
from datetime import date
from discord.ext import commands

# Load in confidential data needed in order to run the bot 
# Also load in all the text strings the bot will be using 

CFG_PARAMS = 'config/cfg.json'
SETUP_PARAMS = 'config/setup.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)
    return param

CFG = load_params(CFG_PARAMS)
SETUP = load_params(SETUP_PARAMS)

# The messages the bot will use
startup_msg = SETUP['startup_msg']
console_start_msg = SETUP['console_start_msg']
card_img_request =  SETUP['card_img_request']
playercard_folder_404 =  SETUP['playercard_folder_404']
playercard_stats_msg =  SETUP['playercard_stats_msg']
playercard_404 =  SETUP['playercard_404']
rlreport_start_msg = SETUP['rlreport_start_msg']
rlreport_upload_msg = SETUP['rlreport_upload_msg']
replays_folder_404 = SETUP['replays_folder_404']
confirm_startup_msg = SETUP['confirm_startup_msg']
embed_title = SETUP['embed_title']
embed_desc = SETUP['embed_desc']
team_img_404 = SETUP['team_img_404']
follow_up = SETUP['follow_up']

# The channel in which the bot will operate 
channel_id = CFG['server_channel_id']

# Initialize the bot client
client = discord.Client()

# Global Variables and information
date = date.today()
formatted_date = date.strftime("%m_%d_%y")
emoji = '\N{THUMBS UP SIGN}'
game_meta = {}
saved = []

###  Helpers Functions ###
# Parse intial input 
def parse_initial_msg(msg):
    split = msg.split('\n')
    d = {}
    for x in split: 
        if x != '!rl_report':
            split = x.split(': ')
            # This line removes spaces from embed team names, replaced with no space removal
            # d[split[0].strip(':')] = split[1].replace(' ', '')
            d[split[0].strip(':')] = split[1]
    return d
# Find winner 
def winner(d):
    score = d['Score']
    h = d['Home']
    a = d['Away']
    parse = score.split('-')
    if int(parse[0]) > int(parse[1]):
        return ('Congratulations {0}!'.format(h), h, a, h)
    else:
        return ('Congratulations {0}!'.format(a), h, a, a)

# Handling Events 
@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    await channel.send(startup_msg)
    print(console_start_msg)

@client.event 
async def on_message(message):
    global saved
    global winners

    # Make sure the bot doesnt reply to itself 
    if client.user.id != message.author.id:
        # Go to the correct channel 
        channel = client.get_channel(channel_id) 

# """ This if statement will manage discord users uploading their own playercard image """
        if message.content.startswith('!card_img'):
            await message.channel.send(card_img_request)
            
            # Console 
            print('{0} has attempted to upload an image'.format(message.author))
            
            def check(m):
                # Check is to make sure the person who called this event is the one replying 
                # Check that it is from the same channel 
                # Check that the message contains an attachment 
                return m.author == message.author and m.channel == channel and bool(m.attachments)

            # Call the check and then save the image to a variable 
            msg = await client.wait_for('message', check=check) #timeout = 10.0)
            player_img = msg.attachments[0]

            # Check to see if 'playercard_imgs' folder exists 
            # Not sure if this replace is even necessary but it works 
            # Goal here was to make every filepath relative from the root directory
 
            filepath = str(os.getcwd()) + '\\' + 'playercard_imgs' + '\\'
            formatted_fp = filepath.replace('\\', '/')

            # Create replay folder if it doesnt exist 
            if not os.path.exists(formatted_fp): 
                print(playercard_folder_404)
                os.mkdir(formatted_fp) 
            
            # Current dir fp : C:\Users\dmarc\TritonRL-ScoreBot\playercard_imgs
            # img_fp : \playercard_imgs\player.png

            #TODO FIX REGEX FOR SPLIT 

            author = str(msg.author).split('#')[0]
            print('{0} has saved a new playercard image'.format(author))
            image_fp = formatted_fp + author + '.png'

            # Save the image
            await player_img.save(fp = image_fp)

# """ This if statement will allow discord users to see their own generated playercard """
        if message.content.startswith('!my_playercard'):
            await message.channel.send(playercard_stats_msg)
            # Console 
            print('{0} has attempted to view their playercard'.format(message.author))
            # Get the author of the msg as reference, this should match up with whomever uploads a card image

            author = str(message.author).split('#')[0]
            # Check to see if a playercards directory exists 
            filepath = str(os.getcwd()) + '\\' + 'playercards' + '\\'
            formatted_fp = filepath.replace('\\', '/')

            # TODO ADD A CHECK TO SEE IF PLAYERCARD EXISTS
            filename = formatted_fp + author + '.png'
            # If the playercard does exist
            if os.path.exists(filename): 
                # Send a picture of message authors playercard to discord channel
                await channel.send(file=discord.File(filename))
            # Otherwise, display an error 
            else: 
                await message.channel.send(playercard_404)
            
# """ This if statement will deal with replay management """
        if message.content.startswith('!rl_report'):
            # Console 
            print('{0} is attempting to report a series scores'.format(message.author))
            await message.channel.send(rlreport_start_msg)


            def check_details(m):
                # Check is to make sure the person who called this event is the one replying
                # Check to make sure message came from same channel as bot 
                # Check that the details are reported correctly 
                # pattern = r'Week: \d\nHome: \w+\nAway: \w+\nScore: \d-\d\nMVP: \w+ ?'
                pattern = r'Week: \d ?\nHome: \w+ ?\w+ ?\w+ ?\w+ ?\nAway: \w+ ?\w+ ?\w+ ?\w+ ?\nScore: \d-\d ?'
                check = bool(re.match(pattern, m.content))
                return m.author == message.author and m.channel == channel and check

            # Call the check and then the response into a variable 
            user_input = await client.wait_for('message', check=check_details) # timeout = 10.0)
            # Get the reported content from the discord message
            report = user_input.content
            # save the name of the user who is reporting the score into a dictionary
            report_details = parse_initial_msg(report)
            # Get all relevant info into variables from the report dictionary 
            # week = report_details['Week']
            home = report_details['Home']
            away = report_details['Away']
            # score = report_details['Score']
            # MVP = report_details['MVP']
            winners = winner(report_details)



            await message.channel.send(rlreport_upload_msg)
            # Initialize filepaths 
            filepath = str(os.getcwd()) + '/' + 'replays' + '/'
            formatted_fp = filepath.replace('\\', '/')
            # Create replay folder if it doesnt exist 
            if not os.path.exists(formatted_fp): 
                print(replays_folder_404)
                os.mkdir(formatted_fp) 

            def check_replay(m):    
                # Check is to make sure the person who called this event is the one replying
                # Check to make sure message came from same channel as bot 
                # Check to see if message contains attachments 
                attachments = m.attachments
                if len(attachments) == 0:
                    return False
                attachment = attachments[0]
                return m.author == message.author and m.channel == channel and attachment.filename.endswith(('.replay'))

            replays_uploaded = 0
            game = 1
            while replays_uploaded < 5:
                replay_input = await client.wait_for('message', check=check_replay)#, timeout = 20.0)
                replays = replay_input.attachments
                replays_uploaded += len(replays)

                for attachment in replays:
                    # Generate filename
                    match_name = home.lower() + '_vs_' + away.lower() + '_' + str(formatted_date)
                    print('match name: {0}'.format(match_name))
                    # If this is the first upload, name it game 1 of the series
                    game_number = match_name + '_g{0}'.format(str(game))
                    # If it is not the first game of the series, adjust game counter accordingly
                    # saved is the global variable containing all of the saved game names
                    if game_number in saved:
                        game += 1
                        game_number = match_name + '_g{0}'.format(str(game))
                        saved.append(game_number) 
                    else: 
                        saved.append(game_number)

                    # Save game to replays folder and add reaction to confirm save
                    await attachment.save(fp = formatted_fp + game_number + '.replay')
                    print(game_number + '.replay' + ' : Saved' )
                    await replay_input.add_reaction(emoji)   
            
# """ This if statement will deal with replay management """
        if message.content.startswith('!confirm'):
            # Console 
            print('{0} is done reporting series scores'.format(message.author))

            home = winners[1]
            away = winners[2]
            win_team = winners[3]
            await message.channel.send(confirm_startup_msg)

            # Intialize the embedded visual
            embed = Embed(
                title = embed_title, 
                description = embed_desc
                )
            fields = [
                ("Home Team", home, True), 
                ("Away Team", away, True),
                ("Outcome", winners[0], False)
                ]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            # Ask for and save replay files locally. 
            embed.set_footer(text = follow_up)
 
            # This is where it is important that upon submission the team uses their full name
            # The teams name will have a similarily named team photo, where its filepath will be generated
            # from the users input.
            directory = str(os.getcwd()) + '\\' + 'team_images' + '\\'
                        
            # Send the embedded window to the channel with match details 
            await message.channel.send(embed = embed)

            # TODO FIX THIS SO ITS MORE RELIABLE

            image_type = '.png'
            fp = directory + win_team + image_type
            filename = fp.replace('\\', '/') 

            # If the team image directory does exist
            if os.path.exists(directory): 
                # Send a picture of message authors playercard to discord channel
                await channel.send(file=discord.File(filename))
            # Otherwise, display an error (Fix later)
            else: 
                await message.channel.send(team_img_404)


# Run the client on the server
server_token = CFG['server_token']
client.run(server_token)

# client.close()
