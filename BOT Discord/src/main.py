import discord 
from discord.ext import commands 
import datetime 
import pandas as pd
import random
bot = commands.Bot(command_prefix='_', description="Primer BOT del discord", help_command = None)

#Ayuda
@bot.command()
async def help(ctx):
    des = """
    Comandos del BOT (la idea es seguir agregando)\n
    _ping   --> el BOT te dice pong\n
    _juego  --> el BOT selecciona un juego al azar de una lista\n
    """
    embed = discord.Embed(title="Gallo claudio",description= des,
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.blue())
    embed.set_footer(text="solicitado por: {}".format(ctx.author.name))
    embed.set_author(name="Felipe",       
    icon_url="")
    await ctx.send(embed=embed)
#Ping-pong
@bot.command()
async def ping(ctx):
     await ctx.send('pong')
#Pong
@bot.command()
async def pong(ctx):
     await ctx.send('QUIEN CHUCHA TE DIJO QUE PUSIERAI PONG PAO CULIAO')
#Elegir juego al azar
@bot.command()
async def juego(ctx):
    juegos = pd.read_csv(r"C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Cabros/Juegos.csv")
    juegos = list(juegos['Juegos'])
    seleccion = random.choice(juegos)
    embed = discord.Embed(title=seleccion,description= juegos ,
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.blue())
    embed.set_footer(text="lucho te aprecio {}".format(ctx.author.name))
    embed.set_author(name="Juegos",       
    icon_url="")
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="_help"))
    print('My bot is ready')

#SUS
@bot.command()
async def sus(ctx):
     await ctx.send('.p https://youtu.be/ekL881PJMjI')

bot.run('OTkxNDQ3MzIxMDA1MDExMDc2.G9FJXg.ti0ra1h7P_yvPi8E-tssjaQ85AmKj_UXGbRGCk')