# Discord Rocket League Replay and Playercard Management Bot
# Author: David Marcus Thierry

# Date: October 18, 2020 - Current 

import os 
import json
import discord
import regex as re
import pandas as pd
from discord import Embed
from datetime import date
from discord.ext import commands
import generate_playercards as gp

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
player_ranks = {}
playercard_names = {}

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
    await channel.send('The available bot commands are listed below.\n\n\nReplay Managment Commands\n> !rl_report -> Report series replays.\n> !confirm -> Confirm replay uploads.\n\n\nPlayercard Related Commands\n> !playercard_img -> Change your playercard avatar\n> !playercard_rank -> Change your 3\'s rank on your playercard.\n> !playercard_name -> Change the name on your playercard.\n> !my_playercard -> View your playercard.\n\nPlease note: All playercard visual changes made today will be available the next time this bot is online.')
    print(console_start_msg)

@client.event 
async def on_message(message):
    global saved
    global winners
    global player_ranks
    global playercard_names

    # Make sure the bot doesnt reply to itself 
    if client.user.id != message.author.id:
        # Go to the correct channel 
        channel = client.get_channel(channel_id) 
  
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
            
# """ This if statement will deal with replay confirmation """
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

# """ This if statement will manage discord users uploading their own playercard image """
        if message.content.startswith('!playercard_img'):
            await message.channel.send('Please crop your image using this website BEFORE uploading the image.\nhttps://www.remove.bg/')
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

            author = str(msg.author)
            print('{0} has saved a new playercard image'.format(author))
            image_fp = formatted_fp + author + '.png'

            # Save the image
            await player_img.save(fp = image_fp)
            await message.channel.send('Update complete!')

# """ This if statement will manage discord users updating their 3v3 rank """
        if message.content.startswith('!playercard_rank'):
            
            await message.channel.send("Your playercard rank is now the rank you gave yourself in the '#get-roles' channel")

            rank_counter = 0
            role_dictionary = {
                'Supersonic Legend': 755914706148917368,
                'Grand Champion III': 755915056805576734,
                'Grand Champion II': 755914957308297349,
                'Grand Champion I': 755914226438242374,
                'Champion III': 504051890125012995,
                'Champion II': 504051805739679778,
                'Champion I': 504051761481515045,
                'Diamond III': 504051711292473364,
                'Diamond II': 504051663473082379,
                'Diamond I': 504051582321688589,
                'Platinum III': 504054978336522241,
                'Platinum II': 666151884201132062,
                'Platinum I': 666153168438165544,
                'Gold III': 666152671622987786,
                'Gold II': 666152330416226305,
                'Gold I': 666152084986396692,
                'Silver III': 666152784277536768,
                'Silver II': 666152711112228874,
                'Silver I': 666152318177116190,
                'Bronze III': 666152322962948106,
                'Bronze II': 666152212438712320,
                'Bronze I': 666152091294892064,
            }

            while rank_counter < 1:
                for role in message.author.roles:
                    if role.name in role_dictionary.keys():
                        author = str(message.author)
                        player_ranks[author] = role.name
                        rank_counter += 1 

            with open("output/player_ranks.json", "w") as outfile:  
                json.dump(player_ranks, outfile) 

            await message.channel.send("Update complete!")

# """ This if statement will allow players to change their name visible on playercards """
        if message.content.startswith('!playercard_name'):

            leaderboard_fp = r'.\leaderboard_imgs\winter_wk3_leaderboard.png'
            # If the playercard does exist
            if os.path.exists(leaderboard_fp): 
                # Send a picture of message authors playercard to discord channel
                await message.channel.send(file=discord.File(leaderboard_fp))

            await message.channel.send("Please use this format provided to change your playercard name.\n\nLeaderboard Name: [Name]\nDesired Playercard Name: [New name]\n\nFor Reference, here are the current league standings. Use the name you find there as your 'Leaderboard Name' input.")

            def check_name_details(m):
                # Check is to make sure the person who called this event is the one replying
                # Check to make sure message came from same channel as bot 
                # Check that the name updates are reported correctly 

                # name_pattern = r'Leaderboard Name: \w* ?\nDesired Playercard Name: \w* ?'
                # kameron_name_pattern_patch = r'Leaderboard Name: \w* ?\(\w* \w*\)\nDesired Playercard Name: \w* ?'
                best_pattern_match = r'Leaderboard Name: [\w ()\X\S]*\nDesired Playercard Name: [\w ()\X\S]* ?\n?'
                check = bool(re.match(best_pattern_match, m.content))
                return m.author == message.author and m.channel == channel and check

            # Call the check and then the response into a variable 
            name_input = await client.wait_for('message', check=check_name_details)
            user_input = name_input.content
            leaderboard_name, playercard_name = user_input.split('\n')

            leaderboard_name = leaderboard_name.split(': ')[1]
            playercard_name = playercard_name.split(': ')[1]
            tup = (leaderboard_name, playercard_name)
            playercard_names[str(message.author)] = tup

            # # Output Data Files 
            DATA_FILENAME = r'.\output\playercard_names.csv'
  
            # If the custom playercard exists
            if not os.path.exists(DATA_FILENAME): 
                name_data = pd.DataFrame(
                    [[str(message.author), leaderboard_name, playercard_name]], 
                    columns = ['message_author','leaderboard_name', 'playercard_name']
                    )
                name_data.to_csv(DATA_FILENAME, mode = 'w')
            else: 
                # In this case, keep all name changes and save them to file. Duplicates will 
                # be removed when dataframe is reingested 
                df = pd.read_csv(DATA_FILENAME)
                name_data = pd.DataFrame(
                    [[str(message.author), leaderboard_name,playercard_name]],
                    columns =['message_author','leaderboard_name','playercard_name']
                    )
                name_data.to_csv(DATA_FILENAME, mode='a', header=False)

            await message.channel.send("Update complete!")

# """ This if statement will allow discord users to see their own generated playercard """
        if message.content.startswith('!my_playercard'):
            await message.channel.send(playercard_stats_msg)
            # Console 
            print('{0} has attempted to view their playercard'.format(message.author))

            # Get the author of the msg as reference, this should match up with whomever uploads a card image
            author = str(message.author)
            player_names_fp = r'.\output\playercard_names.csv'
            df = pd.read_csv(player_names_fp, index_col=0)
            df = df.drop_duplicates(subset=['message_author', 'leaderboard_name'], keep='last')
            df = df.set_index('message_author')

            # If they have already ran the !playercard_name command, the try block runs. 
            try:
                ballchasing_name, playercard_name = df.loc[author]['leaderboard_name'], df.loc[author]['playercard_name']
                # Check to see if a playercards directory exists 
                filepath = str(os.getcwd()) + '\\' + 'playercards' + '\\'
                formatted_fp = filepath.replace('\\', '/')
                default_fp = formatted_fp + ballchasing_name + '.png'
                custom_fp = formatted_fp + playercard_name + '.png'
                # Cant use this because discord requires an absolute path to send a file 
                # custom_fp = r'./playercards/{0}.png'.format(playercard_name)
                custom_exists = False
                if os.path.exists(custom_fp): 
                    await channel.send(file=discord.File(custom_fp))
                    custom_exists = True
                elif not custom_exists: # If the custom playercard does not exist
                    await channel.send(file=discord.File(default_fp)) 
                else: # Otherwise, display the error
                    await message.channel.send(playercard_404)

            except:
                await message.channel.send('You must first use the "!playercard_name" command before viewing your playercard.')

            output_df = df.reset_index()
            player_names_fp = r'.\output\playercard_names.csv'
            output_df.to_csv(player_names_fp)

# """ This if statement will allow discord users 1 chance to regenerate their playercard per day"""
        if message.content.startswith('!generate_playercard'):
            print('Not Implemented')
            # dataset = r'.\output\playercard_stats.csv'
            # df = pd.read_csv(dataset, index_col=0)
            # df = df.fillna('N/A')
            # player = 'goofy'
            # print(gp.generate_playercard(df, player))
            # await message.channel.send('Success! Use the !my_playercard command to see changes!')

# # Run the client on the server
server_token = CFG['server_token']
client.run(server_token)

# client.close()
