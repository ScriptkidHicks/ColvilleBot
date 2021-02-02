"""
This is the first version of the Colville Bot
"""
import random
import discord
import asyncio
from discord.ext import commands


TOKEN = "Your Token goes here     jj "
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
async def RollDice(ctx, *args):
    errormsg = f"The format for this tool is : prefix command *nDx bonus. Please use that format."
    total = 0
    returnstring = "|"
    try:
        for x in range(len(args) - 1):
            temptotal = 0
            splitdice = args[x].lower().split("d")
            quantity, dice = int(splitdice[0]), int(splitdice[1])
            returnstring += f"{args[x]}="
            for y in range(quantity - 1):
                val = random.randint(0, dice)
                temptotal += val
                returnstring += f"{val}+"
            val = random.randint(0,dice)
            temptotal += val
            returnstring += f"{val}="
            returnstring += f"{temptotal}|"
            total += temptotal
        returnstring += f"bonus: {args[len(args) - 1]}|"
        total += int(args[len(args) - 1])
        returnstring += f"total = {total}"
        await ctx.send(returnstring)
    except ValueError:
        await ctx.send(errormsg)


@Colville.command()
async def Bark(ctx):
    message = "I have the following commands:\n" \
              "for formatting information on any of them, use the command: Usage\n" \
              "RollInit: Rolls a new initiative order\n" \
              "NewJoin: Adds a new player to initiative, and adds them to combat order\n" \
              "NewMember: Adds a new player, but does not roll them into initiative\n" \
              "PresentInit: Prints out the current initiative order\n" \
              "QuoteSpell: Reads out the contents of a spell from the handbook\n" \
              "Test: Reads a passage from Moby Dick to confirm that I can send messages!"
    await ctx.send(message)


@Colville.command()
async def QuoteSpell(ctx, *args):
    if not args:
        await ctx.send("Please specify a spell that you want me to quote.")
    name = ''
    for arg in args:
        name += arg.lower()
    message = ''
    try:
        with open(f"spells/{name}.txt") as spellfile:
            for line in spellfile.readlines():
                message += line
        await ctx.send(message)
    except FileNotFoundError:
        errormessage = ''
        for arg in args:
            errormessage += arg
        await ctx.send(f"I'm afraid the spell '{errormessage}' does no exist.")



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

