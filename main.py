import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from cryptoUnicorn import remainingShadowCornEggs, getShadowCorns, totalLootBox, getLootBox, unimLeft, getUNIM
from price import priceOfUNIM, getUNIMPrice

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
  embed.add_field(name="Mythic", value="{} out of 50 [-OS link-](https://opensea.io/assets/matic/0x99a558bdbde247c2b2716f0d4cfb0e246dfb697d/3)".format(remainingShadowCornEggs[0][0][2]), inline=False)
  await ctx.send(embed=embed)

###########################################################################

@slash.slash(
  name="lootbox",
  description="Get the total minted lootbox",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def lootbox(ctx:SlashContext):
  getLootBox()
  embed=discord.Embed(title="Crypto Unicorns Darkforest - Minted lootbox", description="\u200b", color=0xff00c8)
  embed.set_thumbnail(url="https://lh3.googleusercontent.com/EorjfSP6_15XdWcMLzJqHTC-y1aadmGeL_jydEtpL4aTj--lUdQ1GWy_bdvb8PN6Dmf46rXOZxgYQkbDVEoNnjHrWKO9HUdc39RdPkA=s0")
  embed.add_field(name="Rare Lootbox", value="{} minted. [-OS link-](https://opensea.io/assets/matic/0x99a558bdbde247c2b2716f0d4cfb0e246dfb697d/5)".format(totalLootBox["rare"]), inline=False)
  embed.add_field(name="Mythic Lootbox", value="{} minted. [-OS link-](https://opensea.io/assets/matic/0x99a558bdbde247c2b2716f0d4cfb0e246dfb697d/6)".format(totalLootBox["mythic"]), inline=False)
  await ctx.send(embed=embed)

###########################################################################

@slash.slash(
  name="unimLeft",
  description="Get the remaining UNIM tokens in the darkforest",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def unim(ctx:SlashContext):
  getUNIM()
  embed=discord.Embed(title="Crypto Unicorns Darkforest - Remaining UNIM", description="\u200b", color=0xff00c8)
  embed.set_thumbnail(url="https://lh3.googleusercontent.com/EorjfSP6_15XdWcMLzJqHTC-y1aadmGeL_jydEtpL4aTj--lUdQ1GWy_bdvb8PN6Dmf46rXOZxgYQkbDVEoNnjHrWKO9HUdc39RdPkA=s0")
  embed.add_field(name="UNIM", value="{}".format(unimLeft["unim"]), inline=False)
  await ctx.send(embed=embed)

###########################################################################

@slash.slash(
  name="unimPrice",
  description="Get the price of UNIM",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True,
  options=[
    create_option(
      name="currency",
      description="Choose the currency",
      required=True,
      option_type=3,
      choices=[
        create_choice(
          name="Ethereum",
          value="eth"
        ),
        create_choice(
          name="US Dollar",
          value="usd"
        ),
        create_choice(
          name="Philippine Peso",
          value="php"
        ),
        create_choice(
          name="Canadian Dollar",
          value="cad"
        ),
        create_choice(
          name="South African Rand",
          value="zar"
        ),
        create_choice(
          name="Hungarian Forint",
          value="huf"
        ),
        create_choice(
          name="Chinese Yuan",
          value="cny"
        ),
        create_choice(
          name="Russian Ruble",
          value="rub"
        ),
        create_choice(
          name="Thai Baht",
          value="thb"
        )
      ]
    ),
    create_option(
      name="amount",
      description="Choose the amount (optional)",
      required=False,
      option_type=4
    )
  ]
)

async def unimPrice(ctx:SlashContext, currency:str, amount:int = None):
  getUNIMPrice()
  if currency == "eth":
    price = ("%.17f" % priceOfUNIM["eth"]).rstrip('0').rstrip('.')
  else:
    price = priceOfUNIM[currency]
  embed=discord.Embed(title="Crypto Unicorns - UNIM price", description="Official contract address: 0x64060aB139Feaae7f06Ca4E63189D86aDEb51691", color=0xff00c8, url="https://www.coingecko.com/en/coins/unicorn-milk")
  embed.set_thumbnail(url="https://pbs.twimg.com/media/FLWja6dXIAoMgbC?format=png&name=small")
  embed.add_field(name="UNIM price", value=f"{price} {currency.upper()}", inline=False)
  if amount is not None:
    if currency == "eth":
      embed.add_field(name="Calculation", value=f"{price} {currency.upper()} * {amount} UNIM = {float(price)*amount} {currency.upper()}", inline=False)
    else:
      embed.add_field(name="Calculation", value=f"{price} {currency.upper()} * {amount} UNIM = {(price*amount):,.2f} {currency.upper()}", inline=False)
  embed.set_footer(text="Powered by Coingecko. Cached for 30s.",icon_url="https://static.coingecko.com/s/thumbnail-007177f3eca19695592f0b8b0eabbdae282b54154e1be912285c9034ea6cbaf2.png")
  await ctx.send(embed=embed)
  
###########################################################################

client.run("enterYourDiscordBotToken")