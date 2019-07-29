import json
import glob
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

def setup_auth(function):
    def check_auth(ctx):
        if "admin" in reactions[ctx.guild.id].keys():
            adminrole = ctx.guild.get_role(int(reactions[str(ctx.guild.id)]["admin"]))
            if adminrole in ctx.author.roles:
                return function(ctx)
            else:
                return ctx.send("not authorised")
        else:
            return function(ctx)
    return check_auth


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(bot.guilds)
    for g in bot.guilds:
        reactions[str(g.id)] = {}
    for file in glob.glob("settings/*.config"):
        sguild = file.split('/')[1].split('.')[0]
        try:
            with open('settings/{}.config'.format(sguild), 'r') as f:
                reactions[sguild] = json.load(f)
        except:
            print("ignoring file {} as there was an error".format(sguild))
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="v1.0.0"))



@bot.event
async def on_raw_reaction_add(payload):
    """Assign a role to someone based on the user's reaction"""
    print("found a reaction of {}".format(str(payload.emoji)))
    if payload.channel_id != reactions[str(payload.guild_id)]["ManagementChannel"]:
        print("whoops wrong channel, {}:{}".format(payload.channel_id, reactions[payload.guild_id]["ManagementChannel"]))
        return
    
    server = bot.get_guild(payload.guild_id)
    user = server.get_member(payload.user_id)
    try:
        if reactions[str(payload.guild_id)][str(payload.emoji)]:
            Role = server.get_role(int(reactions[str(payload.guild_id)][str(payload.emoji)]))
            print("applying role {} to {}".format(Role.name, user.name))
            await user.add_roles(Role)
    except:
        pass

@bot.event
async def on_raw_reaction_remove(payload):
    """Removes someone from a role based on the user's reaction"""
    print("found a reaction of {}".format(str(payload.emoji)))
    if payload.channel_id != reactions[str(payload.guild_id)]["ManagementChannel"]:
        print("whoops wrong channel, {}:{}".format(payload.channel_id, ManagementChannel))
        return
    
    server = bot.get_guild(payload.guild_id)
    user = server.get_member(payload.user_id)
    try:
        if reactions[str(payload.guild_id)][str(payload.emoji)]:
            Role = server.get_role(int(reactions[str(payload.guild_id)][str(payload.emoji)]))
            print("applying role {} to {}".format(Role.name, user.name))
            await user.remove_roles(Role)
    except Exception as e:
        print(e)

@bot.group()
async def owl(ctx):
    """check for a sub-command (setup or owl specific)"""
    if ctx.invoked_subcommand is None:
        await ctx.send('Yeah? What do you want?')




################################################################################### Setup for Reaction Roles
@owl.group()
async def setup(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Yeah? What do you want to setup?')

@setup_auth
@setup.command(name="setadmin")
async def _setadmin(ctx, role: int):
    """assigns a welcome channel to listen to reactions on"""
    reactions[str(ctx.guild.id)]["admin"] = int(role)
    await ctx.send('saved admin role, now only people with this role can configure your bot')

@setup_auth
@setup.command(name="channel")
async def _channel(ctx, channel: int):
    """assigns a welcome channel to listen to reactions on"""
    reactions[str(ctx.guild.id)]["ManagementChannel"] = int(channel)
    await ctx.send('saved management channel')

@setup_auth
@setup.command(name="roles")
async def _channel(ctx, emoji: str, role: int):
    """Assigns a reaction to a role"""
    reactions[str(ctx.guild.id)][emoji] = role
    await ctx.send('added reaction role')

@setup.command(name="save")
async def _save(ctx):
    """saves the config to a file"""
    with open('settings/{}.config'.format(ctx.guild.id), 'w') as file:
        json.dump(reactions[str(ctx.guild.id)], file)
    await ctx.send("successfully saved the configuration!")

@setup.command(name="load")
async def _load(ctx):
    """loads config from a file"""
    with open('settings/{}.config'.format(ctx.guild.id), 'r') as file:
        reactions[str(ctx.guild.id)] = json.load(file)


################################################################################### OWL Functionality
@owl.command(name="help")
async def _help(ctx):
    """displays help information"""
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
    """Gets team details from api.overwatchleague.com"""
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
