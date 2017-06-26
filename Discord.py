#!/usr/bin/python3

""" This bot is written for romanian users, but the comments are in english. 
    Also, this is my first python project, so the code isn't "ideal" """

import random
import math
import os
import discord
import asyncio
import urllib.request
import urllib.parse
import re
from discord.ext import commands
import collections

version = 0.9

if not discord.opus.is_loaded():
    try:
        import opuslib
        discord.opus.load_opus('opus')
    except:
        print('OpusLib nu a fost gasit. Bot-ul nu va putea sa intre in nici un voice channel. ')


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

client = commands.Bot(command_prefix=".")


@client.event
async def on_ready():
    print("RoBot in actiune...")

class GetInfo:
    def __init__(self, user_voice_ch_id, user_server_id, message):
        self.user_voice_ch_id = message.author.voice_channel.id
        self.user_server_id = message.author.server.id
        self.message_content = message.content
        self.message = message
        self.channel = client.get_channel(self.user_voice_ch_id)


class YoutubePlayer(GetInfo):
    voice_matrix = [[]for i in range(2)]
    player_matrix = [[]for i in range(2)]
    def __init__(self, youtube_url, user_voice_ch_id, user_server_id, message):
        self.youtube_url = youtube_url
        super().__init__(user_voice_ch_id, user_server_id, message)

    # Create a voice object that is unique per server. Isn't that cool? 
    async def create_voice_object(self, add_in_queue):
        try:
            self.voice = await client.join_voice_channel(self.channel)
            pass_server = YoutubePlayer.voice_matrix[0].append(self.user_server_id)
            pass_voice = YoutubePlayer.voice_matrix[1].append(self.voice)
            return self.voice
        except: 
            if self.youtube_url != None and add_in_queue == True:
                add_to_playlist = Playlist.add_to_playlist(self.user_server_id, self.youtube_url)
                await client.send_message(self.message.channel, 'Sigur, adaug in playlist ' + self.youtube_url)

            return False

    def remove_voice_object(self):
        index_to_remove = self.find_list_duplicates(YoutubePlayer.voice_matrix[0], False)
        remove_server = YoutubePlayer.voice_matrix[0].pop(index_to_remove)
        remove_voice = YoutubePlayer.voice_matrix[1].pop(index_to_remove)

    async def create_youtube_player(self, voice, youtube_url, message):
        try:
            player = await voice.create_ytdl_player(youtube_url)
            player.start()
        except:
            if voice != False:
                await client.send_message(self.message.channel, 'URL-ul YouTube este invalid. Ori exista o problema cu drepturile de autor, ori link-ul este gresit.')
                await exit_voice_channel(1, voice)
            return False

        song_time = int(player.duration)
        pass_server = YoutubePlayer.player_matrix[0].append(self.user_server_id)
        pass_player_object = YoutubePlayer.player_matrix[1].append(player)
        return song_time

    """
    Resource management for non-rack mounted servers with
    compute power level less than 9000
    """
    def destroy_youtube_player(self):
        remove_current_song = Playlist.queue_dict.get(self.user_server_id)
        if remove_current_song != None:
            remove_current_song.pop(0)
            #TODO Destroy youtube player object
            if len(remove_current_song) == 0:
                remove_server_key = Playlist.queue_dict.pop(self.user_server_id)
        
    
    #Check all the items in a list and return the index of the first duplicate
    
    def find_list_duplicates(self, lst, return_all):
        count = collections.Counter(lst)
        duplicates = [i for i in count]
        duplicate_index = {}
        for items in duplicates:
            duplicate_index[items] = [i for i, j in enumerate(lst)]
            songs_in_server = duplicate_index[self.user_server_id][0:]
            print(songs_in_server)
            remove_current_index = duplicate_index[self.user_server_id].pop(0)
            if return_all:
                return songs_in_server
            else:
                return songs_in_server[0]

    async def output_trakcs(self):
        await client.send_message(self.message.channel, 'Melodii in playlist: ')
        server_tracks = Playlist.queue_dict.get(self.user_server_id)
        if server_tracks != None:
            await client.send_message(self.message.channel, 'Total melodii: {}, URL: {}'.format(len(server_tracks), server_tracks))
            
        else:
            await client.send_message(self.message.channel, 'Total melodii: 0')


    #Finally, play some music, grab a beer and relax.
    async def play_youtube_url(self):
        if self.youtube_url.startswith('https://www.youtube.com/watch?v=') or self.youtube_url.startswith('http://www.youtube.com/watch?v=') or self.youtube_url.startswith('https://youtu.be/'):
            voice = await self.create_voice_object(True)
            player = await self.create_youtube_player(voice, self.youtube_url, self.message)
            if player != False:
                await client.send_message(self.message.channel, 'Sigur, adaug in playlist ' + self.youtube_url)
                song_time = player
                await exit_voice_channel(song_time, voice)
                self.remove_voice_object()
                self.destroy_youtube_player()

        else:
            await client.send_message(self.message.channel, 'URL-ul nu este valid. Pentru a cauta, foloseste comanda cu argumentul "-s" (.muzica -s)')
            return 

              #If a song is in queue, play it.
            
        while True:
            check_next_song = Playlist.queue_dict.get(self.user_server_id, False)
            if check_next_song != False:
                voice = await self.create_voice_object(False)
                # For whatever reason, create_youtube_player is not working here.
                # For now, I will repeat that code, untill I can figure this out.
                try:
                    player = await voice.create_ytdl_player(check_next_song[0])
                    player.start()
                except:
                    if voice != False:
                        await client.send_message(self.message.channel, 'URL-ul YouTube este invalid. Ori exista o problema cu drepturile de autor, ori link-ul este gresit.')
                        await exit_voice_channel(1, voice)
                    break
                song_time = int(player.duration)
                pass_server = YoutubePlayer.player_matrix[0].append(self.user_server_id)
                pass_player_object = YoutubePlayer.player_matrix[1].append(player)
                await exit_voice_channel(song_time, voice)
                self.remove_voice_object()
                self.destroy_youtube_player()
            else:
                return


class YoutubeSearch:
    def __init__(self, user_keyword, message):
        self.user_keyword = user_keyword
        self.message = message
    
#Method for searching a YouTube url based on keywords
    async def search_youtube_url(self):
        try:
            # Modified code form Grant Curell, https://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video. License: GPLv3.
            query_string = urllib.parse.urlencode({"search_query" : self.user_keyword})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            return ("http://www.youtube.com/watch?v=" + search_results[0])
        # End of copyright
        except:
            await client.send_message(self.message.channel, 'Nu am gasit nici un rezultat cu numele [" ' + self.user_keyword + ' "]')
            return

class Playlist(YoutubePlayer):
    queue_dict = {}

    # The simplest playlist method that you have ever seen. Trust me.
    @classmethod
    def add_to_playlist(cls, server, song):
        if cls.queue_dict.get(server) == None:
            key_to_dict_list = cls.queue_dict[server] = [song]
        else:
            queue_dict_list = cls.queue_dict[server].append(song)
        print('Dict {}'.format(cls.queue_dict))
        

class ForceExit(YoutubePlayer):
    def __init__(self, youtube_url, user_voice_ch_id, user_server_id, message):
        super().__init__(youtube_url, user_voice_ch_id, user_server_id, message)

    async def voice_force_exit(self):
        # I'm sad. You didn't liked my personality, so I'm leaving
        while True:
            check_conn = await self.create_voice_object(False)
            if check_conn == False:
                get_server_index = self.find_list_duplicates(self.voice_matrix[0], False)
                get_voice_object = YoutubePlayer.voice_matrix[1][get_server_index]
                await exit_voice_channel(1, get_voice_object)
                server_queue = Playlist.queue_dict.get(self.user_server_id)
                if server_queue != None:
                    remove_server_key = Playlist.queue_dict.pop(self.user_server_id)
                self.remove_voice_object()
                self.destroy_youtube_player()
                break
            else:
                await client.send_message(self.message.channel, 'Nu sunt conectat la un voice channel. ')
                await exit_voice_channel(1, check_conn)
                break
        
            
        
# Function for playing any aduio file
async def play_audio_file(audio_file, get_voice_channel_id, audio_duration):
    try:
        voice = await client.join_voice_channel(get_voice_channel_id)
        player = voice.create_ffmpeg_player(audio_file)
        player.start()
        await exit_voice_channel(audio_duration, voice)
    except:
        return False


async def exit_voice_channel(exit_time, voice_connection):
    await asyncio.sleep(exit_time)
    await voice_connection.disconnect()


#Function for generating a random number  
def random_int_gen(input_number1, input_number2):
    output_rand = random.randrange(input_number1, input_number2)
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

      
# When the user types a command...

@client.event
async def on_message(message):

    try:
        info = GetInfo(message.author.voice_channel.id, message.author.server.id, message)
    except AttributeError:
        return

    if message.content.startswith('.test'):
        test = await client.send_message(message.channel, "Da, functionez!")
        
    elif message.content.startswith('.debug'):  
        print(message.channel)

    elif message.content.startswith('.amuzant'):
        start_playing_file = await play_audio_file('amuzant.mp3', info.channel, 5)
        if start_playing_file == False:
            await client.send_message(message.channel, 'Sunt un simplu bot, nu pot sa intru in voice channel inca o data.')

    elif message.content.startswith('.taie'):
        start_playing_file = await play_audio_file('taie.mp3', info.channel, 3)
        if start_playing_file == False:
            await client.send_message(message.channel, 'Sunt un simplu bot, nu pot sa intru in voice channel inca o data.')

    elif message.content.startswith('.muzica'):
        output_url = info.message_content.replace('.muzica', '').strip()

        if output_url.startswith('-s'):
            final_user_keyword = output_url.replace('-s', '').strip()

            await client.send_message(message.channel, 'Caut pe YouTube [" ' + final_user_keyword + ' "]')

            returned_youtube_url = await YoutubeSearch(final_user_keyword, message).search_youtube_url()
            start_youtube_player = await YoutubePlayer(returned_youtube_url, info.user_voice_ch_id, info.user_server_id, message).play_youtube_url()   
        else:
            start_youtube_player = await YoutubePlayer(output_url, info.user_voice_ch_id, info.user_server_id, message).play_youtube_url() 

    elif message.content.startswith('.versiune'):
        global version
        await client.send_message(message.channel, 'RoBot v. {} Discord.py API v. {}'.format(version, discord.__version__))

    elif message.content.startswith('.jet'):
        await ForceExit(None, info.user_voice_ch_id, info.user_server_id, message).voice_force_exit()
        pass
    elif message.content.startswith('.playlist'):
        await YoutubePlayer(None, info.user_voice_ch_id, info.user_server_id, message).output_trakcs()
           
        
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
        await client.send_message(message.channel, 'Comenzi: \n .test - Verifica daca functionez. \n .amuzant - Bot-ul intra in voice channel-ul in care se afla si utilizatorul care a invocat bot-ul \n si reda un material audio(recomandabil folosita in cazul in care un memnru din server face o gluma proasta) \n .gluma - Nu mai este nevoie de explicatie \n .muzi_youtube / cuvant cheie - bot-ul insta in voice channel-ul in care se afla \n si utilizatorul care l-a invocat si reda audio-u mentionat.')
               
# Run the bot. Put your own discord Token code in 'quotes'.

client.run('YOUR_TOKEN_HERE')
