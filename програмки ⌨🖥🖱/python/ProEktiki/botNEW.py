import discord
#import responses
import random 
import json
from discord.ext import commands
# from config import settings


# ---- подсказки

# /n - переход на новую строчку

# ----

# ---------------------------------------------------------------- <--импорты

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = '!', intents = intents)


# intents = discord.Intents(messages=True, guilds=True)           хз

# ---------------------------------------------------------------- <--префиксы и настройки
# client = discord.Client(intents=intents)



# ---------------------------------------------------------------- команды-->
@bot.command(aliases=["hfyljv56", "Рандом56"])
async def рандом56(ctx):
    await ctx.send(random.randint(1, 56))

@bot.command(aliases=[])
async def рандом_лс(ctx):
    await ctx.author.send(random.randint(1, 56))#ctx.author.send бот пишет в лс

@bot.command(aliases=[])
async def X56(ctx):
    await ctx.send("56"*556)

@bot.command(aliases=[])
async def прив(ctx):
    embed = discord.Embed(title = "Приветствие", description = "Ну прив пх", color = 7419530)
    await ctx.send(embed = embed)#короч текст в рамке где title оглавление а description текст а color цвет

# ---------------------------------------------------------------- казино -->
with open('persons.json') as json_file:
    data = json.load(json_file)

# money1 = data["moneyob"]
# print("Значение 'moneyob' из файла JSON:", money1)


@bot.command(aliases=["rfpbyj"])
async def казино(ctx, number = 1):
    number = int(number)

    if number == None:
        number = 1

    if number < 1: 
        embed = discord.Embed(description = (f"Невозможная ставка"), color = 7419530)
        await ctx.send(embed = embed)
        return
    
   

    if ctx.author.name not in data:
        data[ctx.author.name] = {}
        data[ctx.author.name]["money"] = 0
        data[ctx.author.name]["dolg"] = 0

    if number <= data[ctx.author.name]["money"]:
        number = number
    else: 
        embed = discord.Embed(description = (f"У вас не хватает денег для ставки..."), color = 7419530)
        await ctx.send(embed = embed)
        return
    
    Win = f"Вы выйграли!\n+{number} копейка"
    Lose = f"Вы проиграли...\n-{number} копейка"

    resultCaz = random.randint(0, 1)
    if resultCaz == 1:

        data[ctx.author.name]["money"] = data[ctx.author.name]["money"] + number

    else: data[ctx.author.name]["money"] = data[ctx.author.name]["money"] - number
    
    if data[ctx.author.name]["money"] < 0: 
        data[ctx.author.name]["money"] = 0

    if resultCaz == 0:
        resultCaz = Lose
    else: resultCaz = Win
    embed = discord.Embed(title = resultCaz, description = (f"у вас {data[ctx.author.name]['money']} копеек"), color = 7419530)
    await ctx.send(embed = embed)

    print(ctx.author.name)


@bot.command(aliases=[])
async def сост(ctx):
    embed = discord.Embed(description = (f"Ваше состояние в данный момент: {data[ctx.author.name]['money']} копеек"), color = 7419530)
    await ctx.send(embed = embed)

@bot.command(aliases=[])
async def сост_долг(ctx):
    embed = discord.Embed(description = (f"Ваш долг: {data[ctx.author.name]['dolg']} копеек"), color = 7419530)
    await ctx.send(embed = embed)
    

@bot.command(aliases=[])
async def дай(ctx):
    if data[ctx.author.name]["money"] == 0:
        embed = discord.Embed(description = (f"Вам перечилили 1 копейку"), color = 7419530)
        await ctx.send(embed = embed)

        data[ctx.author.name]["money"] = data[ctx.author.name]["money"] + 1
    

@bot.command(aliases=["vecjh"])
async def мусор(ctx):
    resultMus = 0
    resultMus = random.randint(1, 100)

    if 1 <= resultMus <= 60: 
        data[ctx.author.name]["money"] = data[ctx.author.name]["money"] + 0
        embed = discord.Embed(title = (f"Вы ничего не нашли ("), description = (f"у вас {data[ctx.author.name]['money']} копеек"), color = 7419530)
        await ctx.send(embed = embed)
    if 61 <= resultMus <= 90: 
        data[ctx.author.name]["money"] = data[ctx.author.name]["money"] + 1
        embed = discord.Embed(title = (f"Вы нашли 1 копейку!"), description = (f"у вас {data[ctx.author.name]['money']} копеек"), color = 7419530)
        await ctx.send(embed = embed)
    if 91 <= resultMus <= 93: 
        data[ctx.author.name]["money"] = data[ctx.author.name]["money"] + 56
        embed = discord.Embed(title = (f"Вы нашли 56 копеек!"), description = (f"у вас {data[ctx.author.name]['money']} копеек"), color = 7419530)
        await ctx.send(embed = embed)
    if 94 <= resultMus <= 95: 
        data[ctx.author.name]["money"] = data[ctx.author.name]["money"] + 156
        embed = discord.Embed(title = (f"Вы нашли 156 копеек!!!"), description = (f"у вас {data[ctx.author.name]['money']} копеек"), color = 7419530)
        await ctx.send(embed = embed)

    if 96 <= resultMus <= 97: 
        data[ctx.author.name]["money"] = data[ctx.author.name]["money"] - 10
        embed = discord.Embed(title = (f"Вы заболели и потратили на лечение 10 копеек..."), description = (f"у вас {data[ctx.author.name]['money']} копеек"), color = 7419530)
        await ctx.send(embed = embed)
    if 98 <= resultMus <= 99: 
        data[ctx.author.name]["money"] = data[ctx.author.name]["money"] - 30
        embed = discord.Embed(title = (f"Вы заболели и потратили на лечение 30 копеек..."), description = (f"у вас {data[ctx.author.name]['money']} копеек"), color = 7419530)
        await ctx.send(embed = embed)
    if resultMus == 100: 
        data[ctx.author.name]["money"] = data[ctx.author.name]["money"] - 56
        embed = discord.Embed(title = (f"Вы заболели и потратили на лечение 56 копеек..."), description = (f"у вас {data[ctx.author.name]['money']} копеек"), color = 7419530)
        await ctx.send(embed = embed)

        
@bot.command(aliases=["rhtlbn"])
async def кредит(ctx):


    data[ctx.author.name]["dolg"] = data[ctx.author.name]["dolg"] - data[ctx.author.name]["money"]
    data[ctx.author.name]["money"] = 0    
    embed = discord.Embed(title = (f"Вы взяли кредит"), description = (f"у вас {data[ctx.author.name]['money']} копеек"), color = 7419530)
    await ctx.send(embed = embed)

# ------
    with open('persons.json', 'w') as file:
            json.dump(data, file)
# ----------------------------------------------------------------

# @bot.command(aliases=[])
# async def chunk1(ctx):
#     await ctx.Guild.chunk()           не работает

# @bot.group()
# async def cool(ctx):
#     """Says if a user is cool.

#     In reality this just checks if a subcommand is being invoked.
#     """
#     if ctx.invoked_subcommand is None:
#         await ctx.send(f'No, {ctx.subcommand_passed} is not cool')            хз
    

@bot.command(aliases = ['byaf'])#всякая инфа сервера в f строке
async def инфа(ctx):
    guild = ctx.guild

    img = "https://cdn.discordapp.com/attachments/869688522276229178/1150887061755277312/1676306116_foni-club-p-oboi-na-aifon-v-stile-kiberpank-37.png"

    emb = discord.Embed(title = "Информация", description = "Тут описание сервера...", color = 7419530)
    emb.add_field(name = "Владелец", value = guild.owner, inline = False) #inline = False значит с новой строки(если во всех то в строчку)
    emb.add_field(name = "ID Владельца:", value = guild.owner_id, inline = False)
    emb.add_field(name = "Сервер создан:", value = guild.created_at, inline = False)#field добавляет поле в эконом
    emb.add_field(name = "Количество всех каналов:", value = len(guild.channels), inline = False)#len обязаловка для считывания
    emb.add_field(name = "Количество войсов:", value = len(guild.voice_channels), inline = False)
    emb.add_field(name = "Количество участников:", value = len(guild.members), inline = False)
    emb.add_field(name = "Участники с бустом:", value = len(guild.premium_subscribers), inline = False)
    emb.add_field(name = "Уровень mfa:", value = guild.mfa_level, inline = False)

    emb.add_field(name = "Количество эмоджи:", value = len(guild.emojis), inline = False)
    #print(guild.emojis)#все эмоджи в терминал
    emb.set_thumbnail(url = guild.icon.url)#изображение в эмбэд с сылкой через url
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)#сверху аватар отправителя и его имя(можно вместо этого ввести любое имя)
    emb.set_footer(text = f"Команду осуществил: {bot.user.name}", icon_url = bot.user.avatar.url)#то что снизу написанно(бот и профиль и тд)
    emb.set_image(url = img)#дисплей с фотки img введённой сверху
    #emb.add_field(name = "Эмоджи:", value = emj[:100], inline = False)#100 ограничение 

    await ctx.send(embed = emb)    

@bot.hybrid_command(description = "Мега имба")#то что будет написано при выборе слеша
async def имба(ctx):
    await ctx.send("Имба")


@bot.command(aliases=["jakfqy"])
async def офлайн(ctx):
    img2 = "https://images-ext-1.discordapp.net/external/UGmQnzKdsl6Rte6R8xj1StE_0jmNp7jDhmRIEXn-Hek/https/media.tenor.com/4fDTwoJ8Aq8AAAPo/botoffline-sublime.mp4"
    embed = discord.Embed(description = (img2), color = 7419530)
    await ctx.send(embed = embed) #на доработку
        

# ----------------------------------------------------------------

# .....






# ---------------------------------------------------------------- для запуска-->
@bot.event
async def on_ready():
    await bot.tree.sync()#обновляет варианты выбора команды при вводе слеша
    print(f'{bot.user} --> Бот запущен!')

if __name__ == '__main__':
    bot.run('MTE0NzYwMTIyMjMyOTcxMjc0Mg.GQU-_R.T8GOH9bVRa1SZgBIvr1E0611799_8-PmTvNMsY')
