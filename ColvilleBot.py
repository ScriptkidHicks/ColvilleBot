"""
This is the first version of the Colville Bot
"""
import discord
import asyncio
from discord.ext import commands


TOKEN = "Nzk5Mzc2NjEyMTQ3MzMxMTQ0.YACrfA.lCKs42Id2goyMFR2StMuh6uxXA0"
intents = discord.Intents.default()
intents.members = True


class Initiative:

    def __init__(self):
        self.order = []
        self.members = {}

    def intake(self, member: str, bonus: int):
        self.members[member] = bonus

    def remove(self, member: str):
        try:
            self.members.pop(member)
            return None
        except KeyError:
            return f"{member} was not in initiative."


initiative_roll = Initiative()

Colville = commands.Bot(command_prefix='>')


@Colville.event
async def on_ready():
    print("This bot has connected to the server")


@Colville.command()
async def test(ctx):
    await ctx.send("Consider the subtleness of the sea; how its most dreaded creatures glide under water,"
                   " unapparent for the most part, and treacherously hidden beneath the loveliest tints of azure. "
                   "Consider also the devilish brilliance and beauty of many of its most remorseless tribes, "
                   "as the dainty embellished shape of many species of sharks. Consider, once more, the universal "
                   "cannibalism of the sea; all whose creatures prey upon each other, carrying on eternal war "
                   "since the world began.Consider all this; and then turn to the green, gentle, and most docile "
                   "earth; consider them both, the sea and the land; and do you not find a strange analogy to something "
                   "in yourself? For as this appalling ocean surrounds the verdant land, so in the soul of man there "
                   "lies one insular Tahiti, full of peace and joy, but encompassed by all the horrors of the half-known "
                   "life. God keep thee! Push not off from that isle, thou canst never return!")

Colville.run(TOKEN)

