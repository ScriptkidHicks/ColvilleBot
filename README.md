# ColvilleBot
This bot acts as an aide for running dnd games on discord. Named after the eminent Colville DM.

Hi, I'm Tammas Hicks, and this is a bot I made for helping people with their dnd games. When 
I'm not in school or working I play dnd with my friends, and since the pandemic started we've 
moved all our games onto discord. We tried a series of other bots, but I noticed that either we
had to use a series of bots to accomplish all the functions we wanted, or the bots we were using
would only work intermittently / break when their web resources changed. I had a class which 
required me to build my own project, so I decided to build the Colville Bot, named in honor of
Matt Colville, one of my favorite DMs and youtubers. The bot is free, and open source, so feel
free to copy it, branch it, or work it up for your own personal needs! I hope it helps you with
your dnd games at this time when we're all having to play dnd from home.

HOW TO INSTALL
  Download the py files provided here, as well as all of the directories I have provided (or you
can make your own directories with the same names) to a folder of your choice. Get a token for 
your bot from discord, paste it into the ColvilleBot.py file where it says token, and run the 
python program. I will paste below a link to how to set up a bot on discord. You will only need
to get as far as setting up the token and bot on your discrod server, the programming is already
done for you!
  *You will want to have python 3.9 installed, as well as discord.py. 

Link:
https://realpython.com/how-to-make-a-discord-bot-python/


HOW TO USE
  The Colville Bot recognizes your commands when you start your message with a prefix. I have
set the prefix as 'Colville ', but you can set it up to whatever you like. You will find the
prefix in the instantiation of the command class. If you want something shorter, I highly
suggest a prefix which you're not going to use in a lot of other messages. Usually something
like '>' will be perfect for that. Consider that when you set up the prefix the spaces
included will be part of the prefix, meaning that '>' != '> '.

  The function you want to call is the next argument in the message. So if I want to call the
bot to use the 'test' function, my message would be as follows:

Colville test

Case matters, and the commands will always be one word. It doesn't feel like natural english, 
but the discord.py module doesn't include a way for me to have functions use extended names, so
RIP I guess.

  Next, you will want to provide necessary arguments in the message. For example, the
NewCharacter function takes *args for arguments, meaning that you can provide a name of any
length, and the bot will process it. The message would look as follows:

Colville NewCharacter Lord Percival Fredrickstein von Musel Klossowski de Rolo III

The bot would process the above argument, using it to track that character (Though the file the
character uses will have no spaces in the name, and be all lower case). Please keep in mind that
every time you want to call on that character sheet, or you want do update that character, you're
going to have to use that name, so insufferably long names will become a nightmare to type every time.

For a list of functions, call the Bark command, and if you want a clarifier on how to use a function,
call the Use command, with an argument of the function name. Colville will give you an explanation on
how to implement that specific command.
