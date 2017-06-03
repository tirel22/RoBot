#!/usr/bin/python3

# This bot is written for roumanian users, but the documentation is in english. Also, this is my first python project, so the code isn't "ideal"

import random
import math
import os
import discord
import asyncio
import urllib.request
import urllib.parse
import re

version = 0.8

if not discord.opus.is_loaded():
    try:
        import opuslib
        discord.opus.load_opus('opus')
    except:
        print('OpusLib nu a fost gasit.')


#Varialbes for the ".gluma" command

said_1 = False
said_2 = False
said_3 = False
said_4 = False
said_5 = False
said_6 = False 
said_7 = False
said_8 = False
said_9 = False

#Create the client

client = discord.Client()


@client.event
async def on_ready():
    is_started = True
    if is_started:
        print("RoBot in actiune...")
    else:
        print("Eroare...")
       
  
# When the user types a command...

@client.event
async def on_message(message):

    if message.content.startswith('.test'):
        test = await client.send_message(message.channel, "Da, functionez!")
        
    elif message.content.startswith('.debug'):
        member = message.author.voice_channel      

    elif message.content.startswith('.amuzant'):
        user_voice_channel = message.author.voice_channel.id
        await client.send_message(message.channel, 'Esti asa de amuzant, am uitat sa rad...')
        start_playing_file = await play_audio_file('amuzant.mp3', user_voice_channel, 5)
        if start_playing_file == False:
            await client.send_message(message.channel, 'Sunt un simplu bot, nu pot sa intru in voice channel inca o data.')

    elif message.content.startswith('.taie'):
        user_voice_channel = message.author.voice_channel.id
        start_playing_file = await play_audio_file('taie.mp3', user_voice_channel, 3)
        if start_playing_file == False:
            await client.send_message(message.channel, 'Sunt un simplu bot, nu pot sa intru in voice channel inca o data.')

    elif message.content.startswith('.muzica'):
        user_url = message.content
        procces_url = user_url.replace('.muzica', '')
        output_url = procces_url.strip()

        if output_url.startswith('-s'):
            prepare_user_keyword = output_url.replace('-s', '')
            final_user_keyword = prepare_user_keyword.strip()
            await client.send_message(message.channel, 'Caut pe YouTube [" ' + final_user_keyword + ' "]')
            returned_youtube_url = search_youtube_url(final_user_keyword)
            try:
                user_voice_channel = message.author.voice_channel.id
                user_server = message.author.server.id
                set_player = YoutubePlayer(returned_youtube_url, user_voice_channel, user_server)
                start_youtube_player = await set_player.play_youtube_url()
            except:
                await client.send_message(message.channel, 'Sunt confuz... In ce voice channel ar trebui sa intru? Ar fi minunat sa imi arati, ce zici daca te conectezi la unul.')
                return

            if returned_youtube_url == 'URL_NOT_FOUND':
                await client.send_message(message.channel, 'Nu am gasit nici un rezultat cu numele [" ' + final_user_keyword + ' "]')
                return
                
            if start_youtube_player == 'YOUTUBE_URL_SUCCES':
                await client.send_message(message.channel, 'Sigur, adaug in playlist ' + returned_youtube_url)
        else:
            try:
                user_voice_channel = message.author.voice_channel.id
                user_server = message.author.server.id
                set_player = YoutubePlayer(output_url, user_voice_channel, user_server)
                start_youtube_player = await set_player.play_youtube_url()
            except:
                 await client.send_message(message.channel, 'Sunt confuz... In ce voice channel ar trebui sa intru? Ar fi minunat sa imi arati, ce zici daca te conectezi la unul.')
                 return

            if start_youtube_player == 'YOUTUBE_URL_SUCCES':
                await client.send_message(message.channel, 'Sigur, adaug in playlist ' + output_url)
        
        if start_youtube_player == 'URL_ERROR':
            await client.send_message(message.channel, 'URL-ul nu este valid. Pentru a cauta, foloseste comanda cu argumentul "-s" (.muzica -s)')

        elif start_youtube_player == 'PLAYER_ERROR':
            await client.send_message(message.channel, 'Exceptie. Probabil bot-ul se mai afla intr-un voice channel in server, sau URL-ul este protejat de drepturi de autor.')


    elif message.content.startswith('.versiune'):
        global version
        await client.send_message(message.channel, 'RoBot v. ' + str(version))
        
        
    elif message.content.startswith('.gluma'):
        random_joke = random_int_gen(1, 9)
        reset_jokes()
        global said_1
        global said_2
        global said_3
        global said_4
        global said_5                
        global said_6
        global said_7
        global said_8
        global said_9

        # If the same random number was generated, generate another in order for the bot to respond

        while random_joke == 1 and said_1 == True or random_joke == 2 and said_2 == True or random_joke == 3 and said_3 == True or random_joke == 4 and said_4 == True or random_joke == 5 and said_5 == True or random_joke == 6 and said_6 == True or random_joke ==7 and said_7 == True or random_joke == 8 and said_8 == True:       
            random_joke = random_int_gen(1, 9)
        # When the user types more than one ".gluma" command, do not repeat the joke.
        if random_joke == 1 and said_1 == False :
            #The first joke
             await client.send_message(message.channel, 'Cum face masina de politie a dinozaurilor? NINO NINO DANONINO, Dar cea de pompieri? NINO NINO FireDINO')
             said_1 = True
                        
        elif random_joke == 2 and said_2 == False :
            
            await client.send_message(message.channel, 'De ce nu alearga melcul ?!?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Pentru ca ii falfaie ochii')
            said_2 = True
            
            
        elif random_joke == 3 and said_3 == False :
            await client.send_message(message.channel, 'De ce nu se uita melcul in priza?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Pentru ca se curenteaza')
            said_3 = True
            

        elif random_joke == 4 and said_4 == False :
            await client.send_message(message.channel, 'Tata, pot face baie daca am diaree?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Da, daca ai destula')
            said_4 = True
          

        elif random_joke == 5 and said_5 == False :
            await client.send_message(message.channel, 'Era seara iar Alina trebuia sa faca baie, dar ii era lene... ')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Mama: -Alina, de ce nu vrei sa faci baie?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Alina: Pentru ca e uda')
            said_5 = True
            
        
        elif random_joke == 6 and said_6 == False:
            await client.send_message(message.channel, 'Alexandra: -Mama, tata s-a imbatat')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Mama: -De unde stii?')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Alexandra: -Barbiereste oglinda din baie')
            said_6 = True
            

        elif random_joke == 7 and said_7 == False :
            await client.send_message(message.channel, '-Alex, stii bancul cu ieputele din baie?')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Alex: -Nu')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Nici eu, era usa inchisa...')
            said_7 = True
           

        elif random_joke == 8 and said_8 == False:
            await client.send_message(message.channel, 'Stii ce face ursul dupa ce se trezeste din hibernat?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Fute o laba')
            said_8 = True

    elif message.content.startswith('.comenzi'):
        await client.send_message(message.channel, 'Comenzi: \n .test - Verifica daca functionez. \n .amuzant - Bot-ul intra in voice channel-ul in care se afla si utilizatorul care a invocat bot-ul \n si reda un material audio(recomandabil folosita in cazul in care un memnru din server face o gluma proasta) \n .gluma - Nu mai este nevoie de explicatie \n .muzica url_youtube / cuvant cheie - bot-ul insta in voice channel-ul in care se afla \n si utilizatorul care l-a invocat si reda audio-u mentionat.')
            
class YoutubePlayer:
    def __init__(self, youtube_url, voice_channel_id, server_id):
        self.youtube_url = youtube_url
        self.voice_channel_id = voice_channel_id
        self.server_id = server_id

    #Function for playing a specific YouTube URL
    async def play_youtube_url(self):
        if self.youtube_url.startswith('https://www.youtube.com/watch?v=') or self.youtube_url.startswith('http://www.youtube.com/watch?v=') or self.youtube_url.startswith('https://youtu.be/'):
            channel = client.get_channel(self.voice_channel_id)
            try:
                voice = await client.join_voice_channel(channel)
                player = await voice.create_ytdl_player(self.youtube_url)
                player.start()
                add_to_playlist = youtube_playlist(self.youtube_url, True, -1)
                song_time = int(player.duration)
                await exit_voice_channel(song_time, voice, 0, 0)    
                return 'YOUTUBE_URL_SUCCES'
            except:
                return 'PLAYER_ERROR'
        else:
            return 'URL_ERROR'

#Function for searching a YouTube url based on keywords
def search_youtube_url(user_keyword):
    try:
        # Modified code form Grant Curell, https://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video. License: GPLv3.
        query_string = urllib.parse.urlencode({"search_query" : user_keyword})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        return ("http://www.youtube.com/watch?v=" + search_results[0])
    # End of copyright
    except:
        return 'URL_NOT_FOUND'

#Function for adding songs to a playlist
def youtube_playlist(song_url, add_to_playlist, counter):
    if add_to_playlist:
        counter +=1
        song_list_url = []
        song_list_url.append(song_url)
        print(str(song_list_url[counter:]))
        print(counter)
        return 'YOUTUBE_URL_SUCCES'
    else:
        return str(song_list_url[counter:])
        
# Function for playing any aduio file
async def play_audio_file(audio_file, voice_channel_id, audio_duration):
    try:
        channel = client.get_channel(voice_channel_id)
        voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player(audio_file)
        player.start()
        await exit_voice_channel(audio_duration, voice, 0, 0)
    except:
        return False

    
    
    
#Function in ordedr for the bot to join a voice channel
async def enter_voice_channel():
    channel = client.get_channel('314466222811119617')
    await client.join_voice_channel(channel)

async def exit_voice_channel(exit_time, voice_connection, id_of_voice_channel, id_of_server):
    await asyncio.sleep(exit_time)
    await voice_connection.disconnect()


#Function for generating a random number  
def random_int_gen(input_number1, input_number2):
    input_number = random.randrange(input_number1, input_number2)
    output_rand = input_number
    return output_rand
            

def reset_jokes():
    #Acces the variables declared uptop.
    global said_1
    global said_2
    global said_3
    global said_4
    global said_5
    global said_6
    global said_7
    global said_8
    global said_9

    # If all the jokes were said...

    if said_1 == True and said_2 == True and said_3 == True and said_4 == True and said_5 == True and said_6 == True and said_7 == True and said_8 == True :
        # Than reset the booleans to False, in order to say the same jokes again... I know, this bot is all a joke...
        said_1 = False
        said_2 = False
        said_3 = False
        said_4 = False
        said_5 = False
        said_6 = False
        said_7 = False
        said_8 = False
        said_9 = False
        
        
        

        
# Run the bot. Put your own discord Token code in 'quotes'.

client.run('YOUR_TOKEN_HERE')