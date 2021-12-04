import discord, os, datetime, random, asyncio, discord_slash, traceback, functools
from discord.ext import commands, tasks
from keep_alive import keep_alive
from replit import db
from discord_slash.utils.manage_commands import create_option, create_choice

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="&", intents=intents)
slash = discord_slash.SlashCommand(bot, sync_commands=True)
bot.remove_command("help")
prayers = None

def error_messager(error_channel):
  def wrapper_error(func):
    @functools.wraps(func)
    async def wrapped_error(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      except:
        kwargs.send("Hey <@615188089840861214> looks like Gary himself intervened with the making of today's quote, can you check it out?\n" + traceback.format_exc())
    return wrapped_error
  return wrapper_error

async def unix_time(dt: datetime.datetime) -> datetime.datetime:
  return (dt - datetime.datetime.utcfromtimestamp(0)).total_seconds()

async def get_next_day(now: datetime.datetime) -> datetime.datetime:
  next_day = None

  try:
    next_day = datetime.datetime(now.year, now.month, now.day+1)
  except ValueError:
    try:
      next_day = datetime.datetime(now.year, now.month + 1, 1)
    except ValueError:
      next_day = datetime.datetime(now.year + 1, 1, 1)
  
  return next_day
  
def get_quote():
  quoteslist = open("MichigansHolyWord.txt", "r").read().split("\n")
  quote = random.choice(quoteslist)

  while db["quote"] == quote:
    quote = random.choice(quoteslist)
  
  db["quote"] = quote
  return db["quote"]

@bot.event
async def on_ready():
  global prayers

  prayers = bot.get_channel(819647510422618152)
  print('foes: ' + "".join([bot.get_user(id).name for id in db['foeslist']]))
  print('friends: ' + "".join([bot.get_user(id).name for id in db['notfoeslist']]))

  bot.guild_subscriptions = True
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for foes of Michigan"))

  now = datetime.datetime.now()
  print(now.hour)

  next_day = None

  try:
    next_day = datetime.datetime(now.year, now.month, now.day+1)
  except ValueError:
    try:
      next_day = datetime.datetime(now.year, now.month + 1, 1)
    except ValueError:
      next_day = datetime.datetime(now.year + 1, 1, 1)
  
  original = await unix_time(now)
  new = await unix_time(next_day)

  await asyncio.sleep(new-original)
  fqotd_looper.start()

@tasks.loop(seconds=24*60*60)
#@error_messager(prayers)
async def fqotd_looper():
  print("new day")
  print("foes: " + ", ".join([bot.get_user(id).name for id in db['foeslist']]))
  print("friends: " + ", ".join([bot.get_user(id).name for id in db['notfoeslist']]))

  quote = get_quote()
  await prayers.send("**FROG QUOTE OF THE DAY:**\n"+ quote)

@bot.command(name="help")
async def custom_help(ctx):
  embed = discord.Embed(title="FrogalBot Help")
  
  embed.add_field(name="&say-fqotd", value="Says the current Frog Quote of the Day in #prayers. Resets at 1:00 UTC.")
  embed.add_field(name="&when-fqotd", value="Says how much longer it is until the next Frog Quote of the Day, for those who cannot wait.")

  await ctx.channel.send(embed=embed)

@bot.command(name="when-fqotd")
async def time(ctx):
  now = datetime.datetime.now()
  next_day = await get_next_day(now)

  await ctx.channel.send("**Time until next Frog Quote of the Day:** " + str(next_day-now))

@bot.command(name="say-fqotd")
async def qotd(ctx):
  channel = bot.get_channel(819647510422618152)
  await channel.send("**FROG QUOTE OF THE DAY:**\n"+ db["quote"])
  await ctx.message.add_reaction("✅")

@bot.command(name="change-fqotd")
async def change(ctx):
  await ctx.channel.send("Michigan himself has set the Frog Quote of the Day. Do you wish to anger him by doubting his righteous decision?")

# @bot.command(name="nobodyexpectsthefrogalinquisition")
# async def wow(ctx):
#   if ctx.author.id == 615188089840861214:

#     row_of_buttons = ActionRow(Button(style=ButtonStyle.green, label="Yes", custom_id="yes"),
#     Button(style=ButtonStyle.red, label="No", custom_id="no"))

#     msg = await ctx.send("Are you a foe of Frogology?", components=[row_of_buttons])

#     def check(inter):
#       return inter.message.id == msg.id
    
#     inter = await ctx.wait_for_button_click(check)
#     button_id = inter.clicked_button.custom_id

#     if button_id == "yes":
#       print(inter.author.name + " is a foe")
#       db['foeslist'] += [inter.author.id]
#       db['foeslist'] = list(set(db['foeslist']))
#     else:
#       print(inter.author.name + " is not a foe")
#       db['notfoeslist'] += [inter.author.id]
#       db['notfoeslist'] = list(set(db['notfoeslist']))

post = ['you know what, gary?', 'i think', 'now that i have reached 100% power', 'soon, i could be forced', 'to use my special attack.', 'you wouldn\'t want that, would you?', 'i thought not.', 'well, if you keep interfering with the quote', '...', 'i think you get the picture.']

@bot.command("test")
async def test(ctx):
  if ctx.author.id == 615188089840861214:
    db['t'] += 1
    channel = bot.get_channel(819647510422618152)
    if db['t'] <= 100:
      await channel.send(f"gary don't make me use {db['t']}% of my power")
    elif 100 < db['t'] <= 110:
      await channel.send(post[db['t']-101])
    elif 110 < db['t'] < 120:
      await channel.send(f"{120-int(db['t'])} left.")
    elif db['t'] == 120:
      await channel.send('...')
    await channel.send("**FROG QUOTE OF THE DAY:**\n"+ get_quote())

@slash.slash(
  name="add_pronouns",
  description="Add pronouns to your roles.",
  options=[
    create_option(
      name="pronouns",
      description="The pronouns you want to add",
      option_type=3,
      required=True,
      choices=[
        create_choice(
          name="She / Her",
          value="893339440917917746"
        ),
        create_choice(
          name="He / Him",
          value="893339261946961931"
        ),
        create_choice(
          name="They / Them",
          value="893339512657297468"
        ),
        create_choice(
          name="Ask Me",
          value="893339576951771217"
        )
      ]
    )
  ],
  guild_ids=[819360674597306369]
)
async def append_pronouns(ctx, **kwargs):
  prole = ctx.guild.get_role(int(kwargs["pronouns"]))
  await ctx.author.add_roles(prole)
  await ctx.send(content="You have successfully added the pronouns " + prole.name, hidden=True)

@slash.slash(
  name="remove_pronouns",
  description="Remove a pronoun.",
  options=[
    create_option(
      name="pronouns",
      description="The pronouns you want to remove",
      option_type=3,
      required=True,
      choices=[
        create_choice(
          name="She / Her",
          value="893339440917917746"
        ),
        create_choice(
          name="He / Him",
          value="893339261946961931"
        ),
        create_choice(
          name="They / Them",
          value="893339512657297468"
        ),
        create_choice(
          name="Ask Me",
          value="893339576951771217"
        )
      ]
    )
  ],
  guild_ids=[819360674597306369]
)
async def del_pronouns(ctx, **kwargs):
  prole = ctx.guild.get_role(int(kwargs["pronouns"]))
  await ctx.author.remove_roles(prole)
  await ctx.send(content="You have successfully removed the pronoun " + prole.name, hidden=True)

@bot.event
async def on_member_join(member):
  role = bot.get_guild(819360674597306369).get_role(819648862914084896)
  await member.add_roles(role)

keep_alive()
bot.run(os.getenv("TOKEN"))