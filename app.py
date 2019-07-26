import json
import OWLPy
import discord
import datetime
import requests
from bs4 import BeautifulSoup as bs
from discord.ext import commands
from discord.utils import get

import secret

bot = commands.Bot(command_prefix="!", description="Commands to get OWL info")
reactions = {}
ManagementChannel = 0

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(bot.guilds)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Testing Version 0.01"))



@bot.event
async def on_raw_reaction_add(payload):
    print("found a reaction of {}".format(str(payload.emoji)))
    global ManagementChannel
    if payload.channel_id != ManagementChannel:
        print("whoops wrong channel, {}:{}".format(payload.channel_id, ManagementChannel))
        return
    
    server = bot.get_guild(payload.guild_id)
    user = server.get_member(payload.user_id)
    try:
        if reactions[str(payload.emoji)]:
            Role = server.get_role(int(reactions[str(payload.emoji)]))
            print("applying role {} to {}".format(Role.name, user.name))
            await user.add_roles(Role)
    except:
        pass

@bot.event
async def on_raw_reaction_remove(payload):
    print("found a reaction of {}".format(str(payload.emoji)))
    global ManagementChannel
    if payload.channel_id != ManagementChannel:
        print("whoops wrong channel, {}:{}".format(payload.channel_id, ManagementChannel))
        return
    
    server = bot.get_guild(payload.guild_id)
    user = server.get_member(payload.user_id)
    try:
        if reactions[str(payload.emoji)]:
            Role = server.get_role(int(reactions[str(payload.emoji)]))
            print("applying role {} to {}".format(Role.name, user.name))
            await user.remove_roles(Role)
    except Exception as e:
        print(e)

@bot.group()
async def owl(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('Yeah? What do you want?')

@owl.group()
async def setup(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Yeah? What do you want to setup?')

@setup.command(name="channel")
async def _channel(ctx, channel: int):
    global ManagementChannel
    ManagementChannel = int(channel)
    await ctx.send('saved management channel')

@setup.command(name="roles")
async def _channel(ctx, emoji: str, role: int):
    reactions[emoji] = role
    await ctx.send('added reaction role')

@owl.command(name="help")
async def _list(ctx):
    """Gets the current match details from api.overwatchleague.com"""
    await ctx.send("No hooting way!")


@owl.command(name='right-now')
async def rightnow(ctx):
    """Gets the current match details from api.overwatchleague.com"""
    await ctx.send("There are no current matches")

@owl.command(name='player')
async def _player(ctx, playerName: str):
    """Gets player details from api.overwatchleague.com"""
    if playerName == None:
        await ctx.send("Which player do you want to view?")
    else:
        d = OWLPy.Driver()
        player = d.get_player_by_name(playerName)
        team = player.get_team()
        embed = discord.Embed(title=player.formatted_name(), colour=discord.Colour(int(player.teams[0]["team"]["primaryColor"],16)), url=team.website, description="{} plays {} for {}".format(player.name, player.attributes["role"], team.name), timestamp=datetime.datetime.utcfromtimestamp(1563783616))

        embed.set_image(url=player.headshot)
        # embed.set_thumbnail(url=player["headshot"])
        embed.set_author(name="OWL-Bot", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text="Provided by OWLPy, Spydernaz", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Team", value=team.name)
        embed.add_field(name="Player Number", value=player.attributes["player_number"], inline=True)
        embed.add_field(name="Nationality", value=player.teams[0]["team"]["name"], inline=True)

        embed.add_field(name="Social Media Accounts for {}".format(player.formatted_name()), value=".")
        for a in player.accounts:
            embed.add_field(name=a.type, value=a.url, inline=True)
            
        # embed.add_field(name="😱", value="try exceeding some of them!")
        # embed.add_field(name="🙄", value="an informative error should show up, and this view will remain as-is until all issues are fixed")
        # embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
        # embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)

        #await ctx.send(content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```", embed=embed)
        await ctx.send(content="Here is some info on {}".format(player.formatted_name()), embed=embed)



@owl.command(name='team')
async def _team(ctx, teamName: str):
    """Gets player details from api.overwatchleague.com"""
    if teamName == None:
        await ctx.send("Which team do you want to view?")
    else:
        try:
            d = OWLPy.Driver()
            team = d.get_team_by_name(teamName)
            embed = discord.Embed(title=team.name, colour=discord.Colour(int(team.colors.primary)), url=team.website, description="{}".format(team.name), timestamp=datetime.datetime.utcfromtimestamp(1563783616))

            embed.set_image(url=team.logo["altDark"]["png"])
            # embed.set_thumbnail(url=player["headshot"])
            embed.set_author(name="OWL-Bot", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_footer(text="Provided by OWLPy, Spydernaz", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

            embed.add_field(name="Team:", value=team.name)
            embed.add_field(name="Location:", value=team.location, inline=True)

            embed.add_field(name="Social Media Accounts for {}".format(team.name), value=".")
            for a in team.accounts:
                embed.add_field(name=a.type, value=a.url, inline=True)
                
            # embed.add_field(name="😱", value="try exceeding some of them!")
            # embed.add_field(name="🙄", value="an informative error should show up, and this view will remain as-is until all issues are fixed")
            # embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
            # embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)

            #await ctx.send(content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```", embed=embed)
            await ctx.send(content="Here is some info on {}".format(team.name), embed=embed)
        except OWLPy.errors.customerrors.TeamNotFound as e:
            await ctx.send("we couldnt find a team by the name of {}. If it is a multi-word team try wrapping \"quotes\" around it".format(teamName))


@owl.command(name='schedule')
async def _schedule(ctx, s: str):
    """Gets player details from api.overwatchleague.com"""
    if s.lower() == "help":
        await ctx.send("Options are \na. <team>: enter a team name for their next 3 games\nb. <round>: enter a round number\nc. \"next\": for the next week")
    elif s == None:
        await ctx.send("Which schedule do you want to view?\n Type ```!owl schedule help``` for help")
    else:
        d = OWLPy.Driver()
        await ctx.send("getting schedule for {}".format(s))


### Use https://playoverwatch.com/en-us/career/pc/Spydernaz-1124 to confirm hero times

bot.run(secret.botPWD)
