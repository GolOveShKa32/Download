import datetime
import discord
from threading import Thread
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from fuzzywuzzy import fuzz

import YouTube
import Net

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

VA_CMD_LIST = {
    'play': ('play', 'p', 'здфн'),
    'playlist': ('playlist', 'здфн_дшые'),
    'pause': ('pause', 'зфгыу'),
    'replay': ('replay', 'куздфн'),
    'stop': ('stop', 'ыещз'),
    'next': ('next', 'туче'),
    'back': ('back', 'ифсл'),
    'radio': ('radio', 'кфвшщ'),
    'room': ('room',),
    'me': ('me',),
    'to': ('to',),
    'warn_list': ('warn_list', 'цфкт_дшые'),
    'warn': ('warn', 'цфкт'),
    'ban_list': ('ban_list', 'ифт_дшые'),
    'clear': ('clear',),
    'mute': ('mute', 'ьгеу'),
    'G_ONLINE_G': ('G_ONLINE_G',)
}

I = 418268464097001474
PREFIX = '-'

intents = discord.Intents.all()

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


# Авто запись в бан лист
@client.event
async def on_member_ban(guild, user):
    time = datetime.datetime.now()
    data = f"{time.day}.{time.month}.{time.year}"

    Ban_List = Net.Get(f"id{guild.id}", "ban", "json")
    Ban_List[user.name] = data

    Net.Set(f"id{guild.id}", "ban", Ban_List, "json")


# Авто удаление из бан листа
@client.event
async def on_member_unban(guild, user):
    Ban_List = Net.Get(f"id{guild.id}", "ban", "json")

    if(user.name in Ban_List):
        Ban_List.pop(user.name)
        Net.Set(f"id{guild.id}", "ban", Ban_List, "json")


@client.event
async def on_message(ctx):
    if not ctx.author.bot:
        if PREFIX not in ctx.content[0]:
            return
        
        CMD = ctx.content.split()[0][1:]
        params = ctx.content.replace(ctx.content.split()[0], '')
        cmd = ''

        for c, v in VA_CMD_LIST.items():
            for x in v:
                vrt = fuzz.ratio(CMD, x)
                print(CMD, x, vrt)
                if vrt >= 85:
                    cmd = c
        

        if cmd == 'play':
            await play(ctx, params)

        elif cmd == 'playlist':
            await playlist(ctx, params)

        elif cmd == 'pause':
            await pause(ctx)

        elif cmd == 'replay':
            await replay(ctx)

        elif cmd == 'stop':
            await stop(ctx)
        
        elif cmd == 'next':
            await next(ctx)
        
        elif cmd == 'back':
            await back(ctx)

        elif cmd == 'radio':
            await stop(ctx)

        elif cmd == 'room':
            await room(ctx, params)
        
        elif cmd == 'me':
            await me(ctx)

        elif cmd == 'to':
            await to(ctx)

        elif cmd == 'warn_list':
            await warn_list(ctx)

        elif cmd == 'warn':
            await warn(ctx, ctx.mentions[0])

        elif cmd == 'ban_list':
            await ban_list(ctx)

        elif cmd == 'clear':
            await clear(ctx, int(params))

        elif cmd == 'mute':
            await mute(ctx, ctx.mentions[0])
        
        elif cmd == 'G_ONLINE_G':
            await G_ONLINE_G(ctx)


# МУЗЫКА
async def play(ctx, url, check=True):
    global track
    global track_num

    voice = get(client.voice_clients, guild = ctx.guild)

    if not url and voice and voice.is_paused():
        voice.resume()
        return
    
    channel = ctx.author.voice.channel

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    track, info = YouTube.music(url, check)
    
    if voice.is_playing():
        voice.pause()

    if type(track) == list:
        voice.play(discord.FFmpegPCMAudio(track[track_num], **FFMPEG_OPTIONS), after=lambda x: next(voice))
    else:
        voice.play(discord.FFmpegPCMAudio(track, **FFMPEG_OPTIONS))

    await player(ctx, info)


async def playlist(ctx, params):
    global track
    global track_num

    params = params.split()
    name = params[0]

    if len(params) == 2: num = int(params[1])
    else: num = 1

    track = []
    track_num = num-1
    channel = get(ctx.guild.channels, name="плейлист-музыка")
    
    async for message in channel.history(limit = 1000):
        msg = message.content.splitlines()

        if name == msg[0][1:-1]:
            await play(ctx, list(msg[num]), False)
            Thread(target=ListMusic, args=(msg,)).start()


def ListMusic(msg):
    global track
    track = []

    for trek in msg[1:]:
        if type(YouTube.music(trek)[0]) == list:
            track.extend(YouTube.music(trek)) 
        else:
            track.append(YouTube.music(trek))


async def replay(ctx):
    if track:
        await play(ctx, track, False)


async def pause(ctx):
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice.is_playing():
        voice.pause()


async def stop(ctx):
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()


async def next(ctx):
    global track
    global track_num

    if type(track) == list:
        if track_num+1 < len(track):
            track_num += 1
            await play(ctx, track, False)


async def back(ctx):
    global track
    global track_num

    if type(track) == list:
        if track_num > 0:
            track_num -= 1
            await play(ctx, track, False)


"""
async def radio(ctx, url):
    voice = get(client.voice_clients, guild = ctx.guild)

    try:
        channel = ctx.author.voice

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
    except: pass

    voice.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
"""


# PLAYER
async def player(ctx, info):
    global PLAYER

    emb = discord.Embed(
        title = info['title'],
        description="Длительность: ",
        url="https://disnake.dev/assets/disnake-logo.png",
        color=discord.Colour.yellow())

    emb.set_author(
        name="Embed Author",
        url="https://disnake.dev/",
        icon_url="https://disnake.dev/assets/disnake-logo.png")
    
    emb.set_thumbnail(url=info['img'])

    message = await ctx.channel.send(embed = emb)

    try: await PLAYER.delete()
    except: pass
    
    PLAYER = message


# Отчистка чата
async def clear(ctx, amount = 100):
    if ctx.author.name:
        await ctx.channel.purge(limit = amount + 1)


# Учасников ко мне
async def me(ctx):
    for channel in ctx.guild.voice_channels:
        for member in channel.members:
            await member.move_to(ctx.author.voice.channel)


# Учасников в канал
async def to(ctx, vc: int):
    for member in ctx.author.voice.channel.members:
        await member.move_to(ctx.guild.voice_channels[vc-1])


def IsAdmin(l1, l2):
    for x in l2:
        if x in l1:
            return True
    return False


# Warn
async def warn(ctx, member):
    if ctx.author.name:
        if IsAdmin(ctx.author.roles, Net.Get(f"id{ctx.guild.id}", "admin_roles", "json")) or ctx.author.id == I:
            WarnList = Net.Get(f"id{ctx.guild.id}", "warn", "json")

            if member.name in WarnList:
                WarnList[member.name] = WarnList[member.name] + 1
            else:
                WarnList[member.name] = 1

            Net.Set(f"id{ctx.guild.id}", "warn", WarnList, "json")
            
            await ctx.channel.send(f"У {member.mention} {WarnList[member.name]}-е предупреждение")

        else:
            await ctx.channel.send('У вас нет доступа к этой команде')


# Warn лист
async def warn_list(ctx):
    value = '-------------------------'
    emb = discord.Embed(title = 'Warn лист')
    WarnList = Net.Get(f"id{ctx.guild.id}", "warn", "json")

    if WarnList:
        for nick in WarnList:
            num = WarnList[nick]
            name = f'{nick} - {num} ПРЕД.'
            emb.add_field(name = name, value = value, inline=False)
        await ctx.channel.send(embed = emb)

    else:
        await ctx.channel.send('Warn лист пуст')


# Бан лист
async def ban_list(ctx):
    value = '-------------------------'
    emb = discord.Embed(title = 'Бан лист')
    Ban_List = Net.Get(f"id{ctx.guild.id}", "ban", "json")

    if Ban_List:
        for nick in Ban_List:
            name = f'{nick} - {Ban_List[nick]}'
            emb.add_field(name = name, value = value, inline=False)
        await ctx.channel.send(embed = emb)

    else:
        await ctx.channel.send('Бан лист пуст')


# МУТ
@client.command()
async def mute(ctx, member):
    if ctx.author.name:
        if IsAdmin(ctx.author.roles, Net.Get(f"id{ctx.guild.id}", "admin_roles", "json")) or ctx.author.id == I:
            mute_role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
            await member.add_roles(mute_role)
            await ctx.channel.send(f'Участнику {member.mention}, выдан МУТ за нарушение правил!')
        else:
            await ctx.channel.send('У вас нет доступа к этой команде')


# Временный голосовой канал
async def room(ctx, params):
    params = params.split()
    print(params)
    limit = None,
    private = None

    if 1 <= len(params):
        name = params[0]

        if 2 <= len(params):
            limit = params[1]

            if 3 == len(params):
                private = params[2]

    Rooms = Net.Get(f"id{ctx.guild.id}", "rooms", "json")

    if Rooms:
        if len(Rooms[ctx.guild.id]) >= 5:
            return
    else:
        Rooms = []

    print(name)
    channel = await ctx.guild.create_voice_channel(name = name, user_limit = limit)
    time = datetime.datetime.now()

    Rooms.append({'id': channel.id, 'name': channel.name, 'time': time.minute})
    Net.Set(f"id{ctx.guild.id}", "rooms", Rooms, "json")

    await channel.set_permissions(ctx.author, connect = True, mute_members = True, move_members = True, manage_channels = True)
    
    if private == "p":
        await channel.set_permissions(ctx.guild.default_role, connect = False, manage_channels = False)


# Онлайн
async def G_ONLINE_G(ctx):
    if ctx.author.id == I:
        value = '-------------------------'
        emb = discord.Embed(title = 'Онлайн лист')
        Status = Net.Get(f"id{ctx.guild.id}", "status", "json")
        

        if 'members' in Status:
            for name in Status['members']:
                emb.add_field(name = name, value = value, inline = False)
        else:
            Status['members'] = {}

        await clear(ctx, 0)
        mes = await ctx.channel.send(embed = emb)

        Status['guild'] = ctx.guild.id
        Status['message'] = mes.id
        Status['channel'] = mes.channel.id

        Net.Set(f"id{ctx.guild.id}", "status", Status, "json")


# Обновление сообщения команды: online
@tasks.loop(seconds = 2)
async def online():
    Status = Net.Get("all", "status", "json")

    for guild in Status:
        if guild:
            if 'guild' in guild:
                Guild = client.get_guild(guild['guild'])
                channel = Guild.get_channel(guild['channel'])

                try:
                    ctx = await channel.fetch_message(guild['message'])
                except:
                    Net.Set(f"id{guild['guild']}", "status", {}, "json")
                    break

                value = '-------------------------'
                emb = discord.Embed(title = 'Онлайн лист', color = discord.Color.from_rgb(0,200,0))

                for member in ctx.guild.members:
                    if str(member.status) != 'offline':
                        message = f"{member.name} - Online"
                        emb.add_field(name = message, value = value, inline = False)

                        if member.name in guild['members']:
                            guild['members'].pop(member.name)

                    elif member.name not in guild['members']:
                        now = datetime.datetime.now()
                        guild['members'][member.name] = f"{now.hour}:{now.minute}:{now.second} / {now.day}.{now.month}.{now.year}"
                
                Net.Set(f"id{guild['guild']}", "status", guild, "json")
                
                for member in guild['members']:
                    message = f"{member} - {guild['members'][member]}"
                    emb.add_field(name = message, value = value, inline = False)

                await ctx.edit(embed = emb)


# Авто удаление временных голосовых каналов
@tasks.loop(seconds = 5)
async def room_timer():
    Rooms = Net.Get("all", "rooms", "json")
    
    for room in Rooms:
        channel = client.get_channel(id=room['id'])
        time = datetime.datetime.now()

        if channel:
            if channel.members:
                room['time'] = int(time.minute)
            else:
                if room['time'] == time.minute-2:
                    await channel.delete()
        else:
            guild = room['guild']
            Rooms.remove(room)
            Net.Set(f"id{guild}", "rooms", Rooms, "json")


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

    await ctx.channel.send(embed = emb)


client.run('NzAyMTg1MzM1MDg5NjU5OTA1.GK091H.29E0CygMrQ8C0NXWay_SJMUKGGoVrjNmEqP90c')
