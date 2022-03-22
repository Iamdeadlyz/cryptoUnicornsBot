import asyncio
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from cryptoUnicorn import getUNIM
from price import priceOfUNIM, getUNIMprice, priceOfRBW, getRBWprice

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
#/unimleft

@slash.slash(
  name="unimLeft",
  description="Get the remaining UNIM tokens in the darkforest",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def unimLeft(ctx:SlashContext):
  unimLeftInDf = await asyncio.get_running_loop().run_in_executor(None, getUNIM)
  embed=discord.Embed(title="Crypto Unicorns Darkforest - Remaining UNIM", description="\u200b", color=0xff00c8)
  embed.set_thumbnail(url="https://lh3.googleusercontent.com/EorjfSP6_15XdWcMLzJqHTC-y1aadmGeL_jydEtpL4aTj--lUdQ1GWy_bdvb8PN6Dmf46rXOZxgYQkbDVEoNnjHrWKO9HUdc39RdPkA=s0")
  embed.add_field(name="UNIM", value="{}".format(unimLeftInDf["unim"]), inline=False)
  await ctx.send(embed=embed)

###########################################################################
#/unimprice

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
      description="Enter the amount (optional)",
      required=False,
      option_type=4
    )
  ]
)

async def unimPrice(ctx:SlashContext, currency:str, amount:int = None):
  await asyncio.get_running_loop().run_in_executor(None, getUNIMprice)
  if currency == "eth":
    price = ("%.17f" % priceOfUNIM["eth"]).rstrip('0').rstrip('.')
  else:
    price = priceOfUNIM[currency]
  embed=discord.Embed(title="Crypto Unicorns - UNIM price", description="**Official contract address:** 0x64060aB139Feaae7f06Ca4E63189D86aDEb51691 \n[Polygonscan link](https://polygonscan.com/token/0x64060ab139feaae7f06ca4e63189d86adeb51691)", color=0xff00c8, url="https://www.coingecko.com/en/coins/unicorn-milk")
  embed.set_thumbnail(url="https://pbs.twimg.com/media/FLWja6dXIAoMgbC?format=png&name=small")
  embed.add_field(name="UNIM price", value=f"{price} {currency.upper()}", inline=False)
  if amount is not None:
    if currency == "eth":
      calculation = float(price)*amount
      finalCalc = ("%.17f" % calculation).rstrip('0').rstrip('.')
      embed.add_field(name="Calculation", value=f"{price} {currency.upper()} * {amount} UNIM = {finalCalc} {currency.upper()}", inline=False)
    else:
      embed.add_field(name="Calculation", value=f"{price} {currency.upper()} * {amount} UNIM = {(price*amount):,.2f} {currency.upper()}", inline=False)
  embed.set_footer(text="Powered by Coingecko. Cached for 30s.",icon_url="https://static.coingecko.com/s/thumbnail-007177f3eca19695592f0b8b0eabbdae282b54154e1be912285c9034ea6cbaf2.png")
  await ctx.send(embed=embed)

###########################################################################
#/rbwprice

@slash.slash(
  name="rbwPrice",
  description="Get the price of RBW",
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
      description="Enter the amount (optional)",
      required=False,
      option_type=4
    )
  ]
)

async def rbwPrice(ctx:SlashContext, currency:str, amount:int = None):
  await asyncio.get_running_loop().run_in_executor(None, getRBWprice)
  if currency == "eth":
    price = ("%.17f" % priceOfRBW["eth"]).rstrip('0').rstrip('.')
  else:
    price = priceOfRBW[currency]
  embed=discord.Embed(title="Crypto Unicorns - RBW price", description="**Official contract address:** 0x431cd3c9ac9fc73644bf68bf5691f4b83f9e104f \n[Polygonscan link](https://polygonscan.com/token/0x431cd3c9ac9fc73644bf68bf5691f4b83f9e104f)", color=0xff00c8, url="https://www.coingecko.com/en/coins/rainbow-token-2")
  embed.set_thumbnail(url="https://pbs.twimg.com/media/FMsgyYFXMAsz4Vx?format=png")
  embed.add_field(name="RBW price", value=f"{price} {currency.upper()}", inline=False)
  if amount is not None:
    if currency == "eth":
      calculation = float(price)*amount
      finalCalc = ("%.17f" % calculation).rstrip('0').rstrip('.')
      embed.add_field(name="Calculation", value=f"{price} {currency.upper()} * {amount} RBW = {finalCalc} {currency.upper()}", inline=False)
    else:
      embed.add_field(name="Calculation", value=f"{price} {currency.upper()} * {amount} RBW = {(price*amount):,.2f} {currency.upper()}", inline=False)
  embed.set_footer(text="Powered by Coingecko. Cached for 30s.",icon_url="https://static.coingecko.com/s/thumbnail-007177f3eca19695592f0b8b0eabbdae282b54154e1be912285c9034ea6cbaf2.png")
  await ctx.send(embed=embed)
  
###########################################################################
#/breedunicorn

@slash.slash(
  name="breedUnicorn",
  description="Calculate the breed points of a unicorn",
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
      name="parent_one",
      description="Enter the current breed count of your first unicorn",
      required=True,
      option_type=3,
      choices=[
        create_choice(
          name="0/8",
          value="0"
        ),
        create_choice(
          name="1/8",
          value="1"
        ),
        create_choice(
          name="2/8",
          value="2"
        ),
        create_choice(
          name="3/8",
          value="3"
        ),
        create_choice(
          name="4/8",
          value="4"
        ),
        create_choice(
          name="5/8",
          value="5"
        ),
        create_choice(
          name="6/8",
          value="6"
        ),
        create_choice(
          name="7/8",
          value="7"
        )
      ]
    ),
    create_option(
      name="parent_two",
      description="Enter the current breed count of your 2nd unicorn",
      required=True,
      option_type=3,
      choices=[
        create_choice(
          name="0/8",
          value="0"
        ),
        create_choice(
          name="1/8",
          value="1"
        ),
        create_choice(
          name="2/8",
          value="2"
        ),
        create_choice(
          name="3/8",
          value="3"
        ),
        create_choice(
          name="4/8",
          value="4"
        ),
        create_choice(
          name="5/8",
          value="5"
        ),
        create_choice(
          name="6/8",
          value="6"
        ),
        create_choice(
          name="7/8",
          value="7"
        )
      ]
    ),
    create_option(
      name="breed_up_to",
      description="How many times do you want to breed the unicorns?",
      required=True,
      option_type=4,
      choices=[
        create_choice(
          name=1,
          value=1
        ),
        create_choice(
          name=2,
          value=2
        ),
        create_choice(
          name=3,
          value=3
        ),
        create_choice(
          name=4,
          value=4
        ),
        create_choice(
          name=5,
          value=5
        ),
        create_choice(
          name=6,
          value=6
        ),
        create_choice(
          name=7,
          value=7
        ),
        create_choice(
          name=8,
          value=8
        )
      ]
    ),
    create_option(
      name="include_evolution_cost",
      description="Want to include the evolution costs of all children?",
      required=True,
      option_type=5
    )
  ]
)

async def breedUnicorn(ctx:SlashContext, currency:str, parent_one:str, parent_two:str, breed_up_to:str, include_evolution_cost:bool):
  parentOne = int(parent_one)
  parentTwo = int(parent_two)
  breedUpTo = int(breed_up_to)
  if (parentOne+breedUpTo) > 8 and (parentTwo+breedUpTo) > 8:
    await ctx.send(f"Can't breed. Your two unicorns cannot be bred to more than 8 times. Currently {parentOne}/8.",hidden=True)
  elif (parentOne+breedUpTo) > 8:
    await ctx.send(f"Can't breed. Your first unicorn cannot be bred to more than 8 times. Currently {parentOne}/8.",hidden=True)
  elif (parentTwo+breedUpTo) > 8:
    await ctx.send(f"Can't breed. Your second unicorn cannot be bred to more than 8 times. Currently {parentTwo}/8.",hidden=True)
  else:
    totalUNIM, totalRBW = 0, 0
    totalBreedingCost = 0
    await asyncio.get_running_loop().run_in_executor(None, getUNIMprice)
    await asyncio.get_running_loop().run_in_executor(None, getRBWprice)
    if currency == "eth":
      thePriceOfUNIM = ("%.17f" % priceOfUNIM["eth"]).rstrip('0').rstrip('.')
      thePriceOfRBW = ("%.17f" % priceOfRBW["eth"]).rstrip('0').rstrip('.')
    else:
      thePriceOfUNIM = priceOfUNIM[currency]
      thePriceOfRBW = priceOfRBW[currency]
    breedPointsUNIM = {
      0:0,
      1:300,
      2:700,
      3:1500,
      4:2700,
      5:4200,
      6:6000,
      7:9000,
      8:12000
    }
    breedPointsRBW = {
      0:0,
      1:5,
      2:5,
      3:5,
      4:5,
      5:5,
      6:5,
      7:5,
      8:5
    }
    message = await ctx.send("Calculating...")
    embed=discord.Embed(title="Crypto Unicorns - Breeding calculator", description="**Official contract addresses:**\n UNIM - 0x64060aB139Feaae7f06Ca4E63189D86aDEb51691\n[Polygonscan link](https://polygonscan.com/token/0x64060ab139feaae7f06ca4e63189d86adeb51691)\n RBW - 0x431cd3c9ac9fc73644bf68bf5691f4b83f9e104f\n[Polygonscan link](https://polygonscan.com/token/0x431cd3c9ac9fc73644bf68bf5691f4b83f9e104f)\n[Breeding costs article](https://medium.com/@lagunagames/breeding-costs-unim-rbw-228be48db67d)", color=0xff00c8)
    embed.set_thumbnail(url="https://i.imgur.com/cQRs6Xz.png")
    embed.add_field(name="Parent 1", value=f"{parentOne}/8", inline=True)
    embed.add_field(name="Parent 2", value=f"{parentTwo}/8", inline=True)
    embed.add_field(name="Breed", value=f"{breedUpTo} time(s)", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    for x in range(parentOne+1,parentOne+breedUpTo+1): #calculate UNIM needed for the first parent
      totalUNIM = totalUNIM+breedPointsUNIM[x]
    for y in range(parentTwo+1,parentTwo+breedUpTo+1): #calculate UNIM needed for the second parent
      totalUNIM = totalUNIM+breedPointsUNIM[y]
    if include_evolution_cost is True:
      unimEvolutionCost = 2500
      totalUNIM = totalUNIM+(unimEvolutionCost*breedUpTo)
      embed.add_field(name="Total UNIM needed (incl. evolution)", value=f"{totalUNIM} UNIM", inline=True)
    else:
      embed.add_field(name="Total UNIM needed", value=f"{totalUNIM} UNIM", inline=True)
    for x in range(parentOne+1,parentOne+breedUpTo+1): #calculate RBW needed for the first parent
      totalRBW = totalRBW+breedPointsRBW[x]
    for y in range(parentTwo+1,parentTwo+breedUpTo+1): #calculate RBW needed for the second parent
      totalRBW = totalRBW+breedPointsRBW[y]
    if include_evolution_cost is True:
      rbwEvolutionCost = 25
      totalRBW = totalRBW+(rbwEvolutionCost*breedUpTo)
      embed.add_field(name="Total RBW needed (incl. evolution)", value=f"{totalRBW} RBW", inline=True)
    else:
      embed.add_field(name="Total RBW needed", value=f"{totalRBW} RBW", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    if currency == "eth":
      unimCalculation = float(thePriceOfUNIM)*totalUNIM
      finalUNIMcalc = ("%.17f" % unimCalculation).rstrip('0').rstrip('.')
      rbwCalculation = float(thePriceOfRBW)*totalRBW
      finalRBWcalc = ("%.17f" % rbwCalculation).rstrip('0').rstrip('.')
      totalBreedingCost = unimCalculation + rbwCalculation
      embed.add_field(name="UNIM price", value=f"{thePriceOfUNIM} {currency.upper()}", inline=True)
      embed.add_field(name="UNIM calculation", value=f"{thePriceOfUNIM} {currency.upper()} * {totalUNIM} UNIM = {finalUNIMcalc} {currency.upper()}", inline=True)
      embed.add_field(name="\u200b", value="\u200b", inline=False)
      embed.add_field(name="RBW price", value=f"{thePriceOfRBW} {currency.upper()}", inline=True)
      embed.add_field(name="RBW calculation", value=f"{thePriceOfRBW} {currency.upper()} * {totalRBW} UNIM = {finalRBWcalc} {currency.upper()}", inline=True)
    else:
      unimCalculation = thePriceOfUNIM * totalUNIM
      rbwCalculation = thePriceOfRBW * totalRBW
      totalBreedingCost = unimCalculation + rbwCalculation
      embed.add_field(name="UNIM price", value=f"{thePriceOfUNIM:.2f} {currency.upper()}", inline=True)
      embed.add_field(name="UNIM calculation", value=f"{thePriceOfUNIM:.2f} {currency.upper()} * {totalUNIM} UNIM = {unimCalculation:,.2f} {currency.upper()}", inline=True)
      embed.add_field(name="\u200b", value="\u200b", inline=False)
      embed.add_field(name="RBW price", value=f"{thePriceOfRBW:.2f} {currency.upper()}", inline=True)
      embed.add_field(name="RBW calculation", value=f"{thePriceOfRBW:.2f} {currency.upper()} * {totalRBW} UNIM = {rbwCalculation:,.2f} {currency.upper()}", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    if currency == "eth":
      embed.add_field(name="Total breeding cost", value=f"{totalBreedingCost} {currency.upper()}", inline=False)
    else:
      embed.add_field(name="Total breeding cost", value=f"{totalBreedingCost:,.2f} {currency.upper()}", inline=False)
    embed.set_footer(text="Powered by Coingecko. Cached for 30s.",icon_url="https://static.coingecko.com/s/thumbnail-007177f3eca19695592f0b8b0eabbdae282b54154e1be912285c9034ea6cbaf2.png")
    await message.edit(content=None,embed=embed)

###########################################################################

client.run("enterYourDiscordBotToken")