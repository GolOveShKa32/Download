import datetime
import discord
import requests
from bs4 import BeautifulSoup
from threading import Thread
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from youtube_dl import YoutubeDL
from Online import Online
import asyncio
import youtube

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

GL_ADMINS = {
    418268464097001474, # GolOveShKa32
}

OFFLINE = {}

WARN_LIST = {}

BAN_LIST = {}

ROOMS = {}

SPAM = {}

PLAYER = ''

PREFIX = '+'


intents = discord.Intents.all()
#intents.members = True
#intents.presences = True
#intents.reactions = True

client = commands.Bot(intents = intents, command_prefix = PREFIX)
client.remove_command('help')


@client.event
async def on_connect():
    print('Bot Connected')
    online.start()
    room_timer.start()


# Выдача роли при входе на сервер
@client.event
async def on_member_join(member: discord.Member):
    role = discord.utils.get(member.guild.roles, name = 'Шиноби')
    await member.add_roles(role)

'''
# проверка сообщений (Анти-спам)
@client.event
async def on_message(message):
    author = message.author.id

    if author in SPAM:
        mes = SPAM[author]['mes'] + 1
        t = SPAM[author]['time']

        SPAM[author] = {"mes": mes, "time": t}
        
        if time("second") - 4 >= t:
            SPAM.pop(author)
        
        elif mes >= 5:
            if author in SPAM:
                SPAM.pop(author)

            await message.channel.send(f'{message.author.mention}, вам выдано предупреждение за спам!')

    else:
        mes = 0
        SPAM[author] = {"mes": mes, "time": time('second')}
'''

# Авто запись в бан лист
@client.event
async def on_member_ban(guild, user):
    time = datetime.datetime.now()
    data = f"{time.day}.{time.month}.{time.year}"

    BAN_LIST[user.name] = data


# Авто удаление из бан листа
@client.event
async def on_member_unban(guild, user):
    if(user.name in BAN_LIST):
        BAN_LIST.pop(user.name)


# Нажатия на эмодзи
@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = discord.utils.get(message.guild.members, id = payload.user_id)
    voice = get(client.voice_clients, guild = message.guild)
    
    try:
        if not member.bot:
            emoji = str(payload.emoji)

            if message.id == PLAYER.id:
                await message.remove_reaction(payload.emoji, member)

                if emoji == "⏮":
                    await back(channel)
                
                elif emoji == "⏯":
                    if voice.is_playing():
                        voice.pause()
                    else:
                        voice.resume()

                elif emoji == "🔄":
                    await replay(channel)
                
                elif emoji == "⏭":
                    await next(channel)
    except:
        pass

@client.event
async def on_raw_reaction_remove(payload):
    pass


# Сообщение всем участникам в лс
@client.command()
async def spam(ctx, text):
    if(ctx.message.author.id in GL_ADMINS):
        if(ctx.message.author.name):
            await ctx.message.channel.purge(limit = 1)
            for member in ctx.message.guild.members:
                print(member)
                try:
                    users = client.get_user(member.id)
                    await users.send(text)
                    print(users)
                except:
                    print(f"{users} - БОТ")
        else:
            await ctx.send('У вас нет доступа к этой команде')


# Warn
@client.command()
async def warn(ctx, member: discord.Member, reason = None):
    if(ctx.message.author.name):
        if(ctx.message.author.id in GL_ADMINS):
            if member.name in WARN_LIST:
                warn = WARN_LIST[member.name]

                if warn == 2:
                    WARN_LIST.pop(member.name)
                    await ctx.send(f'{member.mention} выдан бан на 3 дня')
                    await member.send(f'{member.mention}, вам выдан бан на 3 дня')
                    await member.ban(reason)

                else:
                    await ctx.send(f'У {member.mention} второе предупреждение')
                    WARN_LIST[member.name] += 1

            else:
                WARN_LIST[member.name] = 1
                await ctx.send(f'У {member.mention} первое предупреждение')

        else:
            await ctx.send('У вас нет доступа к этой команде')


# Warn лист
@client.command()
async def warn_list(ctx):
    value = '-------------------------'
    emb = discord.Embed(title = 'Warn лист')

    if WARN_LIST:
        for nick in WARN_LIST:
            num = WARN_LIST[nick]
            name = f'{nick} - {num} ПРЕД.'
            emb.add_field(name = name, value = value, inline=False)
        await ctx.send(embed = emb)

    else:
        await ctx.send('Warn лист пуст')


# Бан лист
@client.command()
async def ban_list(ctx):
    value = '-------------------------'
    emb = discord.Embed(title = 'Бан лист')

    if BAN_LIST:
        for nick in BAN_LIST:
            name = f'{nick} - {BAN_LIST[nick]}'
            emb.add_field(name = name, value = value, inline=False)
        await ctx.send(embed = emb)

    else:
        await ctx.send('Бан лист пуст')


# МУТ
@client.command()
async def mute(ctx, member: discord.Member):
    if(ctx.message.author.name):
        mute_role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
        await member.add_roles(mute_role)
        await ctx.send(f'Участнику {member.mention}, выдан МУТ за нарушение правил!')
    else:
        await ctx.send('У вас нет доступа к этой команде')


# Отчистка чата
@client.command()
async def clear(ctx, amount = 100):
    if(ctx.message.author.name):
        await ctx.channel.purge(limit = amount + 1)


# МУЗЫКА
@client.command()
async def play(ctx, url=None, *args):
    global track
    global track_num

    voice = get(client.voice_clients, guild = ctx.guild)

    if not url and voice and voice.is_paused():
        voice.resume()
        return

    if not url:
        voice.stop()

    try:
        channel = ctx.message.author.voice.channel

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
    except: pass

    for x in args:
        url += x + ' '

    if "http" in url:
        track_num = 0
        try: listId = url.split('list=')[1].split('&')
        except: listId = None

        if listId:
            track = youtube.playlistIds(listId[0])
        else:
            track = url
    else:
        track = youtube.search(url)
    
    if voice.is_playing():
        voice.pause()

    if type(track) == list:
        voice.play(discord.FFmpegPCMAudio(music(track[track_num]), **FFMPEG_OPTIONS), after=lambda x: play_error(voice))
        await player(ctx)
    else:
        voice.play(discord.FFmpegPCMAudio(music(track), **FFMPEG_OPTIONS))

@client.command()
async def playlist(ctx, *args):
    global track
    global track_num

    name = ""
    track = []
    track_num = -1
    channel = get(ctx.guild.channels, name="плейлист-музыка")
    
    for x in args:
        name += x + ' '
    
    async for message in channel.history(limit = 1000):
        msg = message.content.splitlines()

        if name[:-1] == msg[0][1:-1]:
            for trek in msg[1:]:

                if "http" in trek:
                    try: listId = trek.split('list=')[1].split('&')
                    except: listId = None

                    if listId:
                        track.extend(youtube.playlistIds(listId[0]))
                    else:
                        track.append(trek)
                else:
                    track.append(youtube.search(trek))

                if len(track) == 1:
                    try:
                        channel = ctx.message.author.voice.channel
                        voice = get(client.voice_clients, guild = ctx.guild)

                        if voice and voice.is_connected():
                            await voice.move_to(channel)
                        else:
                            voice = await channel.connect()
                    except: pass

                    channel = ctx.message.author.voice.channel
                    voice = get(client.voice_clients, guild = ctx.guild)
                    
                    if voice.is_playing():
                        voice.pause()
                    
                    play_error(voice)
                    await player(ctx)
                    Thread(target=ListMusic, args=(msg,)).start()
                break

@client.command()
async def replay(ctx):
    try:
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild = ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
    except: pass

    if track:
        voice.play(discord.FFmpegPCMAudio(music(track)))

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice.is_playing():
        voice.pause()

@client.command()
async def stop(ctx):
    try:
        voice = get(client.voice_clients, guild = ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()

    except: pass

@client.command()
async def next(ctx):
    if type(track) == list:
        voice = get(client.voice_clients, guild = ctx.guild)
        voice.stop()


async def back(ctx):
    global track_num

    if type(track) == list:
        if track_num-2 >= -1:
            track_num -= 2
        voice = get(client.voice_clients, guild = ctx.guild)
        voice.stop()

@client.command()
async def radio(ctx, url):
    voice = get(client.voice_clients, guild = ctx.guild)

    try:
        channel = ctx.message.author.voice.channel

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
    except: pass

    voice.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))

async def player(ctx):
    global PLAYER
    
    message = await ctx.send("Плеер в разработке. (>_<)")

    try: await PLAYER.delete()
    except: pass
    
    PLAYER = message

    for emoji in "⏮⏯🔄⏭":
        await message.add_reaction(emoji)

def music(url):
    with YoutubeDL() as ydl:
        ydl_info = ydl.extract_info(url, download=False)
        return ydl_info['formats'][0]['url']

def play_error(voice):
    global track_num

    if type(track) == list and len(track) > track_num and voice.is_connected():
        track_num += 1
        try: voice.play(discord.FFmpegPCMAudio(music(track[track_num]), **FFMPEG_OPTIONS), after=lambda x: play_error(voice))
        except: play_error(voice)


def ListMusic(msg):
    global track
    trek = []

    for trek in msg[2:]:
        if "http" in trek:
            try: listId = trek.split('list=')[1].split('&')
            except: listId = None

            if listId:
                track.extend(youtube.playlistIds(listId[0]))
            else:
                track.append(trek)
        else:
            track.append(youtube.search(trek))


# Онлайн
@client.command()
async def G_ONLINE_G(ctx):
    if(ctx.message.author.id in GL_ADMINS):
        value = '-------------------------'
        emb = discord.Embed(title = 'Онлайн лист')
        
        for name in OFFLINE:
            emb.add_field(name = name, value = value, inline = False)

        await ctx.channel.purge(limit = 1)
        mes = await ctx.send(embed = emb)
        Online[mes.id] = mes.channel.id

        f = open("Online.py", "w")
        f.write(f"Online={Online}")
        f.close()


# Учасников ко мне
@client.command()
async def me(ctx):
    for channel in ctx.guild.voice_channels:
        for member in channel.members:
            await member.move_to(ctx.author.voice.channel)


# Учасников в канал
@client.command()
async def to(ctx, vc: int):
    for member in ctx.author.voice.channel.members:
        await member.move_to(ctx.guild.voice_channels[vc-1])


# Временный голосовой чат
@client.command()
async def room(ctx, name, limit = None, private = None):
    if ctx.guild.id in ROOMS:
        if len(ROOMS[ctx.guild.id]) >= 5:
            return
    else:
        ROOMS[ctx.guild.id] = []

    channel = await ctx.guild.create_voice_channel(name = name, user_limit = limit)
    
    ROOMS[ctx.guild.id].append({'id': channel.id, 'name': channel.name, 'time': time('minute')})

    await channel.set_permissions(ctx.message.author, connect = True, mute_members = True, move_members = True, manage_channels = True)
    
    if private == "p":
        await channel.set_permissions(ctx.guild.default_role, connect = False, manage_channels = False)

def time(time = None):
    def supe():
        r = requests.get("https://www.timeserver.ru/cities/ru/chelyabinsk")
        return BeautifulSoup(r.text, "lxml")
    
    def second():
        return supe().find_all(class_ = "seconds")[0].text

    def minute():
        return supe().find_all(class_ = 'minutes')[0].text
    
    def hour():
        return supe().find_all(class_ = 'hours')[0].text
    
    if time == "hour": return int(hour())
    elif time == "minute": return int(minute())
    elif time == "second": return int(second())
    else: return hour() +":"+ minute()


# Обновление сообщения команды: online
@tasks.loop(seconds = 1)
async def online():

    try:
        from Online import Online
    except:
        pass
    
    if not Online:
        return

    for id in list(Online):
        try:
            channel = client.get_channel(id=Online[id])
            ctx = await channel.fetch_message(id)
            now = datetime.datetime.now()
        except:
            Online.pop(id)

    try:
        if now != datetime.datetime.now():
            now = datetime.datetime.now()

            value = '-------------------------'
            emb = discord.Embed(title = 'Онлайн лист', color = discord.Color.from_rgb(0,200,0))

            for member in ctx.guild.members:
                if str(member.status) != 'offline':
                    message = f"{member.name} - Online"
                    emb.add_field(name = message, value = value, inline = False)

                    if member.name in OFFLINE:
                        OFFLINE.pop(member.name)

                elif member.name not in OFFLINE:
                    OFFLINE[member.name] = f"{time()} / {now.day}.{now.month}.{now.year}"

            
            for member in OFFLINE:
                message = f"{member} - {OFFLINE[member]}"
                emb.add_field(name = message, value = value, inline = False)

            await ctx.edit(embed = emb)
    except:
        pass


# Авто удаление временных голосовых каналов
@tasks.loop(seconds = 5)
async def room_timer():
    for id in ROOMS:
        for room in ROOMS[id]:
            channel = client.get_channel(id=room['id'])

            if channel:
                if channel.members:
                    room['time'] = int(time('minute'))
                else:
                    if room['time'] == time('minute')-2:
                        await channel.delete()
            else:
                ROOMS[id].remove(room)


# Помощь по командам
@client.command()
async def help(ctx):
    emb = discord.Embed(title = 'Навигация по командам')

    emb.add_field(name = '{}play'.format(PREFIX), value = 'Включить музыку', inline=False)
    emb.add_field(name = '{}replay'.format(PREFIX), value = 'Повторить трек', inline=False)
    emb.add_field(name = '{}pause'.format(PREFIX), value = 'Остановить музыку', inline=False)
    emb.add_field(name = '{}stop'.format(PREFIX), value = 'Отключить бота от канала', inline=False)
    emb.add_field(name = '{}spam'.format(PREFIX), value = 'Сообщение в лс учасникам сервера', inline=False)
    emb.add_field(name = '{}warn'.format(PREFIX), value = 'Предупреждение', inline=False)
    emb.add_field(name = '{}warn_list'.format(PREFIX), value = 'Warn Лист', inline=False)
    emb.add_field(name = '{}ban_list'.format(PREFIX), value = 'Бан лист', inline=False)
    emb.add_field(name = '{}clear'.format(PREFIX), value = 'Отчистка чата', inline=False)
    emb.add_field(name = '{}mute'.format(PREFIX), value = 'Мут', inline=False)

    await ctx.send(embed = emb)


client.run('NzAyMTg1MzM1MDg5NjU5OTA1.GgKyTz.SF0NyfMuDegPVE1ocB2xKXAy1XrFBOd1BZeYeg')