###########################################################################
#Old main.py which has the major shadowcorn act 1 and copper launch related commands 
###########################################################################

import asyncio
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from cryptoUnicorn import getShadowCorns, getLootBox, getUNIM, updateTransactions, getRequestIDs, filterSummons
from copper import getRBWCopperPrice
from rbwBalancerPrice import getRbwBalancerprice
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
#/shadowcorn

@slash.slash(
  name="shadowCorn",
  description="Get remaining shadow corns",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def shadowCorn(ctx:SlashContext):
  remainingShadowCornEggs = getShadowCorns()
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
#/summonresults

def percentage(part, whole):
  percentage = 100 * float(part)/float(whole)
  final = round(percentage,2)
  return str(final) + "%"

@slash.slash(
  name="summonresults",
  description="Get the number of summons of each category",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def summonresults(ctx:SlashContext):
  message = await ctx.send("Processing data. `/summonresults` commands sent before this message is fully processed will fail. Please wait for 1 to 10 minutes. Thanks!\n(If, after 10 minutes, the bot has not updated this message yet, please send the same command.)")
  updateTransactions()
  getRequestIDs()
  summons = filterSummons()
  basicTotalSummon = summons["basic"]["totalSummon"]
  basicRareLootbox = summons["basic"]["lootbox"]["rare"]
  basicShadowcornCommon = summons["basic"]["shadowCorns"]["common"]
  basicShadowcornRare = summons["basic"]["shadowCorns"]["rare"]
  basicShadowCornMythic = summons["basic"]["shadowCorns"]["mythic"]
  complexTotalSummon = summons["complex"]["totalSummon"]
  complexMythicLootbox = summons["complex"]["lootbox"]["mythic"]
  complexShadowCornCommon = summons["complex"]["shadowCorns"]["common"]
  complexShadowCornRare = summons["complex"]["shadowCorns"]["rare"]
  complexShadowCornMythic = summons["complex"]["shadowCorns"]["mythic"]
  advancedTotalSummon = summons["advanced"]["totalSummon"]
  advancedShadowcornCommon = summons["advanced"]["shadowCorns"]["common"]
  advancedShadowcornRare = summons["advanced"]["shadowCorns"]["rare"]
  advancedShadowcornMythic = summons["advanced"]["shadowCorns"]["mythic"]
  embed=discord.Embed(title="Crypto Unicorns Darkforest - Total summons per category", description="\u200b", color=0xff00c8)
  embed.set_thumbnail(url="https://lh3.googleusercontent.com/EorjfSP6_15XdWcMLzJqHTC-y1aadmGeL_jydEtpL4aTj--lUdQ1GWy_bdvb8PN6Dmf46rXOZxgYQkbDVEoNnjHrWKO9HUdc39RdPkA=s0")
  embed.add_field(name="Basic Summon (5k UNIM)", value=f"{basicTotalSummon}", inline=False)
  embed.add_field(name="Result: Rare lootbox", value=f"{basicRareLootbox} - {percentage(basicRareLootbox,basicTotalSummon)} chance", inline=True)
  embed.add_field(name="Result: Common Shadowcorn", value=f"{basicShadowcornCommon} - {percentage(basicShadowcornCommon,basicTotalSummon)} chance", inline=True)
  embed.add_field(name="Result: Rare Shadowcorn", value=f"{basicShadowcornRare} - {percentage(basicShadowcornRare,basicTotalSummon)} chance", inline=True)
  embed.add_field(name="Result: Mythic Shadowcorn", value=f"{basicShadowCornMythic} - {percentage(basicShadowCornMythic,basicTotalSummon)} chance", inline=True)
  embed.add_field(name="\u200b", value="\u200b", inline=False)
  embed.add_field(name="Complex Summon (21k UNIM)", value=f"{complexTotalSummon}", inline=False)
  embed.add_field(name="Result: Mythic lootbox", value=f"{complexMythicLootbox} - {percentage(complexMythicLootbox,complexTotalSummon)} chance", inline=True)
  embed.add_field(name="Result: Common Shadowcorn", value=f"{complexShadowCornCommon} - {percentage(complexShadowCornCommon,complexTotalSummon)} chance", inline=True)
  embed.add_field(name="Result: Rare Shadowcorn", value=f"{complexShadowCornRare} - {percentage(complexShadowCornRare,complexTotalSummon)} chance", inline=True)
  embed.add_field(name="Result: Mythic Shadowcorn", value=f"{complexShadowCornMythic} - {percentage(complexShadowCornMythic,complexTotalSummon)} chance", inline=True)
  embed.add_field(name="\u200b", value="\u200b", inline=False)
  embed.add_field(name="Advanced Summon (34k UNIM)", value=f"{advancedTotalSummon}", inline=False)
  embed.add_field(name="Result: Common Shadowcorn", value=f"{advancedShadowcornCommon} - {percentage(advancedShadowcornCommon,advancedTotalSummon)} chance", inline=True)
  embed.add_field(name="Result: Rare Shadowcorn", value=f"{advancedShadowcornRare} - {percentage(advancedShadowcornRare,advancedTotalSummon)} chance", inline=True)
  embed.add_field(name="Result: Mythic Shadowcorn", value=f"{advancedShadowcornMythic} - {percentage(advancedShadowcornMythic,advancedTotalSummon)} chance", inline=True)
  embed.add_field(name="\u200b", value="\u200b", inline=False)
  embed.add_field(name="Total shadowcorns minted", value=f"{summons['overall']['totalShadowCorns']}", inline=False)
  embed.add_field(name="Common", value=f"{summons['overall']['common']}", inline=True)
  embed.add_field(name="Rare", value=f"{summons['overall']['rare']}", inline=True)
  embed.add_field(name="Mythic", value=f"{summons['overall']['mythic']}", inline=True)
  await message.edit(content=None,embed=embed)

###########################################################################
#/lootbox

@slash.slash(
  name="lootbox",
  description="Get the total minted lootbox",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def lootbox(ctx:SlashContext):
  totalLootBox = getLootBox()
  embed=discord.Embed(title="Crypto Unicorns Darkforest - Minted lootbox", description="\u200b", color=0xff00c8)
  embed.set_thumbnail(url="https://lh3.googleusercontent.com/EorjfSP6_15XdWcMLzJqHTC-y1aadmGeL_jydEtpL4aTj--lUdQ1GWy_bdvb8PN6Dmf46rXOZxgYQkbDVEoNnjHrWKO9HUdc39RdPkA=s0")
  embed.add_field(name="Rare Lootbox", value="{} minted. [-OS link-](https://opensea.io/assets/matic/0x99a558bdbde247c2b2716f0d4cfb0e246dfb697d/5)".format(totalLootBox["rare"]), inline=False)
  embed.add_field(name="Mythic Lootbox", value="{} minted. [-OS link-](https://opensea.io/assets/matic/0x99a558bdbde247c2b2716f0d4cfb0e246dfb697d/6)".format(totalLootBox["mythic"]), inline=False)
  await ctx.send(embed=embed)

###########################################################################
#/unimleft

@slash.slash(
  name="unimLeft",
  description="Get the remaining UNIM tokens in the darkforest",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def unim(ctx:SlashContext):
  unimLeft = getUNIM()
  embed=discord.Embed(title="Crypto Unicorns Darkforest - Remaining UNIM", description="\u200b", color=0xff00c8)
  embed.set_thumbnail(url="https://lh3.googleusercontent.com/EorjfSP6_15XdWcMLzJqHTC-y1aadmGeL_jydEtpL4aTj--lUdQ1GWy_bdvb8PN6Dmf46rXOZxgYQkbDVEoNnjHrWKO9HUdc39RdPkA=s0")
  embed.add_field(name="UNIM", value="{}".format(unimLeft["unim"]), inline=False)
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
  await ctx.send(content=f"<@{ctx.author.id}>",embed=embed)
  
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
    await ctx.send(f"Can't breed. Your two unicorns cannot be bred to more than 8 times. Parent one has {parentOne}/8 while parent two has {parentTwo}/8 breeding points.",hidden=True)
  elif (parentOne+breedUpTo) > 8:
    await ctx.send(f"Can't breed. Your first unicorn cannot be bred to more than 8 times. Currently {parentOne}/8 breeding points.",hidden=True)
  elif (parentTwo+breedUpTo) > 8:
    await ctx.send(f"Can't breed. Your second unicorn cannot be bred to more than 8 times. Currently {parentTwo}/8 breeding points.",hidden=True)
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
    await message.edit(content=f"<@{ctx.author.id}>",embed=embed)

###########################################################################
#/rbwcopperprice

@slash.slash(
  name="rbwCopperPrice",
  description="Get the price of RBW in the Copper Launch",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def rbwCopperPrice(ctx:SlashContext, rbwamount:int = None):
  rbw = getRBWCopperPrice()
  rbwPrice = float(rbw["price"])
  embed=discord.Embed(title="Crypto Unicorns - RBW price in Copper", description="**Official contract address:** 0x431cd3c9ac9fc73644bf68bf5691f4b83f9e104f \n[Polygonscan link](https://polygonscan.com/token/0x431cd3c9ac9fc73644bf68bf5691f4b83f9e104f)", color=0xff00c8, url="https://polygon.copperlaunch.com/pools/0x34497B3fD9e337B19F3C0B119caFE78EA7F46a94")
  embed.set_thumbnail(url="https://pbs.twimg.com/media/FMsgyYFXMAsz4Vx?format=png")
  embed.add_field(name="RBW price", value=f"{rbwPrice:.4f} USDC", inline=False)
  if rbwamount is not None:
    calculation = rbwPrice * rbwamount
    embed.add_field(name="RBW calculation", value=f"{rbwPrice:.4f} USDC * {rbwamount} RBW = {calculation:.4f} USDC", inline=False)
  embed.add_field(name="Price last updated on", value="<t:{}:F>".format(rbw["timeAndDate"]), inline=False)
  await ctx.send(embed=embed)

###########################################################################
#/rbwbalancerprice

@slash.slash(
  name="rbwBalancerPrice",
  description="Get the price of RBW in Balancer",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True
)

async def rbwBalancerPrice(ctx:SlashContext, rbwamount:int = None):
  rbw = getRbwBalancerprice()
  embed=discord.Embed(title="Crypto Unicorns - RBW price in Balancer", description="**Official contract address:** 0x431cd3c9ac9fc73644bf68bf5691f4b83f9e104f \n[Polygonscan link](https://polygonscan.com/token/0x431cd3c9ac9fc73644bf68bf5691f4b83f9e104f)", color=0xff00c8, url="https://polygon.copperlaunch.com/pools/0x34497B3fD9e337B19F3C0B119caFE78EA7F46a94")
  embed.set_thumbnail(url="https://pbs.twimg.com/media/FMsgyYFXMAsz4Vx?format=png")
  embed.add_field(name="RBW price", value=f"{rbw:.4f} USDC", inline=False)
  if rbwamount is not None:
    calculation = rbw * rbwamount
    embed.add_field(name="RBW calculation", value=f"{rbw:.4f} USDC * {rbwamount} RBW = {calculation:.4f} USDC", inline=False)
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
  await ctx.send(content=f"<@{ctx.author.id}>",embed=embed)

###########################################################################

client.run("enterYourDiscordBotToken")