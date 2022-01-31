import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from cryptoUnicorn import remainingShadowCornEggs, getShadowCorns

###########################################################################

client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
###########################################################################

@slash.slash(
  name="shadowCorn",
  description="Get remaining shadow corns",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def shadowCorn(ctx:SlashContext):
  getShadowCorns()
  embed=discord.Embed(title="Crypto Unicorns Darkforest - Remaining shadowcorn eggs", description="\u200b", color=0xff00c8)
  embed.set_thumbnail(url="https://lh3.googleusercontent.com/EorjfSP6_15XdWcMLzJqHTC-y1aadmGeL_jydEtpL4aTj--lUdQ1GWy_bdvb8PN6Dmf46rXOZxgYQkbDVEoNnjHrWKO9HUdc39RdPkA=s0")
  embed.add_field(name="Total eggs", value="3000", inline=False)
  embed.add_field(name="Redeemable", value="{}".format(remainingShadowCornEggs[0][1]), inline=False)
  embed.add_field(name="Redeemed", value="{}".format(3000-remainingShadowCornEggs[0][1]), inline=False)
  embed.add_field(name="\u200b", value="\u200b", inline=False)
  embed.add_field(name="Common", value="{} out of 2000 [-OS link-](https://opensea.io/assets/matic/0x99a558bdbde247c2b2716f0d4cfb0e246dfb697d/1)".format(remainingShadowCornEggs[0][0][0]), inline=False)
  embed.add_field(name="Rare", value="{} out of 950 [-OS link-](https://opensea.io/assets/matic/0x99a558bdbde247c2b2716f0d4cfb0e246dfb697d/2)".format(remainingShadowCornEggs[0][0][1]), inline=False)
  embed.add_field(name="Epic", value="{} out of 50 [-OS link-](https://opensea.io/assets/matic/0x99a558bdbde247c2b2716f0d4cfb0e246dfb697d/3)".format(remainingShadowCornEggs[0][0][2]), inline=False)
  await ctx.send(embed=embed)

###########################################################################

client.run("enterYourDiscordBotToken")