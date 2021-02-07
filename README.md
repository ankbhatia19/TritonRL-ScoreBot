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
The tournaments we host for our gaming community typically span five weeks, and with an average of 10 teams playing 4 series per week. Each game will have one replay file associated with it, and this .replay file will contain game_information such as ball position, player positioning, total shots per player, total saves per player and more. Each series of games played will have a minimum of three .replay files that need to be uploaded for tournament result verification purposes. This means that we needed a way to conviently store .replay files uploaded on our Discord Server, thus the creation of this bot. 

### Setup 
- Requirements - PIP stuff #TODO
- Setup - Tokens #TODO
- Execute - Run Bot.py #TODO

#### Upon Startup
In order to get started with this Bot, first follow all the instruction in the previous 'Setup' field. Then, simply run Bot.py. When bot.py is ran, this will be the startup message send to the designated bot channel. Below is an image of what this startup message would look like while in the server.

![OnStartup](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/on_startup.png)

#### Replay Managment 
In order to submit replays using the bot, users must use the "!rl_report" command in order to start the submission process. This will prompt the user to type out the results of the series they are trying to report. Results must be reported using a specified format. The image below is an example of a tournament participant reporting their series replays. 
![!rl_report](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!rl_report.png)
After the participant uploads their replays, they will then be asked to confirm their submission.
![!confirm](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!confirm.png)

That is all the tournament participants must do to submit their series replays. The images below are for the person hosting this bot service. 

The individual running the bot will be running it from their local system, and all uploaded replays will be named according to user input and saved in a "replays" folder. If this "replays" folder does not already exist, one will be created locally. 
![!replay_managment](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!replay_managment.png)

After all replays for any given match day are uploaded, they will appear in the replays folder as I previously said. The bot host can the replay_upload.py file. When this python script is ran, it will upload each replay to the ballchasing.com replay account. Ballchasing.com is an online service which allows users to upload their Rocket League replay files and parse game information for all players in that particular game. By uploading these files to this site, I did not need to write my own .replay file parser. 

![!replay_upload](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!replay_managment.png)

When the replay_upload.py script finishes runinng, the script will save a file to the output folder. The output folder is a folder that contains any important data generated that may be needed at a later time. First, the script checks to see if an output folder exists, and if it doesnt, it will make a local folder. The replays uploaded can now be found on the hosts ballchasing.com account. It would appear under their profile as such. There is one last step in managing these replay files, they ust be grouped into one final group. 

![!upload_data](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!upload_data.png)

replay_upload.py will output a json file that contains the name of the replay uploaded and the link to the replay location on ballchasing.com. This information is saved for later use in the replay_grouper.py script. The upload_data.json file structure can be seen below. 

![!upload_data](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!upload_data.png)

replay_grouper.py is a script that will move all replays into the into one group on ballchasing. Replay grouper will utilize the upload_data.json file found in the output folder in order to move replays from the bot host's ballchasing.com account "general replay' group to a user created group. The name of the group which were are moving the replays just uploaded must be made ballchasing.com first and is specified inside of the replay_grouper.py.

![!replay_grouper_results](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!replay_grouper_results.png)


## Added Features: Playercard Support from Replay Data (Fall 2020)

#### Playercards 

![!playercard_img](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!playercard_img.png)
![!playercard_rank](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!playercard_rank.png)
![!playercard_name](https://github.com/davidMthierry/TritonRL-ScoreBot/blob/main/readme_imgs/!playercard_name.png)
![!my_playercard]






