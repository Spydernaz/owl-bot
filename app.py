import json
import OWLPy
import discord
import datetime
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix="!", description="Commands to get OWL info")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Testing Version 0.01"))





@bot.group()
async def owl(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('Yeah? What do you want?')

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
        await ctx.send("Which Player do you want to view?")
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
        await ctx.send("Which Player do you want to view?")
    else:
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


bot.run("NjAxMDY2ODY0OTQwMTU0ODgx.XS9fuw.ZSYTyeFgY84FBmCa8zC26fREUGc")
