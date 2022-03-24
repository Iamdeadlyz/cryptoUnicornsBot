import asyncio
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from cryptoUnicorn import getUNIM

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
  await ctx.send(content=f"<@{ctx.author.id}>",embed=embed)

###########################################################################
#/breedunicorn

@slash.slash(
  name="breedUnicorn",
  description="Calculate the breeding costs",
  guild_ids=[000000000000000], #replace the guildID here to your server ID
  default_permission=True,
  options=[
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

async def breedUnicorn(ctx:SlashContext, parent_one:str, parent_two:str, breed_up_to:str, include_evolution_cost:bool):
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
    for x in range(parentOne+1,parentOne+breedUpTo+1): 
      totalUNIM = totalUNIM+breedPointsUNIM[x] #calculate UNIM needed for the first parent
      totalRBW = totalRBW+breedPointsRBW[x] #calculate RBW needed for the first parent
    for y in range(parentTwo+1,parentTwo+breedUpTo+1): 
      totalUNIM = totalUNIM+breedPointsUNIM[y] #calculate UNIM needed for the second parent
      totalRBW = totalRBW+breedPointsRBW[y] #calculate RBW needed for the second parent
    if include_evolution_cost is True:
      unimEvolutionCost, rbwEvolutionCost = 2500, 25
      totalUNIM = totalUNIM+(unimEvolutionCost*breedUpTo)
      totalRBW = totalRBW+(rbwEvolutionCost*breedUpTo)
      embed.add_field(name="Total UNIM needed (incl. evolution)", value=f"{totalUNIM} UNIM", inline=True)
      embed.add_field(name="Total RBW needed (incl. evolution)", value=f"{totalRBW} RBW", inline=True)
    else:
      embed.add_field(name="Total UNIM needed", value=f"{totalUNIM} UNIM", inline=True)
      embed.add_field(name="Total RBW needed", value=f"{totalRBW} RBW", inline=True)
    await message.edit(content=f"<@{ctx.author.id}>",embed=embed)

###########################################################################

client.run("enterYourDiscordBotToken")