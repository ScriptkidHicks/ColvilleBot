"""
This is the first version of the Colville Bot
"""
import random
import discord
import asyncio
from discord.ext import commands


TOKEN = "Your Token goes here"
intents = discord.Intents.default()
intents.members = True


class Initiative:

    def __init__(self):
        self.order = []
        self.members = {}

    def intake(self, member: str, bonus: int):
        self.members[member] = bonus

    def insert(self, member: str, bonus: int):
        self.members[member] = bonus
        roll = random.randint(1, 20) + bonus
        self.order.append((member, roll))
        self.order.sort(reverse=True, key=lambda tup: tup[1])

    def remove(self, member: str):
        try:
            self.members.pop(member)
            return None
        except KeyError:
            return f"{member} was not in initiative."

    def rollup_initiative(self):
        self.order = []
        for member in self.members:
            roll = random.randint(1, 20)
            self.order.append((member, self.members[member] + roll))
            self.order.sort(reverse=True, key=lambda tup: tup[1])

    def clear(self):
        self.order = []
        self.members = {}

    def present(self):
        send_string = ""
        for member in self.order:
            send_string += f"{member[0]}: {member[1]}\n"
        return send_string


class colvile(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='Colville ')
        self.Initiative = Initiative()


Colville = colvile()


@Colville.event
async def on_ready():
    print("This bot has connected to the server")


@Colville.command()
async def RollInit(ctx):
    Colville.Initiative.rollup_initiative()
    sendout = Colville.Initiative.present()
    if sendout == '':
        await ctx.send("There are currently no players in combat")
    else:
        await ctx.send(sendout)


@Colville.command()
async def NewJoin(ctx, member, bonus):
    Colville.Initiative.insert(member, int(bonus))
    ctx.send(Colville.Initiative.present())


@Colville.command()
async def NewMember(ctx, member, bonus):
    Colville.Initiative.intake(member, int(bonus))
    await ctx.send(f"New combatant {member} with initiative bonus {bonus}\n"
             f"There are currently {len(Colville.Initiative.members)} combatants.")


@Colville.command()
async def PresentInit(ctx):
    this = Colville.Initiative.present()
    await ctx.send(this)


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

