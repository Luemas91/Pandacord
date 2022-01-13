from asyncio.windows_events import NULL
import discord
import os
from dotenv import load_dotenv
import random
from discord import HTTPException
import json
from csvfunctions import custom_func_get,custom_func_update

load_dotenv()
token = os.getenv('Discord_token')
close_mutuals = os.getenv('close_moots')
daddycord = os.getenv('daddycord')
muse = os.getenv('muse')
shitshow=os.getenv('shitshow')


leadvar = '>'
EMOJI_NAMES = ["pin", "📌"]

panda = discord.Client()

@panda.event
async def on_ready():
    for guild in panda.guilds:
        if guild.name == daddycord: # or guild.name == close_mutuals:
            break

        print(
            f'{panda.user} has entered the swimming pool!:\n'
            f'{guild.name}(id: {guild.id})\n'
            )

# Panda Gifer
@panda.event
async def on_message(message):
    if message.author == panda.user:
        return
    
    pangif = [
        'https://c.tenor.com/2XHTM3NHQfYAAAAC/panda-jjk.gif',
        'Panda is not a Panda',
        'https://c.tenor.com/gmvdv-e1EhcAAAAC/weliton-amogos.gif'
        'https://c.tenor.com/ZiNqSxHmdIYAAAAC/jjk-jujutsu-kaisen.gif',
        'https://c.tenor.com/YDionZwapW4AAAAC/jjk-lazy.gif',
        'https://media3.giphy.com/media/N6funLtVsHW0g/giphy.gif?cid=ecf05e47oy0ihuz5qzbrdflupwb28sk98dfnwc2j8hrc5nou&rid=giphy.gif&ct=g',
        'https://media3.giphy.com/media/EPcvhM28ER9XW/giphy.gif?cid=ecf05e47oy0ihuz5qzbrdflupwb28sk98dfnwc2j8hrc5nou&rid=giphy.gif&ct=g',
        'https://media.tenor.co/videos/6c5f4ceb9199e579fe690b4df0050747/mp4',
    ]
    
    # trims message of punctuation, fixes cases
    message.content = message.content.lower()
    #message.content = message.content.replace('.', "")
    message.content = message.content.replace("'", "")
    # >panda
    if message.content.startswith(leadvar+'panda'):
        response = random.choice(pangif)
        await message.channel.send(response)

    # Functional Responses
    # imvegan, checks if message contains i'm vegan, and returns one of the potential responses.
    if message.content.find('im vegan') >= 0:
        vegan = [
            'But where do you get your protein?',
            'Oh me too! I only eat meat on Thursdays!',
            'Oh I could never be vegan, where would I get my B12?',
            'So that means you eat fish right?'
        ]
        t = random.randrange(0,len(vegan))
        await message.channel.send(vegan[t])
    
    # Bonkboard iterates through messages and returns a semisorted list of users and their bonks. Has a selection of bonk emotes (maybe should just check for the text bonk)
    # List needs to be sorted largest to smallest, and needs brackets removed
    # If not from closemutuals, return null
    # Also needs to have separate handling for args like alltime (csv), days, etc.
    if message.content.startswith(leadvar+'bonkboard'):
        bonk = ['<:bonk:896886830622965820>','<:BONK:718289967155118130>','<:bonk:930818372831174656>']
        bonkboard = {}
        closemoots = panda.get_guild(881855141077213185) # needs to be updated to control for close mutuals
        messagechannel = message.channel
        for channels in closemoots.channels:
            try:
                messages = await channels.history(limit=100).flatten()
                for message in messages:
                    for react in message.reactions:
                        if str(react) in bonk:
                            try: 
                                temp = bonkboard[message.author.name] + react.count
                                bonkboard.update({message.author.name: temp})
                            except:
                                bonkboard[message.author.name] = react.count
                        else:
                            continue
            except AttributeError:
                continue
            except:
                continue
        pbonkboard = dict(sorted(bonkboard.items(),key=lambda item: item[1],reverse=True))
        prettybonkboard =json.dumps(pbonkboard, indent=4,ensure_ascii=False)
        await messagechannel.send(prettybonkboard)

    # Custom Command Adder
    if message.content.startswith(leadvar + 'addcommand'):
        arg1, arg2, arg3 = message.content.split('|')
        arg2 = arg2.strip()
        arg3 = arg3.strip()
        guild = message.guild
        if arg2 and arg3 != NULL:
            if custom_func_update(guild,arg2,arg3) == True:
                await message.channel.send('Done! Function Successfully Updated')
            else:
                await message.channel.send('Something broke <@253019708360491010>')
        else:
            await message.channel.send('Please use the syntax: >addcomand | arg1 | arg2')
    
    # Custom Command Reader
    if message.content.startswith(leadvar):
        command = message.content.strip(leadvar)
        guild = message.guild
        custom_function_data = custom_func_get(guild)
        for key in custom_function_data.keys():
            if command == key:
                responseoptions = custom_function_data[key]
                j = random.randrange(0,len(responseoptions))
                response = responseoptions[j].strip("'")
                await message.channel.send(response)

    




@panda.event       
async def on_raw_reaction_add(reaction):
    # print(reaction)
    message_id = reaction.message_id
    # print(type(message_id))
    channel_id = reaction.channel_id
    channel = panda.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    
    if message.pinned:
                return
    try:
        reaction = next(x for x in message.reactions if (isinstance(x.emoji, str) and str(x.emoji) in EMOJI_NAMES) or (not isinstance(x.emoji, str)and x.emoji.name in EMOJI_NAMES))
        if reaction.count >= 5:
            try:
                await message.pin()
            except HTTPException:  # This most likely means we reached max pins
                pins = await channel.pins()
                oldest_pin = pins.pop()
                await oldest_pin.unpin()
                await message.pin()
    except Exception:
        pass

panda.run(token)