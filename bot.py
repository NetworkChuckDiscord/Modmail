# bot.py
import os
#import random
import yaml

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

TicketNumber = 0
tickets = {}

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='DM for complaints'))    
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

@client.event
async def on_message(message):
    print(message)
# verify that the bot doesn't respond to itself
    if message.author == client.user:
        return
    # debug data
    print(message.channel.type)
    print(type(message.channel.type))
    # verify that message was sent via DM/PM
    if str(message.channel.type) == "private":
           guild = discord.utils.get(client.guilds)
           print(guild)
           response = 'How can I Help you'
           global tickets
           global TicketNumber
           global msgnumber
          # Check if user has submitted complaints in the past
           print(tickets.keys())
           if message.author.id not in tickets.keys():
               msgnumber = 0
               TicketNumber = int(TicketNumber) + 1
               TicketName = f'ticket-' + str(TicketNumber)
               # initilize ticket
               tickets.update({message.author.id: {
                       "count" : msgnumber,
                       "author": message.author.name + '#' + message.author.discriminator,
                       "channel": message.channel.id,
                       "TicketNumber": TicketNumber,
                       "TicketName" : 'ticket-' + str(TicketNumber)
                       }})

           print(msgnumber)
           msgnumber = int(tickets[message.author.id]['count']) + 1
           tickets[message.author.id]['count'] = msgnumber 
           ticketnumber = int(tickets[message.author.id]['TicketNumber'])
           ticketname = tickets[message.author.id]['TicketName']
           channel = discord.utils.get(guild.text_channels, name=TicketName)
           catagory = discord.utils.get(guild.categories, id=798284727794270229)
           if channel is None:
               await guild.create_text_channel(TicketName, category=catagory)
           tickets[message.author.id].update({ msgnumber: {"content": message.content, "author": message.author.name + '#' + message.author.discriminator, }})
           print(tickets[message.author.id])
           print(message)
           channel = discord.utils.get(guild.text_channels, name=TicketName)
           yaml.dump(tickets)
           await channel.send(message.content)
           embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
           admin_log = client.get_channel(797996052074201088)
           await admin_log.send(embed=embedVar)
    elif message.channel.category_id == 798284727794270229:
       for ticket in tickets:
           if tickets[ticket]['TicketName'] == message.channel.name:
#                guild = client.get_guild(788119131068301332)
               user = await client.fetch_user(ticket)
               print(user)
               DM = await user.create_dm()
               embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
               await DM.send(embed=embedVar)
               msgnumber = int(tickets[ticket]['count']) + 1
               tickets[ticket]['count'] = msgnumber 
               ticketNumber = int(tickets[ticket]['TicketNumber'])
               TicketName = tickets[ticket]['TicketName']
               tickets[ticket].update({ msgnumber: {"content": message.content, "author": message.author.name + '#' + message.author.discriminator, }})
               print(tickets[ticket])
client.run(TOKEN)
