"""
This is the first version of the Colville Bot
"""
from Initiative import Initiative
from Character import character
import random
import discord
import asyncio
import pickle
import os
from discord.ext import commands


TOKEN = "Your Token goes here"
intents = discord.Intents.default()
intents.members = True


class colville(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix=['Colville', '~', '>', '$'], case_insensitive=True)
        self.Initiative = Initiative()


Colville = colville()
client = discord.Client()

def to_lower(argument):
    return argument.lower()


@Colville.event
async def on_ready():
    print("This bot has connected to the server")


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
async def Use(ctx, command):
    command = command.lower()
    if not command:
        await ctx.send("Oops! it doesn't look like you provided a function for me to explain!")
    elif command.startswith('newcharacter'):
        await ctx.send("Colville NewCharacter Name(*args)\n"
                       "Creates a new .pickle file with your character object stored inside.")
    elif command.startswith('deletecharacter'):
        await ctx.send("Colville DeleteCharacter Name(*args)\n"
                       "Deletes the character pickle file if present, or tell you if that file doesn't exist.")
    elif command.startswith('setlevel'):
        await ctx.send("Colville SetLevel 'level'(int) name(*args)\n"
                       "Sets the level of the named character to the given integer")
    elif command.startswith('bark'):
        await ctx.send("Colville Bark\n"
                       "Colville reports all the commands it contains, and summarizes their use.")
    elif command.startswith('quotespell'):
        await ctx.send("Colville QuoteSpell 'spell name'(*args)\n"
                       "If the spell exists, Colville reports the contents of the spell.")
    else:
        await ctx.send(f"Uh oh, I don't recognize the command {command}!\n"
                       f"If you need a list of commands, please try the command 'Bark'(no arguments).")


@Colville.command()
async def NewCharacter(ctx, *args):
    name = ''
    for x in range(len(args) - 1):
        name += f"{args[x]} "
    name += args[len(args) - 1]
    searchname = ''.join(arg.lower() for arg in args)
    if os.path.exists(f"Characters/{searchname}.pickle"):
        await ctx.send(f"I'm sorry {ctx.author.nick if ctx.author.nick else ctx.author.name}"
                       f", a character by the name {name} already exists!\n"
                       f"Consider using the DeleteCharacter command to get rid of it!")
    else:
        newcharacter = character(name)
        with open(f"Characters/{searchname}.pickle", "wb+") as charsheet:
            pickle.dump(newcharacter, charsheet)
            await ctx.send(f"The character {name} has been created")


@Colville.command()
async def DeleteCharacter(ctx, *args):
    name = ''
    for x in range(len(args) - 1):
        name += f"{args[x]} "
    name += args[len(args) - 1]
    searchname = ''.join(arg.lower() for arg in args)
    if os.path.exists(f"Characters/{searchname}.pickle"):
        os.remove(f"Characters/{searchname}.pickle")
        await ctx.send(f"The character {name} has been thrown into the void")
    else:
        await ctx.send(f"I'm sorry {ctx.author.nick if ctx.author.nick else ctx.author.name}"
                       f", the character {name} doesn't appear to exist.\n"
                       f"So I guess you didn't need to delete it anyway, huh?")


@Colville.command()
async def SetLevel(ctx, *args):
    errormessage = "The use of this function is as follows: Level(int), Character Name"
    if not args:
        await ctx.send("You don't appear to have provided any arguments for that command!")
    elif len(args)<2:
        await ctx.send(errormessage)
    else:
        try:
            lvl = int(args[0])
            searchname = ''
            for arg in args[1:]:
                searchname += arg.lower()
            charsheet = open(f"Characters/{searchname}.pickle", 'rb')
            tempchar = pickle.load(charsheet)
            charsheet.close()
            tempchar.level = lvl
            os.remove(f"Characters/{searchname}.pickle")
            with open(f"Characters/{searchname}.pickle", 'wb') as newchar:
                pickle.dump(tempchar, newchar)
            await ctx.send(f"{ctx.author.nick if ctx.author.nick else ctx.author.name} I have finished!")
        except ValueError:
            await ctx.send(errormessage)


@Colville.command()
async def SetAttributes(ctx, *args: to_lower):
    errormessage = "The use of this function is as follows:\n" \
                   "you can pass in any number of attribute value pairings\n" \
                   "Colville SetAttributes name(s) | Attribute=Value\n" \
                   "ex: Colville SetAttributes str=12 int=13\n" \
                   "please do not use spaces between attribute, equals, and value."
    if not args:
        await ctx.send("You don't appear to have provided any arguments for that command!")
    elif len(args) < 3:
        await ctx.send(errormessage)
    else:
        try:
            messageindex = 0
            name = ''
            while args[messageindex] != '|':
                name += args[messageindex]
                messageindex += 1
            messageindex += 1
            if not os.path.exists(f"Characters/{name}.pickle"):
                await ctx.send(f"I'm sorry {ctx.author.nick if ctx.author.nick else ctx.author.name},"
                               f" a character with that name doesn't exist.")
                return
            charsheet = open(f"Characters/{name}.pickle", "rb")
            tempchar = pickle.load(charsheet)
            charsheet.close()
            for arg in args[messageindex:]:
                try:
                    atr = arg.split("=")
                    if atr[0] in tempchar.attributes:
                        tempchar.attributes[atr[0]] = int(atr[1])
                except:
                    await ctx.send(errormessage)
                    return
            os.remove(f"Characters/{name}.pickle")
            with open(f"Characters/{name}.pickle", "wb") as newchar:
                pickle.dump(tempchar, newchar)
            await ctx.send(f"{ctx.author.nick if ctx.author.nick else ctx.author.name} I have finished!")
        except:
            await ctx.send(errormessage)
            return


@Colville.command()
async def SetAge(ctx, *args: to_lower):
    errormessage = "The use of this function is as follows: Age(int) Character Name"
    if not args:
        await ctx.send("You don't appear to have provided any arguments for that command!")
    elif len(args)<2:
        await ctx.send(errormessage)
    else:
        try:
            age = int(args[0])
            searchname = ''
            for arg in args[1:]:
                searchname += arg
            charsheet = open(f"Characters/{searchname}.pickle", 'rb')
            tempchar = pickle.load(charsheet)
            charsheet.close()
            tempchar.age = age
            os.remove(f"Characters/{searchname}.pickle")
            with open(f"Characters/{searchname}.pickle", 'wb') as newchar:
                pickle.dump(tempchar, newchar)
            await ctx.send(f"{ctx.author.nick if ctx.author.nick else ctx.author.name} I have finished!")
        except ValueError:
            await ctx.send(errormessage)


@Colville.command()
async def SetClass(ctx, *args: to_lower):
    errormessage = "The use of this function is as follows: Class Character Name"
    if not args:
        await ctx.send("You don't appear to have provided any arguments for that command!")
    elif len(args) < 2:
        await ctx.send(errormessage)
    else:
        try:
            charclass = args[0]
            searchname = ''
            for arg in args[1:]:
                searchname += arg
            charsheet = open(f"Characters/{searchname}.pickle", 'rb')
            tempchar = pickle.load(charsheet)
            charsheet.close()
            tempchar.charClass = charclass
            os.remove(f"Characters/{searchname}.pickle")
            with open(f"Characters/{searchname}.pickle", 'wb') as newchar:
                pickle.dump(tempchar, newchar)
            await ctx.send(f"{ctx.author.nick if ctx.author.nick else ctx.author.name} I have finished!")
        except ValueError:
            await ctx.send(errormessage)


@Colville.command()
async def CallCharacterName(ctx, *args):
    searchname = ''.join(arg.lower() for arg in args)
    with open(f"Characters/{searchname}.pickle", 'rb') as charfile:
        tempchar = pickle.load(charfile)
        await ctx.send(f"The character {tempchar.name} has a strength of {tempchar.attributes['str']}")


@Colville.command()
async def RollDice(ctx, *args):
    errormsg = f"The format for this tool is : prefix command *nDx bonus.\nPlease use that format."
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
async def QuoteSpell(ctx, *args):
    if not args:
        await ctx.send(f"{ctx.author.nick if ctx.author.nick else ctx.author.name},"
                       f"please specify a spell that you want me to quote.")
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
        await ctx.send(f"I'm afraid the spell '{errormessage}' does not exist.")


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
async def SendMe(ctx, *args):
    prefix = args[0].lower().strip("'?-)(*&^%$$#@!{}[]|=+-")
    searchname = ''
    for arg in args[1:]:
        searchname += arg
    if prefix == 'npcs' or prefix == 'npc':
        await ctx.send(file=discord.File(f"NPCs/{searchname}.txt"))
    elif prefix == 'spell' or prefix == 'spells':
        await ctx.send(file=discord.File(f"Spells/{searchname}.txt"))
    elif prefix == 'characters' or prefix == 'character':
        await ctx.send(file=discord.File(f"Characters/{searchname}.pickle"))
    else:
        await ctx.send(f"I'm sorry {ctx.author.nick if ctx.author.nick else ctx.author.name},"
                       f" I don't recognize that prefix.")


@Colville.command()
async def NewNPC(ctx, *args):
    npcName = ''.join(arg.lower() for arg in args)
    npcFileName = ' '.join(arg for arg in args)
    with open(f"NPCs/{npcName}.txt", "w+") as newNPC:
        newNPC.write(npcFileName + '\n')
    await ctx.send(f"The new NPC has been created {ctx.author.nick if ctx.author.nick else ctx.author.name}!")


@Colville.command()
async def DeleteNPC(ctx, *args):
    npcName = ''.join(arg.lower() for arg in args)
    if os.path.exists(f"NPCs/{npcName}.txt"):
        os.remove(f"NPCs/{npcName}.txt")
        await ctx.send("Done!")
    else:
        await ctx.send(f"Oops, sorry {ctx.author.nick if ctx.author.nick else ctx.author.name}!"
                       f" That NPC doesn't appear to exist!")


@Colville.command()
async def AppendNPC(ctx, *args):
    errormessage = "The format of this tool is as follows: Character name | Message.\n" \
                   "The '|' is important, and must be spaced."
    if ('|' not in args) or (len(args) < 2):
        await ctx.send(errormessage)
        return
    argpointer = 0
    CharName = ''
    message = ''
    while args[argpointer] != '|':
        CharName += args[argpointer]
        argpointer += 1
    argpointer+= 1
    if not os.path.exists(f"NPCs/{CharName}.txt"):
        await ctx.send(f"I'm sorry {ctx.author.nick if ctx.author.nick else ctx.author.name},"
                       f" but that NPC doesn't appear to exist!")
    for arg in args[argpointer:]:
        message+= arg + ' '
    with open(f"NPCs/{CharName}.txt", "a") as npcFile:
        npcFile.write(f"{message}\n\n")


@Colville.command()
async def presentNPC(ctx, *args):
    npcName = ''.join(arg.lower() for arg in args)
    message = ''
    if not os.path.exists(f"NPCs/{npcName}.txt"):
        await ctx.send("I'm sorry, that quest doesn't seem to exist!")
    with open(f"NPCs/{npcName}.txt", 'r') as npctext:
        for line in npctext.readlines():
            message += line
    await ctx.send(message)


@Colville.command()
async def NewQuest(ctx, *args):
    QuestFileName = ''.join(arg.lower() for arg in args)
    QuestName = ' '.join(arg for arg in args)
    with open(f"Quests/{QuestFileName}.txt", "w+") as newNPC:
        newNPC.write(QuestName + '\n')
    await ctx.send("The new quest has been created!")


@Colville.command()
async def DeleteQuest(ctx, *args):
    QuestName = ''.join(arg.lower() for arg in args)
    if os.path.exists(f"Quests/{QuestName}.txt"):
        os.remove(f"Quests/{QuestName}.txt")
        await ctx.send("Done!")
    else:
        await ctx.send(f"Oops, sorry {ctx.author.nick if ctx.author.nick else ctx.author.name}!"
                       f" That quest doesn't appear to exist!")


@Colville.command()
async def AppendQuest(ctx, *args):
    errormessage = "The format of this tool is as follows: Quest Name | Message.\n" \
                   "The '|' is important, and must be spaced."
    if ('|' not in args) or (len(args) < 2):
        await ctx.send(errormessage)
        return
    argpointer = 0
    QuestName = ''
    message = ''
    while args[argpointer] != '|':
        QuestName += args[argpointer]
        argpointer += 1
    argpointer += 1
    if not os.path.exists(f"Quests/{QuestName}.txt"):
        await ctx.send(f"I'm sorry {ctx.author.nick if ctx.author.nick else ctx.author.name}, but that quest doesn't appear to exist!")
    for arg in args[argpointer:]:
        message += arg + ' '
    with open(f"Quests/{QuestName}.txt", "a") as npcFile:
        npcFile.write(f"{message}\n\n")


@Colville.command()
async def PresentQuest(ctx, *args: to_lower):
    QuestName = ''.join(arg for arg in args)
    message = ''
    if not os.path.exists(f"Quests/{QuestName}.txt"):
        await ctx.send("I'm sorry, that quest doesn't seem to exist!")
    with open(f"Quests/{QuestName}.txt", 'r') as npctext:
        for line in npctext.readlines():
            message += line
    await ctx.send(message)


@Colville.command()
async def test2(ctx, *args: to_lower):
    message = " ".join(arg for arg in args)
    await ctx.send(message)


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

