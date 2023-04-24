import requests
import discord
from discord.ext import commands
import asyncio
import random
import random
import csv

secrets = []
with open('token.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        secrets.append(row[0])
token = secrets[0]
key = secrets[1]
print("token",token)
print("key",key)

#dictionary to hold extra headers
HEADERS = {"X-API-Key":key}
membershipType = "All"

url = 'https://www.bungie.net/platform/Destiny2/SearchDestinyPlayerByBungieName/{membershipType}/'.format(membershipType=membershipType)
User = {"displayName":"Nasa2907","displayNameCode":1043}
r = requests.post(url, headers=HEADERS, json=User);
#convert the json object we received into a Python dictionary object
#and print the name of the item

result = r.json()

destinyMembershipId = result['Response'][0].get("membershipId")
membershipType = result['Response'][0].get("membershipType")

url = "https://www.bungie.net/platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/".format(membershipType=membershipType,destinyMembershipId=destinyMembershipId)
r = requests.get(url, params={"components":"Characters"},headers=HEADERS);
result = r.json()

characters = result['Response']['characters']['data']
characterKeys = characters.keys()

classTypesToNames = ["Titan","Hunter","Warlock"]

classToId = {}
for chara in characterKeys:
    classToId[classTypesToNames[characters[chara].get("classType")]] = chara

url = "https://www.bungie.net/platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/".format(membershipType=membershipType,destinyMembershipId=destinyMembershipId)
r = requests.get(url, params={"components":"ProfileInventories"},headers=HEADERS);
result = r.json()


intents = discord.Intents.all() #(value=68608) 
client = commands.Bot(command_prefix="!", intents=intents)
prefix = "!"

class Cmd:
    message = ""
    tokens = []
    def __init__(self, message, tokens):
        self.message = message
        self.tokens = tokens

async def get_rockets(cmd):
    print("ROCKETSS!!")
    await cmd.message.channel.send("ROCKETS!!")

bot_commands = {
    "!getrockets": get_rockets,
}


@client.event
async def on_ready():
    print("online")


@client.event
async def on_message(ctx):
    print("yo")
    if ctx.content[0] == prefix:
        tokens = ctx.content.lower().split(" ")
        user_cmd = Cmd(ctx,tokens)
        function = bot_commands.get(user_cmd.tokens[0])
        await function(user_cmd)
        print("done?")



client.run(token)