# UCSD Triton Rocket League - Discord Bot 

This bot was created for use in the University of California, San Diego Triton Rocket League ESports Community found on Discord. Rocket League is a vehicular soccer video game available on PC, PlayStation, Xbox, and Nintendo Switch developed and published by Psyonix. Described as "soccer, but with rocket-powered cars," Rocket League involves two teams that use rocket-powered vehicles to hit a ball into their opponent's goal and score points over the course of a match. Here at the Triton Rocket League Community, we host quarterly tournaments in which current UCSD students, alumni and friends compete in randomized teams of 3 to win the grand prize!

The tournaments hosted by Triton Rocket League Administrators (myself included) is structured as a five week commitment, where randomized teams of three players play four Best-of-5 series per week. Games are played and streamed in the late evening of Tuesdays and Thursdays. Teams are required save the replays of their game and submit them for tournament result verification. This bot stores replay files in a convenient way which allow for player statistics to be generated based on real in game data. 

# Community Links and Social Media 
- Discord: #TODO
- Twitch: #TODO
- Youtube: #TODO
- Ballchasing.gg: #TODO
- Facebook: #TODO
- Twitter: #TODO
- Instagram: #TODO

# Table of Contents 
- bot.py 
- replay_upload.py
- replay_grouper.py
- player_data_processing.py
- make_playercards.py

# Bot.py - Discord Replay Managment
## Added Features: Playercard Support from Replay Data (Fall 2020)

The tournaments we host for our gaming community typically span five weeks, and with an average of 10 teams playing 4 series per week. Each series of games played will have a minimum of three .replay files that need to be uploaded for verification. This means that we needed a way to conviently store .replay files uploaded on our Discord Server, thus the creation of this bot. 

### Setup 
Requirements - PIP stuff #TODO
Setup - Tokens #TODO
Execute - Run Bot.py #TODO

#### Upon Startup
In order to get started with this Bot, first follow all the instruction in the previous 'Setup' field. Then, simply run Bot.py. 

When bot.py is ran, this will be the startup message send to the designated bot channel. Below is an image of what this startup message would look like while in the server. 
![OnStartup]

#### Replay Managment 
In order to submit replays using the bot, users must use the "!rl_report". This will prompt the user to type out the results of the series they are trying to report. 
![!rl_report]
![!confirm]






