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

# Bot.py - Discord Replay Upload Managment Bot 
The tournaments we host for our gaming community typically span five weeks, and with an average of 10 teams playing 4 series per week. Each game will have one replay file associated with it, and this .replay file will contain game_information such as ball position, player positioning, total shots per player, total saves per player and more. Each series of games played will have a minimum of three .replay files that need to be uploaded for tournament result verification purposes. This means that we needed a way to conviently store .replay files uploaded on our Discord Server, thus the creation of this bot. 

### Setup 
- Requirements - PIP stuff #TODO
- Setup - Tokens #TODO
- Execute - Run Bot.py #TODO

### Startup
In order to get started with this Bot, first follow all the instruction in the previous 'Setup' field. Then, simply run Bot.py. When bot.py is ran, this will be the startup message send to the designated bot channel. Below is an image of what this startup message would look like while in the server.

![OnStartup](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/on_startup.png)

### Replay Upload Process (Participant Perspective) 
In order to submit replays using the bot, users must use the "!rl_report" command in order to start the submission process. This will prompt the user to type out the results of the series they are trying to report. Results must be reported using a specified format. The image below is an example of a tournament participant reporting their series replays. 

![!rl_report](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!rl_report.png)

After the participant uploads their replays, they will then be asked to confirm their submission.

![!confirm](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!confirm.png)

That is all the tournament participants must do to submit their series replays. The images below are for the person hosting this bot service. 

### Replay Upload Process (Bot Host Perspective) 

The individual running the bot will be running it from their local system, and all uploaded replays will be named according to user input and saved in a "replays" folder. If this "replays" folder does not already exist, one will be created locally.

![!replay_folder](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/replay_folder.png)

After all replays for any given match day are uploaded, they will appear in the replays folder as I previously said. The bot host can run the replay_upload.py file. When this python script is ran, it will upload each replay to the ballchasing.com replay account. Ballchasing.com is an online service which allows users to upload their Rocket League replay files and parse game information for all players in that particular game. By uploading these files to this site, I did not need to write my own .replay file parser. 

When the replay_upload.py script finishes runinng, the script will save a file to the output folder. The output folder is a folder that contains any important data generated that may be needed at a later time. First, the script checks to see if an output folder exists, and if it doesnt, it will make a local folder. The replays uploaded can now be found on the hosts ballchasing.com account. It would appear under their profile as such. There is one last step in managing these replay files, they must be moved from a users 'my replays' on ballchasing.com to a customized group in that users 'my groups'. 

As of February 1st 2021, This is an image of ballchasing.com's 'my replays' location on ballchasing.com's website. 
![!my_replays](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/my_replays.png)

Similariy, this is an image of 'my replay groups' tab general location on ballchasing.com.
![!my replay groups](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/my_replay_groups.png)

replay_upload.py will output a json file that contains the name of the replay uploaded and the link to the replay location on ballchasing.com. This information is saved for later use in the replay_grouper.py script. The upload_data.json file structure can be seen below. 

![!upload_data](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/upload_data.png)

replay_grouper.py is a script that will move all replays into the into one group on ballchasing. Replay grouper will utilize the upload_data.json file found in the output folder in order to move replays from the bot host's ballchasing.com account "general replay' group to a user created group. The name of the group which were are moving the replays just uploaded must be made ballchasing.com first and is specified inside of the replay_grouper.py.

![!replay_grouper_results](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/replay_grouper_results.png)

# make_playercards.py - Replay Data Stat Generation 

Using my Discord Bot, I was able to neatly upload replays onto Ballchasing.com and fortunately Ballchasing.com has an easy option to export all game statistics to CSV format. I simply download export and will utilize make_playercards.py to make a player overalls based on multiple statistics return from replay data. A sample of the CSV file structure from Ballchasing.com is shown below. 

![!upload_data](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/upload_data.png)

Next, this script will take in that CSV data and output a CSV file that contains the names of all participants in a tournament (in this example, this is Winter 2021 Player Data). The resulting Dataframe will displays each players Win Percentage, Overall Rating, Offensive Rating, Defensive Rating, Aggression Rating, and Speed Rating. Each of these statistics were generated based original game statistics tweaked based on game knowledge accuired from playing this game since release (Over 3000 hours in game experience). 

![!player_statistics](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/export_data_df.png)

# Added Features: Playercard Support from Replay Data (Fall 2020)

#### Playercards 
![!playercard_img](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!playercard_img.png)

![!playercard_rank](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!playercard_rank.png)

![!playercard_name](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!playercard_name.png)

![!my_playercard]






