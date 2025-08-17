import discord
#import responses
import random 
#import json
from discord.ext import commands
from config import settings



    


intents = discord.Intents().all()
bot = commands.Bot(command_prefix = '!', intents = intents)


@bot.command()
async def прив(ctx):
    embed = discord.Embed(title = "Приветствие", description = "Ну прив пх", color = 7419530)
    await ctx.send(embed = embed)#короч текст в рамке где title оглавление а description текст а color цвет


@bot.command(aliases=['denlog'])#<-aliases = другие обозначения через запятую(эта команда)
async def hello(ctx):#ctx принимает из канала с сообщением(всё из канала)
    await ctx.send(f'Hello, {ctx.author.mention}!')
    

@bot.command(aliases=[])
async def рандом(ctx):
    await ctx.send(random.randint(1, 56))

@bot.command()
async def созд_кан(ctx, name):
    guild = ctx.guild #встака для экономии с приёмом сообщения(ОБЗОР ВАЛЕРЫ!)
    await guild.create_text_channel(name)


@bot.command(aliases=[])
async def рандом_лс(ctx):
    await ctx.author.send(random.randint(1, 56))#ctx.author.send бот пишет в лс


@bot.event
async def on_message(message):#on_message просто без префикса текста в данном случае, И В ЭТОТ МЕССЕДЖ МОЖНО ВСЁ ВВОДИТЬ, НЕ CОЗДАВАТЬ НОВЫЙ!
    #print(message.content)#убрать (#) что бы считывать всю инфу что ввели в чате
    ctx = message.content.lower()
    if ctx == 'hello':
        await message.channel.send('hi')

    await bot.process_commands(message)





@bot.command()
async def канал(ctx, cid):
    cid = cid[2:]#срез с числа не 0 не 1 а 2 -> после второго символа берётся
    cid = cid[:(len(cid) - 1)]#а тут срез последнего символа после преврощения в 01234 и тд
    channel = bot.get_channel(int(cid))#берёт тобой вписанный id канала или имя и пишет туда по факту чел
    await channel.send("Это канал!")
    
    #p_cid = cid.copy()
    #for i in cid:
    #if i in ["<", "#", ">"]:
        #del p_cid[i]    #<-это без срезов( там нельзя вроде как в строке удалять по индексу)



@bot.command()
async def канал_имя(ctx, cid, name):
    cid = cid[2:]
    cid = cid[:(len(cid) - 1)]
    channel = bot.get_channel(int(cid))
    await channel.edit(name = name)#это всё меняет имя канала который выберешь(команда,имя в (#),новое имя



@bot.command(aliases = ['byaf'])#всякая инфа сервера в f строке
async def инфа(ctx):
    guild = ctx.guild

    #emj = ""
    #for i in guild.emojis:
        #emj += f"<:{i.name}:{i.id}>"

 ## emj += f"<:{i.name}:{i.id}>" --- <:emoji_50:1118040582598701176>  = :emoji_50:(то что надо пнг)
    
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


#    text =f'''   #вариант через f строку
#Владелец: {guild.owner}
#Сервер создан: {guild.created_at}
#Количество всех каналов:{len(guild.channels)} 
#Количество участников: {len(guild.members)}

#Иконка:{guild.icon_url}
#'''
#    await ctx.send(text)
##рамочка добавится через ``` ```

@bot.hybrid_command(description = "Мега имба")#то что будет написано при выборе слеша
async def имба(ctx):
    await ctx.send("Имба")

@bot.command()
async def войс(ctx):
    channel = bot.get_channel(869688522469154912)
    await channel.connect()

@bot.command()
async def лив(ctx):
    await ctx.guild.voice_client.disconnect()

@bot.hybrid_command(description = "Играть музыку")#!войс, !играть
async def играть(ctx, name):
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    audio_source = discord.FFmpegPCMAudio(executable = "D:/ffmpeg-6.0-essentials_build/ffmpeg-6.0-essentials_build/bin/ffmpeg.exe", source = name )#"D:/ffmpeg-6.0-essentials_build/HyperSonic.mp3")#поменять на ссылку на мп3
    voice_client.play(audio_source, after=None)#тут был await

@bot.hybrid_command(description = "Играть музыку")#!войс, !играть, !стоп
async def стоп(ctx):
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice_client.stop()

@bot.event
async def on_ready():
    await bot.tree.sync()#обновляет варианты выбора команды при вводе слеша
    print(f'{bot.user}Бот запущен!')

if __name__ == '__main__':
    bot.run('MTE0NzYwMTIyMjMyOTcxMjc0Mg.GQU-_R.T8GOH9bVRa1SZgBIvr1E0611799_8-PmTvNMsY')









