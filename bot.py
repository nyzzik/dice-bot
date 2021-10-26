import discord
from discord.ext import commands
import random
import re

# intents = discord.Intents.default()
# intents.members = True

bot = commands.Bot(command_prefix='oswald-')


@bot.event
async def on_ready():
    print("logged")


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if(message.guild.get_role(859632248789139456) in message.author.roles):
        print(re.match("[r]\d[d]\d", message.content), message.content)
        if re.match("[r]\d[d]\d", message.content):
            await dice_roll(message, message.content[1:])


@bot.command(aliases=['r'])
async def roll(ctx, dice: str):
    lower = False
    higher = False
    check = False
    try:
        rolls, rest = dice.split('d')
        rolls = int(rolls)

        if 'kh' not in rest and 'kl' not in rest:
            limit = int(rest)
        if "kh" in rest:
            check = True
            print('lowered')
            limit, rest = map(int, rest.split('kh'))
            print(limit, rest)
            if rest > limit:
                raise(Exception)

            higher = True
        print('done')
        if not check:
            if "kl" in rest:
                print('highered')

                limit, rest = map(int, rest.split('kl'))
                if rest > limit:
                    raise(Exception)

                lower = True

    except Exception:
        await ctx.send('Format has to be in NdN')
        return
    results = [random.randint(1, limit) for r in range(rolls)]
    result_log = results[:]
    removed = []
    if lower:
        for x in range(rolls-rest):
            removed.append(results.remove(max(results)))

    if higher:
        for x in range(rolls-rest):
            removed.append(results.remove(min(results)))

    result_string = ""
    for result in results:
        result_string += " " + str(result) + '+'

    result_string = result_string[:-1]

    hl = (f'{rest}' + (' highest ' if higher else ' lowest ') +
          f"roll(s):{result_string} ")
    hl = hl if (higher or lower) else ""

    embed = discord.Embed(title=f"{dice} rolls by {ctx.author}",
                          description=f'{hl} SUM: {sum(results)}')
    count = 1
    for result in result_log:
        embed.add_field(name=f'Roll #{count}', value=result)
        count += 1

    await ctx.send(embed=embed)


async def dice_roll(msg, dice: str):
    lower = False
    higher = False
    check = False
    try:
        rolls, rest = dice.split('d')
        rolls = int(rolls)

        if 'kh' not in rest and 'kl' not in rest:
            limit = int(rest)
        if "kh" in rest:
            check = True
            print('lowered')
            limit, rest = map(int, rest.split('kh'))
            print(limit, rest)
            if rest > limit:
                raise(Exception)

            higher = True
        print('done')
        if not check:
            if "kl" in rest:
                print('highered')

                limit, rest = map(int, rest.split('kl'))
                if rest > limit:
                    raise(Exception)

                lower = True

    except Exception:
        await msg.channel.send('Format has to be in NdN')
        return
    results = [random.randint(1, limit) for r in range(rolls)]
    result_log = results[:]
    removed = []
    if lower:
        for x in range(rolls-rest):
            removed.append(results.remove(max(results)))

    if higher:
        for x in range(rolls-rest):
            removed.append(results.remove(min(results)))

    result_string = ""
    for result in results:
        result_string += " " + str(result) + '+'

    result_string = result_string[:-1]

    hl = (f'{rest}' + (' highest ' if higher else ' lowest ') +
          f"roll(s):{result_string} ")
    hl = hl if (higher or lower) else ""

    embed = discord.Embed(title=f"{dice} rolls by {msg.author}",
                          description=f'{hl} SUM: {sum(results)}')
    count = 1
    for result in result_log:
        embed.add_field(name=f'Roll #{count}', value=result)
        count += 1

    await msg.channel.send(embed=embed)

bot.run('token.token')
