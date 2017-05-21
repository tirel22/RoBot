#!/usr/bin/python3

# This bot is written for roumanian users, but the documentation is in english. Also, this is my first python project, so the code isn't "ideal"

import random
import math
import os
import discord
import asyncio

version = 0.3

#Varialbes for the ".gluma" command

Said1 = False
Said2 = False
Said3 = False
Said4 = False
Said5 = False
Said6 = False 
Said7 = False
Said8 = False
Said9 = False

#Create the client

client = discord.Client()

@client.event
async def on_ready():
    isStarted = True
    if isStarted == True:
        print("RoBot in actiune...")
    else:
        print("Eroare...")
       
  
# When the user types a command...

@client.event
async def on_message(message):

    if message.content.startswith('.test'):
        test = await client.send_message(message.channel, "Da, functionez!")
        
    elif message.content.startswith('.debug'):
        test1 = RandomIntGen(0 ,2)
        test2 = await client.send_message(message.server, "Vlaoare: " + str(test1))
        print(str(test1))
        

    elif message.content.startswith('.amuzant'):
        await client.send_message(message.channel, 'Esti asa de amuzant, am uitat sa rad...')
        await PlayAudioFile('amuzant.mp3')

    elif message.content.startswith('.taie'):
        await PlayAudioFile('taie.mp3')

    elif message.content.startswith('.muzica'):
        
        await PlayYoutubeURL(inputURL)
        

    elif message.content.startswith('.versiune'):
        global version
        await client.send_message(message.channel, 'RoBot v. ' + str(version))
        
        
    elif message.content.startswith('.gluma'):
        randomJoke = RandomIntGen(0, 9)
        ResetJokes()
        global Said1
        global Said2
        global Said3
        global Said4
        global Said5
        global Said6
        global Said7
        global Said8
        global Said9

        # If the same random number was generated, generate another in order for the bot to respond

        while randomJoke == 1 and Said1 == True or randomJoke == 2 and Said2 == True or randomJoke == 3 and Said3 == True or randomJoke == 4 and Said4 == True or randomJoke == 5 and Said5 == True or randomJoke == 6 and Said6 == True or randomJoke ==7 and Said7 == True or randomJoke == 8 and Said8 == True:       
            RandomIntGen(1, 9)
        # When the user types more than one ".gluma" command, do not repeat the joke.
        if randomJoke == 1 and Said1 == False :
            #The first joke
             await client.send_message(message.channel, 'Cum face masina de politie a dinozaurilor? NINO NINO DANONINO, Dar cea de pompieri? NINO NINO FireDINO')
             Said1 = True
                        
        elif randomJoke ==2 and Said2 == False :
            
            await client.send_message(message.channel, 'De ce nu alearga melcul ?!?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Pentru ca ii falfaie ochii')
            Said2 = True
            
            
        elif randomJoke ==3 and Said3 == False :
            await client.send_message(message.channel, 'De ce nu se uita melcul in priza?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Pentru ca se curenteaza')
            Said3 = True
            

        elif randomJoke ==4 and Said4 == False :
            await client.send_message(message.channel, 'Tata, pot face baie daca am diaree?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Da, daca ai destula')
            Said4 = True
          

        elif randomJoke ==5 and Said5 == False :
            await client.send_message(message.channel, 'Era seara iar Alina trebuia sa faca baie, dar ii era lene... ')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Mama: -Alina, de ce nu vrei sa faci baie?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Alina: Pentru ca e uda')
            Said5 = True
            
        
        elif randomJoke ==6 and Said6 == False:
            await client.send_message(message.channel, 'Alexandra: -Mama, tata s-a imbatat')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Mama: -De unde stii?')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Alexandra: -Barbiereste oglinda din baie')
            Said6 = True
            

        elif randomJoke ==7 and Said7 == False :
            await client.send_message(message.channel, '-Alex, stii bancul cu ieputele din baie?')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Alex: -Nu')
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'Nici eu, era usa inchisa...')
            Said7 = True
           

        elif randomJoke ==8 and Said8 == False:
            await client.send_message(message.channel, 'Stii ce face ursul dupa ce se trezeste din hibernat?')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Fute o laba')
            Said8 = True

    elif message.content.startswith('.comenzi'):
        await client.send_message(message.channel, 'Comenzi: \n .test - Verifica daca functionez. \n .amuzant - Bot-ul intra in voice channel-ul in care se afla si utilizatorul care a invocat bot-ul \n si reda un material audio(recomandabil folosita in cazul in care un memnru din server face o gluma proasta) \n .gluma - Nu mai este nevoie de explicatie \n .muzica url_youtube - nu functioneaza momentan')
            
            

#Function for playing a specific YouTube URL

async def PlayYoutubeURL(youtubeURL):
    channel = client.get_channel('267686533593694208')
    voice = await client.join_voice_channel(channel)
    player = await voice.create_ytdl_player(youtubeURL)
    player.start()

async def PlayAudioFile(audiofile):
    channel = client.get_channel('267686533593694208')
    voice = await client.join_voice_channel(channel)
    player = voice.create_ffmpeg_player(audiofile)
    player.start()
    isDone = player.is_done()
    if isDone :
        player.stop()
        voice.stop()
    




#Function in ordedr for the bot to join a voice channel

async def EnterVoiceChannel():
    channel = client.get_channel('267686533593694208')
    await client.join_voice_channel(channel)

#Function for generating a random number  
def RandomIntGen(inputNumber1, inputNumber2):
    inputNumber = random.randrange(inputNumber1, inputNumber2)
    outputRand = inputNumber
    return outputRand

async def GetInfo():
    destChannel = client.get_channel(id)
    destServer = client.get_server(id)
    print (str(destChannel))
    print (str(destServer))

            
        
def ResetJokes():
    #Acces the variables declared uptop.
    global Said1
    global Said2
    global Said3
    global Said4
    global Said5
    global Said6
    global Said7
    global Said8
    global Said9

    # If all the jokes were said...

    if Said1 == True and Said2 == True and Said3 == True and Said4 == True and Said5 == True and Said6 == True and Said7 == True and Said8 == True :
        # Than reset the booleans to False, in order to say the same jokes again... I know, this bot is all a joke...
        Said1 = False
        Said2 = False
        Said3 = False
        Said4 = False
        Said5 = False
        Said6 = False
        Said7 = False
        Said8 = False
        Said9 = False
        
        
        

        
# Run the bot. Put your own discord Token code in 'quotes'.

client.run('MzE0NDY1OTU2NzExNjI4ODAx.C_8o2Q.gWZxOd_zlaTHiDeIIwssfazSCaM')


