import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandOnCooldown
from discord.ui import Button, View
import asyncio
import random
import os
from datetime import datetime, timezone
import traceback
import json
from discord.errors import NotFound, HTTPException
import aiohttp
import time

intents = discord.Intents.default()
intents.guild_messages = True
intents.guilds = True
intents.members = True


# 샤드 수를 지정합니다.
shard_count = 1 # 샤드 수를 원하는 만큼 설정합니다.
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("."),  owner_ids=[837570564536270848], intents=intents, shard_count=shard_count)
timers = {}  # 각 서버별 타이머를 저장할 딕셔너리
online_records = {}

SERVER_DATA_FILE = 'server_data.json'
BOT_SETTINGS_FILE = 'bot_settings.json'

TOKEN = 'Token'

# Load your token and authorization data from a secure place
with open('config.json', 'r') as file:
    config = json.load(file)


KOREANBOTS_AUTH = config['KOREANBOTS_AUTH']
CHANNEL_ID = config['CHANNEL_ID']
DEVELOPER_IDS = 837570564536270848 # 개발자 유저 ID
WEBHOOK_URL = '에러로그 웹훅링크크'

# 로그 기록을 저장할 리스트
join_logs = []

# 입장 로그를 보낼 채널 ID와 알림 기능 활성화 설정
settings = {
    'notification_channel_id': None,
    'notification_enabled': True
}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)
    
@bot.event
async def on_command_error(ctx, error):
    # 오류 메시지에 대한 조건 처리
    if isinstance(error, commands.CommandNotFound):
        user_message = "존재하지 않는 명령어인거 같아요..! / 업데이트로 인해 사라졌을 수도 있어요!"
    elif isinstance(error, commands.MissingPermissions):
        user_message = "이 명령어를 실행할 권한이 없으시네요..! / 권한이 있는지 확인하고 다시 시도해보세요!"
    elif isinstance(error, commands.BotMissingPermissions):
        user_message = "봇에게 이 명령어를 실행할 권한이 없어요! / 봇에게 권한을 지급해주세요!"
    elif isinstance(error, commands.CommandOnCooldown):
        user_message = f"명령어가 쿨다운중이에요! / {round(error.retry_after, 2)}초 후에 다시 시도해주세요!"
    elif isinstance(error, commands.MissingRequiredArgument):
        user_message = "옵션에 값이 없는거 같아요! / 다시 시도해주세요!"
    elif isinstance(error, commands.NotOwner):
        user_message = "해당 명령어는 개발자 전용 명령어에요!"
    else:
        user_message = "명령어 실행 중 알 수 없는 오류가 발생했네요.. / 오류가 지속된다면 `버그제보` 명령어로 버그를 제보해주세요!"

    # 슬래시 명령어와 텍스트 명령어를 모두 지원
    try:
        if hasattr(ctx, 'respond'):  # 슬래시 명령어 대응
            await ctx.respond(user_message, ephemeral=True)
        else:  # 일반 텍스트 명령어 대응
            await ctx.send(user_message)
    except Exception as e:
        print(f"오류 메시지 전송 중 오류 발생: {e}")
    
bot_owner_id = 개발자 ID

class Timer:
    def __init__(self, ctx, duration):
        self.ctx = ctx
        self.duration = duration
        self.start_time = datetime.now()

# 쿨다운을 관리할 딕셔너리
cooldowns = {}
target_guild_ids = [1081161469195980831, 987654321098765432]  # 자동으로 나가고 싶은 서버 ID
warnings = {}


# 마지막 사용 시간을 저장할 딕셔너리 (유저 ID와 명령어를 키로 사용)
last_used = {}
# 파일 경로 설정
SETTINGS_FILE = 'settings.json'    
start_time = datetime.now()

boot_time = datetime.now()

DATA_DIR = 'server_data'
USER_BLACKLIST_FILE = os.path.join(DATA_DIR, 'user_blacklist.json')
SERVER_BLACKLIST_FILE = os.path.join(DATA_DIR, 'server_blacklist.json')
LOG_CHANNEL_ID = 1248099521985249286  # 로그를 보낼 채널 ID
ADMIN_CHANNEL_ID = 1248099521985249286  # 관리자 채널 ID

# JSON 파일 경로
DATA_FILE = 'user_db.json'

ALLOWED_USER_ID = 837570564536270848 # 허용되는 유저 ID

@bot.event
async def on_guild_join(guild):
    if guild.id in target_guild_ids:
        await guild.leave()
        print(f"{guild.name} 서버를 떠났습니다.")
    else:
        print(f"{guild.name} 서버에 가입했습니다.")

# 시간 변환 함수: 초를 적절한 단위로 변환
def format_time(seconds):
    if seconds >= 86400:  # 24시간 (하루) 이상
        days = seconds // 86400
        return f"{days}일"
    elif seconds >= 3600:  # 1시간 이상
        hours = seconds // 3600
        return f"{hours}시간"
    elif seconds >= 60:  # 1분 이상
        minutes = seconds // 60
        return f"{minutes}분"
    else:
        return f"{seconds}초"
    
cute_images = [
    "https://cdn.discordapp.com/attachments/977151085707923496/1253245883030437918/hannis.jpg?ex=667527ae&is=6673d62e&hm=d78d65207dafee930eb56248d75ad8908985aad82b2ebf8f726884e8c91dfb10&",
    "https://cdn.discordapp.com/attachments/977151085707923496/1253245882460016690/HANNI.jpg?ex=667527ae&is=6673d62e&hm=bc0fd5b360896659e8faf4bb49708011aa6a6696388e4631baccec4371a5c0bc&",
    "https://cdn.discordapp.com/attachments/977151085707923496/1253381912722935859/haniii.jpg?ex=6675a65e&is=667454de&hm=ad91a7bf0bb96e49fcc1f0a1221dfcde7fe0786cab737414c775e0c67834c474&",
    "https://cdn.discordapp.com/attachments/1101044991922556969/1256913091313274993/icon_26.gif?ex=6683d089&is=66827f09&hm=ba809e8928bb98301a96ccf5eb306c5a04ca5425fa0198c455db04d9db9b95fd&",
    "https://cdn.discordapp.com/attachments/1101044991922556969/1257015231914180779/icon_22.gif?ex=66842fa9&is=6682de29&hm=4fd9e672bf9c53ed33324b00d63451cd7b2e2b1adc6447f4f2e3dec7df90d406&",
    "https://cdn.discordapp.com/attachments/1101044991922556969/1257016993094041660/icon_18_1.gif?ex=6684314d&is=6682dfcd&hm=5c4d7362d24fe1aba2923e72948f58d2c3fee05b0a4249a21db552e5718bcc9c&",
    "https://cdn.discordapp.com/attachments/1254307776407142420/1256285872941174956/GIF.gif?ex=66842b64&is=6682d9e4&hm=1c5516bfb406655175d830a737d2309ce65d7f0052f7873df0a7b504afe7288a&",
]
newjeans_songs = [
    "Attention", "Hype Boy", "Cookie", "Hurt", "Ditto", "OMG", "ASAP", "Cool With You", "New Jeans", "Super Shy", "ETA", 
    "Get Up", "Zero", "How Sweet", "Bubble Gum", "아름다운 구속", "우리의 밤은 당신의 낮보다 아름답다", "GODS", "Ditto 250 Remix", 
    "OMG – FRNK Remix", "Attention 250 Remix", "Hype Boy 250 Remix", "Cookie FRNK Remix", "Hurt 250 Remix", "Right Now", "Supernatural"
]

INVITE_LINK = 'https://discord.gg/UfHSqhcj2j'
SPECIFIC_USER_IDS = ['837570564536270848', '3231313312']

DEVELOPER_ID = '837570564536270848'
BOT_VERSION = '2.0.0'

# 도박 데이터 저장
gambling_data = {} 

@bot.event
async def on_ready():
    print(f"봇 로그인을 성공했습니다!")
    print(f"봇 이름: {bot.user.name}")
    print(f"봇 아이디: {bot.user.id}")
    print(f'샤드 ID: {bot.shard_id}')
    print(f'샤드 수: {bot.shard_count}')

    # JSON 파일 초기화 (존재하지 않을 경우)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)

status_index = 0

@tasks.loop(seconds=20)
async def update_status():
    global status_index
    server_count = len(bot.guilds)
    
    status_messages = [
        discord.Game('Prefix: /'),
        discord.Game(f'{server_count}개의 서버에서 활동')
    ]
    
    await bot.change_presence(activity=status_messages[status_index])
    status_index = (status_index + 1) % len(status_messages)

# 파일에서 설정을 로드하는 함수
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("파일이 올바르지 않아서 기본 설정으로 초기화됨..")
            return {
                'notification_channel_id': None,
                'notification_enabled': True
            }
    else:
        return {
            'notification_channel_id': None,
            'notification_enabled': True
        }

# 파일에 설정을 저장하는 함수
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# 서버 데이터 가져오기 함수
def get_server_data(server_id):
    try:
        with open(SERVER_DATA_FILE, 'r', encoding='utf-8') as file:
            server_data = json.load(file)
        return server_data.get(str(server_id), {"users": {}})
    except FileNotFoundError:
        return {"users": {}}

# 초기 설정 로드
settings = load_settings()

# 서버 데이터 업데이트 함수
def update_server_data(server_id, user_id=None, user_data=None, settings=None):
    with open(SERVER_DATA_FILE, 'r+', encoding='utf-8') as file:
        server_data = json.load(file)
        if str(server_id) not in server_data:
            server_data[str(server_id)] = {"users": {}, "settings": {}}
        if user_id and user_data:
            server_data[str(server_id)]["users"][str(user_id)] = user_data
        if settings:
            server_data[str(server_id)]["settings"] = settings
        file.seek(0)
        json.dump(server_data, file, ensure_ascii=False, indent=4)
        file.truncate()

# 봇 설정 가져오기 함수
def get_bot_settings():
    try:
        with open(BOT_SETTINGS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def load_user_data():
    if not os.path.exists(DATA_FILE):
        data = {"users": {}}
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
        return data

    with open(DATA_FILE, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {"users": {}}
            with open(DATA_FILE, 'w') as file:
                json.dump(data, file, indent=4)
    
    return data

def save_user_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# 도박 데이터를 관리하는 딕셔너리
gambling_data = {}

# 서버별 도박 데이터를 불러오거나 초기화하는 함수
def get_guild_data(guild_id):
    if guild_id not in gambling_data:
        gambling_data[guild_id] = {"balances": {}}
    return gambling_data[guild_id]

# 사용자의 잔액을 확인하거나 설정하는 함수
def get_user_balance(guild_id, user_id):
    guild_data = get_guild_data(guild_id)
    if user_id not in guild_data["balances"]:
        guild_data["balances"][user_id] = 0  # 초기 잔액 설정
    return guild_data["balances"][user_id]

def set_user_balance(guild_id, user_id, balance):
    guild_data = get_guild_data(guild_id)
    guild_data["balances"][user_id] = balance
  
@bot.slash_command(description="뉴진스 하니에 대한 소개를 전송해요!")
async def 하니(ctx):
        embed = discord.Embed(title="뉴진스 하니 소개", description="하니의 대한 소개에요!", color=0x0082ff)
        embed.add_field(name="활동명", value="하니 (Hanni)", inline=True)
        embed.add_field(name="본명", value="Hanni Ngoc Pham (하니 응옥 팜)", inline=True)
        embed.add_field(name="소속 그룹", value="NewJeans", inline=True)
        embed.add_field(name="출생", value="2004년 10월 6일 (만 19세)", inline=True)
        embed.add_field(name="신체", value="162cm, O형", inline=True)
        embed.add_field(name="소속사", value="ADOR", inline=True)
        embed.set_footer(text="출처: 나무위키")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1247817281484881958/1270376432526168205/kh_u9UOL2mRZzX3A0lCFxfFcqtgnC1Ed7FvlcWnN3TykKJD-S_ABE3yCDb_UnWc-lfIz-md2MuQ6bTVs019XrQ.png")
        await ctx.respond(embed=embed)

@bot.slash_command(description="뉴진스 다니엘에 대한 소개를 전송해요!")
async def 다니엘(ctx):
        embed = discord.Embed(title="다니엘", description="", color=0x0082ff)
        embed.add_field(name="활동명", value="다니엘 (Danielle)", inline=True)
        embed.add_field(name="본명", value="Danielle June Marsh (다니엘 준 마쉬) / 모지혜 (牟智慧, Mo Jihye)", inline=True)
        embed.add_field(name="소속 그룹", value="NewJeans", inline=True)
        embed.add_field(name="출생", value="2005년 4월 11일 (만 19세)", inline=True)
        embed.add_field(name="신체", value="165cm, AB형", inline=True)
        embed.add_field(name="소속사", value="ADOR", inline=True)
        embed.set_footer(text="출처: 나무위키")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1247817281484881958/1270368554620948510/c4f00b5408186e5c076b4607639d07ab.png")  # Replace with the actual URL of 
        await ctx.respond(embed=embed)

@bot.slash_command(description="뉴진스 민지의 대한 소개를 전송해요!")
async def 민지(ctx):
        embed = discord.Embed(title="민지", description="", color=0x0082ff)
        embed.add_field(name="활동명", value="민지 (MINJI)", inline=True)
        embed.add_field(name="본명", value="김민지 (金玟池, Kim Minji)", inline=True)
        embed.add_field(name="소속 그룹", value="NewJeans", inline=True)
        embed.add_field(name="출생", value="2004년 5월 7일 (만 20세)", inline=True)
        embed.add_field(name="신체", value="169cm, A형", inline=True)
        embed.add_field(name="소속사", value="ADOR", inline=True)
        embed.set_footer(text="출처: 나무위키")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1247817281484881958/1270369633022644357/IMG_1912.png")
        await ctx.respond(embed=embed)

@bot.slash_command(description="뉴진스 해린에 대한 소개를 전송해요!")
async def 해린(ctx):
        embed = discord.Embed(title="해린", description="", color=0x0082ff)
        embed.add_field(name="활동명", value="해린 (Haerin)", inline=True)
        embed.add_field(name="본명", value="강해린 (姜諧潾, Kang Haerin)", inline=True)
        embed.add_field(name="소속 그룹", value="NewJeans", inline=True)
        embed.add_field(name="출생", value="2006년 5월 15일 (만 18세)", inline=True)
        embed.add_field(name="신체", value="165cm, B형", inline=True)
        embed.add_field(name="소속사", value="ADOR", inline=True)
        embed.set_footer(text="출처: 나무위키")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1247817281484881958/1270371518068686883/4458a6af23c7c63b891b5f557f609e68.png")
        await ctx.respond(embed=embed)

@bot.slash_command(description="뉴진스 혜인에 대한 소개를 전송해요!")
async def 혜인(ctx):
        embed = discord.Embed(title="혜인", description="", color=0x0082ff)
        embed.add_field(name="활동명", value="혜인 (Hyein)", inline=True)
        embed.add_field(name="본명", value="이혜인 (李惠仁, Lee Hyein)", inline=True)
        embed.add_field(name="소속 그룹", value="NewJeans", inline=True)
        embed.add_field(name="출생", value="2008년 4월 21일 (만 16세)", inline=True)
        embed.add_field(name="신체", value="170cm, O형", inline=True)
        embed.add_field(name="소속사", value="ADOR", inline=True)
        embed.set_footer(text="출처: 나무위키")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1247817281484881958/1270374488629842111/5_J4ISygzRHOsh0v5_wrRkQpYT0FtgMmLRLJh-3QrtZXOi1I_7YE8dj5AgESn0sRosLzSZww3HPjMQvHXBE_kg.png")
        await ctx.respond(embed=embed)
        
@bot.slash_command(description="하니봇 개발자에 대한 정보를 전송해요!")
async def 개발자(ctx):
        user_id = '837570564536270848'
        user_mention = f'<@{user_id}>'
        embed = discord.Embed(title="하니봇 개발자", description=f"하니봇은 {user_mention}님이 개발하였어요!", color=0x0082ff)
        embed.add_field(name="문의 및 제안", value="아래 버튼을 눌러 서포트 서버에 입장해주세요!", inline=True)
        
        # Create a button
        view = discord.ui.View()
        button = discord.ui.Button(label="서포트 서버", url=f'https://discord.gg/8xZtuQ5rsr')
        view.add_item(button)
        await ctx.respond(embed=embed, view=view)

#@bot.slash_command(description="현재 봇의 상태를 확인할수 있어요!")
#async def 봇상태(ctx):
#        embed = discord.Embed(title="현재 하니봇이 업데이트 중이에요!", description="현재 하니봇이 업데이트 중이에요!")
#        embed.add_field(name="문의 및 제안", value="아래 버튼을 눌러 서포트 서버에 입장해주세요!", inline=True)
#        
#       # Create a button
#       view = discord.ui.View()
#        button = discord.ui.Button(label="서포트 서버", url=f'https://discord.gg/8xZtuQ5rsr')
#        view.add_item(button)
#        await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="서버 정보를 확인할 수 있어요!")
async def 서버정보(ctx):
    guild = ctx.guild
    boost_level = guild.premium_tier
    
    # 부스트 레벨
    boost_tier = {
        0: "부스트 없음",
        1: "레벨 1",
        2: "레벨 2",
        3: "레벨 3"
    }.get(boost_level, "알 수 없음")
    
    # 서버 아이콘 URL
    server_icon_url = guild.icon.url if guild.icon else discord.Embed.Empty
    
    server_creation_unix_timestamp = int(guild.created_at.timestamp())
    server_creation_timestamp = f"<t:{server_creation_unix_timestamp}:D>"  # Discord 타임스탬프 포맷으로 변환
    
    embed = discord.Embed(title=f'{guild.name} 서버 정보', color=discord.Color.blue())
    embed.set_thumbnail(url=server_icon_url)
    embed.add_field(name='서버 이름', value=guild.name, inline=True)
    embed.add_field(name='멤버 수', value=guild.member_count, inline=True)
    embed.add_field(name='부스트 레벨', value=boost_tier, inline=True)
    embed.add_field(name='역할 수', value=len(guild.roles), inline=True)
    embed.add_field(name='텍스트 채널 수', value=len(guild.text_channels), inline=True)
    embed.add_field(name='음성 채널 수', value=len(guild.voice_channels), inline=True)
    embed.add_field(name='서버 생성 일자', value=server_creation_timestamp, inline=True)
    embed.set_footer(text=f'서버 ID: {guild.id}')
    await ctx.respond(embed=embed)
    
@bot.slash_command(description="하니봇의 정보를 알려줘요!")
async def 봇정보(ctx):
    # 봇의 기본 정보
    bot_name = bot.user.name
    bot_id = bot.user.id
    server_count = len(bot.guilds)
    boot_time_unix = int(boot_time.timestamp())
    
    # 코드 길이 측정
    code_file_path = os.path.abspath(__file__)
    with open(code_file_path, 'r', encoding='utf-8') as file:
        code_length = len(file.readlines())
    
    # 개발자 멘션
    developer_mention = f'<@{DEVELOPER_ID}>'

    total_users = sum(guild.member_count for guild in bot.guilds)
    latency = bot.latency * 1000  # 초 단위의 지연 시간을 밀리초로 변환
    
    # 봇 정보 Embed 생성
    bot_info_embed = discord.Embed(title=f'{bot_name}의 정보', color=discord.Color.blue())
    bot_info_embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else discord.Embed.Empty)
    bot_info_embed.add_field(name='봇 이름', value=bot_name, inline=True)
    bot_info_embed.add_field(name='봇 ID', value=bot_id, inline=True)
    bot_info_embed.add_field(name='핑', value=f"🏓: {latency:.2f} ms!", inline=True)
    bot_info_embed.add_field(name='서버 수', value=server_count, inline=True)
    bot_info_embed.add_field(name='이용자 수', value=total_users, inline=True)
    bot_info_embed.add_field(name='부팅 시간', value=f'<t:{boot_time_unix}:R>', inline=True)
    bot_info_embed.add_field(name='코드 길이', value=f'{code_length} lines', inline=True)
    bot_info_embed.add_field(name='봇 버전', value=BOT_VERSION, inline=True)
    bot_info_embed.add_field(name='봇 개발 언어', value='py-cord', inline=True)
    
    # Create buttons for the website and support server
    view = discord.ui.View()
    website_button = discord.ui.Button(
        label="웹사이트 방문", 
        url='https://hannibot.netlify.app', 
        style=discord.ButtonStyle.primary
    )
    support_server_button = discord.ui.Button(
        label="서포트 서버", 
        url='https://discord.gg/8xZtuQ5rsr', 
        style=discord.ButtonStyle.primary
    )
    
    view.add_item(website_button)
    view.add_item(support_server_button)
    
    # Add the developer mention field
    bot_info_embed.add_field(name='개발자', value=developer_mention, inline=True)

    await ctx.respond(embed=bot_info_embed, view=view)

@bot.slash_command(description="멘션한 유저를 서버에서 추방해요!")
@discord.option(name='유저', description='유저을 선택해주세요')
@discord.option(name='사유', description='사유 입력해주세요')
@commands.has_permissions(kick_members=True)
async def 킥(ctx, 유저: discord.Member, 사유: str):
        member = 유저
        reason = 사유 if 사유 else '사유 없음'

        await ctx.guild.kick(member, reason=reason)

        embed = discord.Embed(
            description=f"{member.name} 님을 추방했습니다.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)

@킥.error
async def set_balance_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title='권한 부족',
            description='이 명령어를 사용하려면 관리자 권한이 필요해요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
    else:
        # Handle other errors
        embed = discord.Embed(
            title='오류',
            description='명령어를 실행하는 중에 오류가 발생했어요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

@bot.slash_command(description="멘션한 유저를 서버에서 추방해요!")
@discord.option(name='유저', description='유저를 멘션해주세요!', type=discord.Member)
@discord.option(name='사유', description='사유를 입력해주세요!', required=False)
@commands.has_permissions(ban_members=True)
async def 벤(ctx, 유저: discord.Member, 사유: str = '사유 없음'):
    member = 유저
    reason = 사유

    try:
        await ctx.guild.ban(member, reason=reason)

        embed = discord.Embed(
            description=f"{member.name} 님을 서버에서 차단했어요! 사유: {reason}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(
            title="오류",
            description="권한이 부족하여 사용자를 차단할 수 없습니다.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="오류",
            description=f"사용자를 차단하는 동안 오류가 발생했습니다: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

@벤.error
async def set_balance_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title='권한 부족',
            description='이 명령어를 사용하려면 관리자 권한이 필요해요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
    else:
        # Handle other errors
        embed = discord.Embed(
            title='오류',
            description='명령어를 실행하는 중에 오류가 발생했어요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        
@bot.slash_command(description="채널의 메시지를 삭제합니다.")
@discord.option(name='수량', type=int, description='지울 메시지 수를 입력해주세요 (14일이 지난 메세지는 삭제가 불가능합니다.)')
async def 청소(ctx, 수량: int):
    if not ctx.author.guild_permissions.manage_messages:
        embed = discord.Embed(
            description="권한이 부족하여 명령어를 처리할 수 없어요!",
            colour=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)
        return

    await ctx.defer()  # 상호작용 시간 초과를 방지하기 위해 지연 응답 사용

    try:
        if 수량 <= 0:
            await ctx.followup.send("지울 메시지 수는 1 이상이어야 해요!", ephemeral=True)
            return

        deleted_count = 0
        messages_to_delete = []
        
        async for message in ctx.channel.history(limit=100):  # 100개씩 가져오기
            # 메시지가 14일 이내일 경우에만 삭제 목록에 추가
            if (discord.utils.utcnow() - message.created_at).days < 14:
                messages_to_delete.append(message)
                if len(messages_to_delete) == 수량:
                    break

        if not messages_to_delete:
            await ctx.followup.send("삭제할 수 있는 메시지가 없습니다!", ephemeral=True)
            return

        # 메시지 삭제 시도
        headers = {
            'Authorization': f'Bot {TOKEN}',
            'Content-Type': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            message_ids = [msg.id for msg in messages_to_delete]
            data = {'messages': message_ids}
            
            try:
                async with session.post(f'https://discord.com/api/v10/channels/{ctx.channel.id}/messages/bulk-delete', headers=headers, json=data) as response:
                    if response.status == 204:
                        deleted_count += len(message_ids)
                    else:
                        error_msg = await response.text()
                        raise discord.HTTPException(response=response, text=error_msg)
            except discord.HTTPException:
                # 삭제 불가한 메시지가 있는 경우, 예외를 무시하고 계속 진행
                pass

        embed = discord.Embed(
            title=f"{deleted_count}개의 메시지가 삭제되었어요!",
            description=f"요청한 메시지 수: {수량}개 / 실제 삭제된 메시지 수: {deleted_count}개",
            color=discord.Color.green()
        )
        view = discord.ui.View()
        button = discord.ui.Button(label="서포트 서버", url='https://discord.gg/8xZtuQ5rsr')
        view.add_item(button)
        response_message = await ctx.followup.send(embed=embed, view=view)

        # 5초 후에 명령어 메시지 삭제
        await asyncio.sleep(5)
        try:
            await ctx.delete()
        except discord.NotFound:
            pass  # 이미 삭제된 경우 무시
        
        # 5초 후에 삭제 완료 메시지 삭제
        await asyncio.sleep(5)
        try:
            await response_message.delete()
        except discord.NotFound:
            pass  # 이미 삭제된 경우 무시

    except discord.Forbidden:
        # 봇에게 권한이 없을 때의 오류 처리
        embed = discord.Embed(
            description="봇에게 메시지를 관리할 권한이 없어요! / 봇에게 권한을 지급해주세요!",
            color=discord.Color.red()
        )
        await ctx.followup.send(embed=embed, ephemeral=True)
    except Exception as e:
        # 모든 다른 예외 처리, 로그 기록은 하지 않음
        embed = discord.Embed(
            description=f"메시지 삭제 중 오류가 발생했어요: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.followup.send(embed=embed, ephemeral=True)
        # 오류 메시지를 사용자에게 전송하고, 로그는 기록하지 않음
    
@bot.slash_command(description="뉴진스의 최신곡 정보를 전송해요!")
async def 최신곡(ctx):
    await send_latest_song_info(ctx)

async def send_latest_song_info(ctx):
    embed = discord.Embed(title="뉴진스 최신곡", description="", color=0x0082ff)
    embed.add_field(name="", value="아래의 `보러가기` 버튼을 눌러주세요!", inline=True)

    # 썸네일 가져오기
    video_id = 'ZncbtRo7RXs'
    image_url = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
    embed.set_image(url=image_url)
    
    # Create a button
    view = discord.ui.View()
    button = discord.ui.Button(label="보러가기", url=f'https://www.youtube.com/watch?v={video_id}')
    view.add_item(button)   
    await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="뉴진스의 이전 곡 정보를 전송해요!")
async def 이전곡 (ctx):
        embed = discord.Embed(title="Right Now", description="최신곡의 이전 곡인 Right Now의 뮤비에요!", color=0x0082ff)
        embed.add_field(name="", value="아래의 `보러가기` 버튼을 눌러주세요!", inline=True)
        
        # 썸네일 가져오기
        video_id = 'm6pTbEz4w3o'
        image_url = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
        embed.set_image(url=image_url)
        
        # Create a button
        view = discord.ui.View()
        button = discord.ui.Button(label="보러가기", url=f'https://www.youtube.com/watch?v={video_id}')
        view.add_item(button)
        await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="뉴진스의 데뷔 곡 정보를 전송해요!")
async def 데뷔곡 (ctx):
        embed = discord.Embed(title="데뷔곡", description="뉴진스 데뷔 곡을 알려드릴게요!", color=0x0082ff)
        embed.add_field(name="", value="아래의 `보러가기` 버튼을 눌러주세요!", inline=True)
        # 썸네일 가져오기
        video_id = 'js1CtxSY38I'
        image_url = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
        embed.set_image(url=image_url)
        
        # Create a button
        view = discord.ui.View()
        button = discord.ui.Button(label="보러가기", url=f'https://www.youtube.com/watch?v={video_id}')
        view.add_item(button)
        await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="뉴진스의 하입보이 영상을 전송해요!")
async def 하입보이(ctx):
    embed = discord.Embed(title="하입보이", description="뉴진스 하입보이의 퍼포먼스 영상이에요! ", color=0x0082ff)
    embed.add_field(name="영상 링크", value="아래의 `보러가기` 버튼을 눌러주세요!", inline=True)
    
    video_id = '11cta61wi0g'
    image_url = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
    embed.set_image(url=image_url)
    
    # Create a button
    view = discord.ui.View()
    button = discord.ui.Button(label="보러가기", url=f'https://www.youtube.com/watch?v={video_id}')
    view.add_item(button)
    
    await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="봇의 핑을 확인하실수 있어요!")
async def 핑(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="Pong!", description=f"현재 핑은 {round(bot.latency)}ms 이에요!", color=0x0082ff)
    # Create a button
    view = discord.ui.View()
    button = discord.ui.Button(label="서포트 서버", url=f'https://discord.gg/8xZtuQ5rsr')
    view.add_item(button)
    await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="뉴진스의 노래 중 한 곡을 추천 해 드려요!")
async def 노래추천 (ctx):
        song = random.choice(newjeans_songs)
        embed = discord.Embed(title="뉴진스 노래 추천", description=f"오늘은 **{song}** 이 곡 어떠세요?", color=0x0082ff)
        # Create a button
        view = discord.ui.View()
        button = discord.ui.Button(label="서포트 서버", url=f'https://discord.gg/8xZtuQ5rsr')
        view.add_item(button)
        await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="컴백일")
async def 컴백일 (ctx):
        embed = discord.Embed(title="컴백일", description="뉴진스의 컴백일을 알려드릴게요!", color=0x0082ff)
        embed.add_field(name="컴백일", value="2024년 5월 24일에 Bubble Gum으로 컴백했어요!", inline=True)
        await ctx.respond(embed=embed)

@bot.slash_command(description="사진을 전송해요!")
async def 귀여워 (ctx):
        random_image = random.choice(cute_images)
        await ctx.respond(random_image)
    # 사용자 메시지 이벤트 핸들러

@bot.slash_command(description="멘션한 유저의 정보를 전송해요!")
@discord.option(name='유저', description='유저 선택해주세요', type=discord.Member)
async def 유저정보(ctx, 유저: discord.Member):
    try:
        # 경고 횟수 가져오기
        warning_count = warnings.get(유저.id, 0)
        join_unix_timestamp = int(유저.joined_at.timestamp())
        join_timestamp = f"<t:{join_unix_timestamp}:D>"  # 서버 참여 일자

        account_create_unix_timestamp = int(유저.created_at.timestamp())
        account_create_timestamp = f"<t:{account_create_unix_timestamp}:D>"  # 계정 생성 일자

        embed = discord.Embed(title=f"{유저}님의 정보", color=0x0082ff)
        embed.set_thumbnail(url=유저.avatar.url if 유저.avatar else discord.Embed.Empty)
        embed.add_field(name="유저 이름", value=유저.name, inline=True)
        embed.add_field(name="유저 ID", value=유저.id, inline=True)
        embed.add_field(name="서버 참여 일자", value=join_timestamp, inline=True)
        embed.add_field(name="계정 생성 일자", value=account_create_timestamp, inline=True)
        embed.add_field(name="경고 횟수", value=warning_count, inline=True)

        # Create a button
        view = discord.ui.View()
        button = discord.ui.Button(label="서포트 서버", url='https://discord.gg/8xZtuQ5rsr')
        view.add_item(button)
        await ctx.respond(embed=embed, view=view)

    except Exception as e:
        await ctx.respond(f"오류 발생: {str(e)}")
    
@bot.slash_command(description="뉴진스의 정보를 전송해요!")
async def 뉴진스 (ctx):
        embed = discord.Embed(title='뉴진스 소개', description='뉴진스(NewJeans)는 대한민국의 5인조 걸그룹으로,어도어(ADOR) 소속이에요!', color=0xbca5e6)
        embed.add_field(name='멤버', value='하니,혜인,민지,해린,다니엘', inline=True)
        embed.add_field(name='데뷔일', value='2022년 7월 22일', inline=True)
        embed.add_field(name='데뷔곡', value='EP 1집 New Jeans로 데뷔했어요!', inline=True)
        embed.add_field(name='소속사', value='어도어(ADOR)', inline=True)
        # Create a button
        view = discord.ui.View()
        button = discord.ui.Button(label="서포트 서버", url=f'https://discord.gg/8xZtuQ5rsr')
        view.add_item(button)
        await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="뉴진스의 데뷔일 정보를 전송해요!")
async def 데뷔일 (ctx):
        embed = discord.Embed(title="데뷔일", description="뉴진스 데뷔일을 알려드릴게요!", color=0x00bffd)
        embed.add_field(name="", value="**2022년 7월 22일에  EP 1집 New Jeans로 데뷔했어요!**", inline=True)
        await ctx.respond(embed=embed)

# 상태 인텐트 관련 이슈로 삭제
# @bot.slash_command(description="멘션한 유저의 현재 활동 상태 정보를 전송해요!")
# @discord.option(name='유저', type=discord.Member, description='유저를 멘션해주세요!')
# async def 상태(ctx, 유저: discord.Member = None):
#     유저 = 유저 or ctx.author
#
#     if 유저:
#         activity = 유저.activity
#         if activity is None:
#             embed = discord.Embed(
#                 title=f'{유저.name}님의 현재 활동',
#                 description='현재 어떤 활동도 하고 있지 않아요!',
#                 color=discord.Color.red()
#             )
#             await ctx.respond(embed=embed)
#         else:
#             activity_type = activity.type
#             activity_name = activity.name
#             embed = discord.Embed(title=f'{유저.name}님의 현재 활동', color=discord.Color.green())
#
#             if activity_type == discord.ActivityType.playing:
#                 embed.description = f'`{activity_name}`을 하고 계시네요!'
#             elif activity_type == discord.ActivityType.streaming:
#                 embed.description = f'`{activity_name}`을 스트리밍하고 계시네요!'
#                 embed.add_field(name='URL', value=activity.url)
#             elif activity_type == discord.ActivityType.listening:
#                 if isinstance(activity, discord.Spotify):
#                     embed.description = f'Spotify에서 `{activity.title}`을 듣고 계시네요!'
#                     embed.add_field(name='아티스트', value=', '.join(activity.artists))
#                     embed.add_field(name='앨범', value=activity.album)
#                     embed.set_thumbnail(url=activity.album_cover_url)
#                     # "노래 듣기" 버튼 추가
#                     view = View()
#                     button = Button(label="노래 듣기", url=f'https://open.spotify.com/track/{activity.track_id}')
#                     view.add_item(button)
#                     await ctx.respond(embed=embed, view=view)
#                     return
#                 elif "YouTube Music" in activity_name:
#                     embed.description = f'YouTube Music에서 `{activity.details}`을 듣고 계시네요!'
#                     embed.add_field(name='아티스트', value=activity.state)
#                     embed.set_thumbnail(url=activity.assets.large_image_url)
#                     # "노래 듣기" 버튼 추가
#                     view = View()
#                     button = Button(label="노래 듣기", url=f'https://music.youtube.com/watch?v={activity.session_id}')
#                     view.add_item(button)
#                     await ctx.respond(embed=embed, view=view)
#                     return
#                 elif "SoundCloud" in activity_name:
#                     embed.description = f'SoundCloud에서 `{activity.details}`을 듣고 계시네요!'
#                     embed.add_field(name='아티스트', value=activity.state)
#                     embed.set_thumbnail(url=activity.assets.large_image_url)
#                     # "노래 듣기" 버튼 추가
#                     view = View()
#                     button = Button(label="노래 듣기", url=activity.url)
#                     view.add_item(button)
#                     await ctx.respond(embed=embed, view=view)
#                     return
#                 else:
#                     embed.description = f'`{activity_name}`을 듣고 계시네요!'
#             elif activity_type == discord.ActivityType.watching:
#                 embed.description = f'`{activity_name}`을 시청 중이네요!'
#             elif activity_type == discord.ActivityType.custom:
#                 embed.description = f'`{activity_name}`을 하고 계시네요!'
#             else:
#                 embed.description = f'`{activity_name}`을 하고 계시네요!'
#             
#             await ctx.respond(embed=embed)
#
#             # "서포트 서버" 버튼 추가
#             view = View()
#             button = Button(label="서포트 서버", url='https://discord.gg/8xZtuQ5rsr')
#             view.add_item(button)
#             await ctx.respond(embed=embed, view=view)
        
@bot.slash_command(description="주어진 옵션 중에서 하나를 골라요!")
@discord.option(name='옵션', description='봇이 고를 옵션을 입력해주세요! (띄어쓰기로 구분)')
async def 골라(ctx, 옵션: str):
    # 띄어쓰기로 옵션을 분리
    옵션_목록 = [opt.strip() for opt in 옵션.split()]
    
    if len(옵션_목록) < 2:
        await ctx.respond("2개 이상의 옵션을 입력해주세요!")
    else:
        선택된_옵션 = random.choice(옵션_목록)
        embed = discord.Embed(
            title="옵션 선택 결과",
            description=f"저는 **{선택된_옵션}**이(가) 더 좋아요!",
            color=discord.Color.blue()
        )

        # Fallback to default avatar if user has no custom avatar
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url

        # 멘션 추가
        embed.set_footer(text=f"요청자: {ctx.author.display_name}", icon_url=avatar_url)
        await ctx.respond(embed=embed)

@bot.slash_command(description="멘션한 유저에게 경고를 지급해요!")
@commands.has_permissions(administrator=True)
@discord.option(name='유저', description='유저를 멘션해주세요!')
@discord.option(name='사유', description='경고 사유를 입력해주세요!')
async def 경고(ctx, 유저: discord.Member, 사유: str):
    if 유저 == ctx.author:
        await ctx.respond('자신에게 경고를 줄 수 없어요!', ephemeral=True)
        return

    if 유저.id not in warnings:
        warnings[유저.id] = []

    warnings[유저.id].append(사유)
    await ctx.respond(f'{유저.mention}님에게 경고를 지급했어요!')

@경고.error
async def 경고_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title='권한 부족',
            description='이 명령어를 사용하려면 관리자 권한이 필요해요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        # 다른 오류 처리
        embed = discord.Embed(
            title='오류 발생',
            description='명령어를 실행하는 중에 오류가 발생했어요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(description="유저의 경고 횟수를 볼 수 있어요!")
@discord.option(name='유저', description='경고 목록을 확인할 유저를 멘션해주세요!')
async def 경고목록(ctx, 유저: discord.Member):
    try:
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["administrator"])
        
        if 유저.id not in warnings or not warnings[유저.id]:
            embed = discord.Embed(
                title=f'{유저}님의 경고 목록',
                description='현재 경고가 없습니다.',
                color=discord.Color.green()
            )
            await ctx.respond(embed=embed)
            return
        
        embed = discord.Embed(
            title=f'{유저}님의 경고 목록',
            color=discord.Color.red()
        )
        for i, warning in enumerate(warnings[유저.id], 1):
            # 경고 사유를 필드에 추가
            embed.add_field(name=f'`{i}`번째 경고', value=f'사유: {warning}', inline=True)
        
        await ctx.respond(embed=embed)
    
    except commands.MissingPermissions as e:
        embed = discord.Embed(
            title='권한 부족',
            description=f"이 명령어를 사용하려면 다음 권한이 필요해요: {', '.join(e.missing_perms)}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

@경고목록.error
async def 경고목록_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title='권한 부족',
            description='이 명령어를 사용하려면 관리자 권한이 필요해요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        # 다른 오류 처리
        embed = discord.Embed(
            title='오류 발생',
            description='명령어를 실행하는 중에 오류가 발생했어요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)
        
@bot.slash_command(name='투표', description='투표를 생성해요!')
@commands.has_permissions(administrator=True)
@discord.option("제목", str, description="투표 주제를 입력해주세요!")
@discord.option("항목1", str, description="첫 번째 항목을 입력해주세요!")
@discord.option("항목2", str, description="두 번째 항목을 입력해주세요!")
@discord.option("항목3", str, description="세 번째 항목을 입력해주세요!", required=False)
@discord.option("항목4", str, description="네 번째 항목을 입력해주세요!", required=False)
@discord.option("항목5", str, description="다섯 번째 항목을 입력해주세요!", required=False)
@discord.option("항목6", str, description="여섯 번째 항목을 입력해주세요!", required=False)
async def 투표(ctx, 제목: str, 항목1: str, 항목2: str, 항목3: str = None, 항목4: str = None, 항목5: str = None, 항목6: str = None):
    options = [항목1, 항목2, 항목3, 항목4, 항목5, 항목6]
    options = [option for option in options if option is not None]

    if len(options) < 2:
        await ctx.respond('적어도 두 가지 이상의 옵션을 입력해주세요!', ephemeral=True)
        return
    if len(options) > 6:
        await ctx.respond('최대 6개까지만 가능합니다!', ephemeral=True)
        return

    embed = discord.Embed(title=제목, color=discord.Color.blue())
    for i, option in enumerate(options):
        embed.add_field(name=f'옵션 {i+1}', value=option, inline=True)

    poll_message = await ctx.respond(embed=embed)
    poll_message = await poll_message.original_response()

    for i in range(len(options)):
        await poll_message.add_reaction(chr(127462 + i))
        
# 타이머 설정 슬래시 커맨드
@bot.slash_command(description="타이머를 설정해요! (시간이 다 지나면 멘션)")
@discord.option(name='시간', type=str, description='설정할 시간을 입력해주세요! / 10s,2h,24h')
async def 타이머(ctx, 시간: str):
    # 최대 시간 설정 (24시간)
    MAX_SECONDS = 24 * 60 * 60

    # 시간을 초 단위로 변환
    seconds = 0
    try:
        if 'h' in 시간:
            hours = int(시간.replace('h', ''))
            seconds = hours * 3600
        elif 'm' in 시간:
            minutes = int(시간.replace('m', ''))
            seconds = minutes * 60
        elif 's' in 시간:
            seconds = int(시간.replace('s', ''))
        elif 'd' in 시간:
            days = int(시간.replace('d', ''))
            seconds = days * 86400
        else:
            await ctx.respond("잘못된 시간 형식인 것 같아요! / 예: 10s, 5m, 1h")
            return
    except ValueError:
        await ctx.respond("잘못된 시간 형식인 것 같아요! / 예: 10s, 5m, 1h")
        return

    # 최대 시간 초과 시 에러 메시지
    if seconds <= 0 or seconds > MAX_SECONDS:
        await ctx.respond(f'시간은 0보다 크고 {MAX_SECONDS // 3600}시간 이하로 설정해야 해요!')
        return

    # 타이머 시작 메시지 (임베드)
    time_display = format_time(seconds)  # 적절한 단위로 변환된 시간 표시
    embed = discord.Embed(title="타이머 설정", description=f'{time_display} 타이머를 설정했어요!', color=discord.Color.green())
    await ctx.respond(embed=embed)

    # 타이머 대기
    await asyncio.sleep(seconds)

    # 타이머 완료 후 멘션 메시지 (텍스트로 멘션)
    await ctx.respond(f'{ctx.author.mention}님이 설정하신 {time_display}가 지났어요!')

@bot.slash_command(description="에브리원 공지를 전송해요!")
@commands.has_permissions(administrator=True)
@discord.option(name='내용', description='공지를 할 내용을 적어주세요! (관리자 권한이 필요해요!)')
@discord.option(name='색상', description='임베드 색상을 선택해주세요!', choices=['빨간색', '초록색', '파란색'])
@discord.option(name='멘션', description='에브리원 멘션 여부를 선택해주세요!', choices=['멘션', '노멘션'])
@commands.cooldown(1, 120, commands.BucketType.user)  # (갯수, 시간(초), 버켓타입
async def 공지사항(ctx, 내용: str, 색상: str = 'red', 멘션: str = 'yes'):
    color_dict = {
        'red': discord.Color.red(),
        'green': discord.Color.green(),
        'blue': discord.Color.blue()
    }

    embed_color = color_dict.get(색상, discord.Color.red())
    embed = discord.Embed(title="공지사항", description=내용, color=embed_color)
    
    if 멘션 == 'yes':
        await ctx.respond("||@everyone||", embed=embed)
    else:
        await ctx.respond(embed=embed)

    await ctx.message.delete()

@공지사항.error
async def announce_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f'이 명령어는 {error.retry_after:.0f}초 후에 다시 사용할 수 있어요!')
        
@bot.slash_command(description="하니봇 도박 서비스에 가입해요!")
async def 가입(ctx):
    try:
        user_id = str(ctx.author.id)

        # 사용자 데이터 불러오기
        user_data = load_user_data()

        if user_id in user_data:
            embed = discord.Embed(
                title='가입 실패',
                description='이미 가입되어 있습니다! `/도박` 명령어로 도박 서비스를 이용해 보세요!',
                color=discord.Color.red()
            )
        else:
            user_data[user_id] = {
                'money': 10000,
                'last_daily_reward': None,  # 마지막 일일 보상 일시
                'items': {},  # 사용자 아이템 목록
                'last_check_in': None  # 마지막 출석 체크 일시
            }
            save_user_data(user_data)
            embed = discord.Embed(
                title='가입 완료',
                description='가입이 완료되었습니다! / 초기 자산 `10000원`을 지급받았고, `/도박` 명령어로 도박을 이용해 보세요!',
                color=discord.Color.green()
            )

        # Create a button
        view = discord.ui.View()
        button = discord.ui.Button(label="서포트 서버", url=f'https://discord.gg/8xZtuQ5rsr')
        view.add_item(button)
        await ctx.respond(embed=embed, view=view)
        
    except Exception as e:
        print(f"An error occurred in register command: {e}")
        embed = discord.Embed(
            title='오류 발생',
            description=f'명령어 처리 중 오류가 발생했습니다: {e}',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

@bot.slash_command(description="유저의 지갑 정보를 확인해요!")
@discord.option(name='유저', description='유저 선택해주세요', type=discord.Member)
async def 지갑(ctx, 유저: discord.Member):
    try:
        # 유저 정보 가져오기
        user_info = get_user_info(유저.id)  # 이 함수는 유저 정보를 반환하는 함수로 가정합니다.

        # 기본값 설정
        money = user_info.get("money", 0)
        daily_streak = user_info.get("daily_streak", 0)

        embed = discord.Embed(
            title=f"{유저.name}님의 지갑",
            description=f'현재 잔고: {money}원\n**연속 출석 횟수**: {daily_streak}',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=유저.avatar.url if 유저.avatar else discord.Embed.Empty)

        # Create a button
        view = discord.ui.View()
        button = discord.ui.Button(label="서포트 서버", url='https://discord.gg/8xZtuQ5rsr')
        view.add_item(button)
        await ctx.respond(embed=embed, view=view)

    except Exception as e:
        await ctx.respond(f"오류 발생: {str(e)}")

# 유저 정보 가져오기 함수
def get_user_info(user_id):
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        user_data = json.load(file)
    return user_data.get(str(user_id), {"money": 0, "daily_streak": 0})

@bot.slash_command(description="도박을 해요!")
@discord.option(name='베팅액', description='베팅할 금액을 입력해주세요!')
async def 도박(ctx, 베팅액: int):
    try:
        user_id = str(ctx.author.id)

        # 사용자 데이터 불러오기
        user_data = load_user_data()

        if user_id not in user_data:
            embed = discord.Embed(
                title='도박 실패',
                description='가입되어 있지 않습니다. 가입을 먼저 해주세요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        if 베팅액 <= 0:
            await ctx.respond("베팅액은 양수여야 해요!", ephemeral=True)
            return

        if 베팅액 < 1000:
            await ctx.respond("베팅액은 최소 1,000원 이상이어야 해요!", ephemeral=True)
            return

        if user_data[user_id]['money'] < 베팅액:
            embed = discord.Embed(
                title='도박 실패',
                description='소지한 금액보다 많은 금액을 베팅할 수 없습니다.',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        # 도박 결과 계산
        win_probability = 0.5  # 50% 확률 예시
        if random.random() <= win_probability:
            result = 'win'
            user_data[user_id]['money'] += 베팅액
        else:
            result = 'lose'
            user_data[user_id]['money'] -= 베팅액

        # 사용자 데이터 저장
        save_user_data(user_data)

        if result == 'win':
            description = f'베팅 성공으로 {베팅액}원을 얻었습니다!'
            color = discord.Color.green()
        else:
            description = f'베팅 실패로 {베팅액}원을 잃었습니다..'
            color = discord.Color.red()

        embed = discord.Embed(
            title='도박 결과',
            description=description,
            color=color
        )
        await ctx.respond(embed=embed)

    except Exception as e:
        print(f"An error occurred in gamble command: {e}")
        embed = discord.Embed(
            title='오류 발생',
            description=f'명령어 처리 중 오류가 발생했습니다: {e}',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

@bot.slash_command(description="출석체크를 해 돈을 받아요!")
async def 출첵(ctx):
    try:
        user_id = str(ctx.author.id)

        # 사용자 데이터 불러오기
        user_data = load_user_data()

        if user_id not in user_data:
            embed = discord.Embed(
                title='출석체크 실패',
                description='도박 서비스에 가입되지 않아 출석체크를 실패했습니다! /`/가입` 명령어로 가입할 수 있어요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        now = datetime.now()
        last_check_in = user_data[user_id].get('last_check_in')

        if last_check_in:
            last_check_in = datetime.fromisoformat(last_check_in)

        if last_check_in and (now - last_check_in).days < 1:
            embed = discord.Embed(
                title='출석체크 실패',
                description='오늘은 이미 출석체크를 완료하셨어요! / 내일 다시 시도해주세요!',
                color=discord.Color.red()
            )
        else:
            reward_amount = random.randint(2000, 5000)  # 임의의 출석체크 보상 설정
            user_data[user_id]['money'] += reward_amount
            user_data[user_id]['last_check_in'] = now.isoformat()
            save_user_data(user_data)
            embed = discord.Embed(
                title='출석체크 완료',
                description=f'출석체크를 완료했습니다! 출석 보상으로 {reward_amount}원을 받았어요!',
                color=discord.Color.green()
            )

        await ctx.respond(embed=embed)
    except Exception as e:
        print(f"An error occurred in check_in command: {e}")
        embed = discord.Embed(
            title='오류 발생',
            description=f'명령어 처리 중 오류가 발생했습니다: {e}',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
            
# 잔고 설정 명령어
@bot.slash_command(description="멘션한 유저의 금액을 조정해요!")
@commands.is_owner()
@discord.option(name='유저', description='금액을 조정할 유저를 멘션해주세요.', type=discord.User)
@discord.option(name='금액', description='조정할 금액을 입력해주세요.', type=int)
async def set_balance(ctx, 유저: discord.User, 금액: int):
    user_id = str(유저.id)

    # 사용자 데이터 불러오기
    user_data = load_user_data()

    if user_id not in user_data:
        embed = discord.Embed(
            title='오류',
            description='해당 사용자는 가입되지 않은 상태입니다.',
            color=discord.Color.red()
        )
    else:
        user_data[user_id]['money'] = 금액
        save_user_data(user_data)

        embed = discord.Embed(
            title='잔고 설정 완료',
            description=f'{유저}님의 잔고를 {금액}원으로 설정했습니다!',
            color=discord.Color.green()
        )

    await ctx.respond(embed=embed)

# 사용자 데이터 리셋 명령어 (개발자 전용)
@bot.slash_command(description="공지를 전송해요!")
async def reset_data(ctx, 유저: discord.User):
    if str(ctx.author.id) != DEVELOPER_ID:
        embed = discord.Embed(
            title='권한 부족',
            description='이 명령어는 개발자 전용입니다. / 데이터 리셋이 필요하신 경우 서포트 서버에서 문의를 넣어주세요. ',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return

    user_id = str(유저.id)

    # 사용자 데이터 불러오기
    user_data = load_user_data()

    if user_id not in user_data:
        embed = discord.Embed(
            title='오류',
            description='해당 사용자는 가입되지 않은 상태입니다.',
            color=discord.Color.red()
        )
    else:
        del user_data[user_id]
        save_user_data(user_data)

        embed = discord.Embed(
            title='데이터 리셋 완료',
            description=f'{유저}님의 데이터를 초기화했습니다.',
            color=discord.Color.green()
        )

    await ctx.respond(embed=embed)
    
@bot.slash_command(description="멘션한 유저에게 송금을 해요!")
@discord.option(name='유저', description='송금할 유저를 멘션해주세요!')
@discord.option(name='금액', description='송금할 금액을 입력해주세요!')
async def 송금(ctx, 유저: discord.User, 금액: int):
    try:
        user_id = str(ctx.author.id)
        target_user_id = str(유저.id)
        user_data = load_user_data()

        if user_id not in user_data:
            embed = discord.Embed(
                title='송금 실패',
                description='도박 서비스에 가입되지 않아 출석체크를 실패했습니다! / `/가입` 명령어로 가입할 수 있어요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        if target_user_id not in user_data:
            embed = discord.Embed(
                title='송금 실패',
                description='대상 사용자가 가입되어 있지 않아요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        if 금액 <= 0:
            embed = discord.Embed(
                title='송금 실패',
                description='1 이상의 금액을 입력해주세요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        if user_data[user_id]['money'] < 금액:
            embed = discord.Embed(
                title='송금 실패',
                description='소지한 금액보다 많은 금액을 송금할 수 없어요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        user_data[user_id]['money'] -= 금액
        user_data[target_user_id]['money'] += 금액
        save_user_data(user_data)

        embed = discord.Embed(
            title='송금 성공',
            description=f'{유저}님에게 {금액}원을 송금했어요!',
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title='오류 발생',
            description=f'명령어 처리 중 오류가 발생했습니다: {e}',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)     

@bot.slash_command(description="일일 퀴즈를 풀어 돈을 받아요!!")
async def 일일퀴즈(ctx):
    try:
        user_id = str(ctx.author.id)
        user_data = load_user_data()

        if user_id not in user_data:
            embed = discord.Embed(
                title='퀴즈 실패',
                description='도박 서비스에 가입되지 않아 퀴즈 질문 생성을 실패했습니다! / `/가입` 명령어로 가입할 수 있어요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        now = datetime.now()
        last_quiz = user_data[user_id].get('last_quiz')

        if last_quiz and (now - datetime.fromisoformat(last_quiz)).days < 1:
            embed = discord.Embed(
                title='퀴즈 실패',
                description='오늘 이미 퀴즈를 참여하셨어요! 내일 다시 시도해주세요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        quiz_questions = [
            {"question": "1+1은?", "answer": "2"},
            {"question": "3 X 3은?", "answer": "9"},
            {"qusetion": "하니의 소속 그룹은?", "answer": "뉴진스"},
            {"qusetion": "뉴진스의 소속사는?", "answer": "ADOR"},
            {"question": "뉴진스의 팬덤 (팬 애칭)은?", "answer": "버니즈"},
            {"question": "대한민국의 수도는?", "answer": "서울"},
        ]

        quiz = random.choice(quiz_questions)
        embed = discord.Embed(
            title='일일 퀴즈 (해당 메세지에 멘션답장을 해 정답을 입력해주세요!)',
            description=quiz["question"],
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            msg = await bot.wait_for('messaghttps://discord.com/developers/applicationse', check=check, timeout=30)
            if msg.content == quiz["answer"]:
                reward_amount = random.randint(2000, 5000)
                user_data[user_id]['money'] += reward_amount
                user_data[user_id]['last_quiz'] = now.isoformat()
                save_user_data(user_data)
                embed = discord.Embed(
                    title='퀴즈 성공',
                    description=f'정답입니다! {reward_amount}원을 보상으로 받았어요!',
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title='퀴즈 실패',
                    description='오답입니다! 다음 기회에 도전해주세요!',
                    color=discord.Color.red()
                )
            await ctx.respond(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title='퀴즈 실패',
                description='시간 초과입니다! 다음 기회에 도전해주세요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title='오류 발생',
            description=f'명령어 처리 중 오류가 발생했습니다: {e}',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

@bot.slash_command(description="베팅한 금액으로 주사위를 돌려요!")
@discord.option(name='베팅액', description='베팅할 금액을 입력해주세요!')
async def 주사위(ctx, 베팅액: int):
    try:
        user_id = str(ctx.author.id)
        user_data = load_user_data()

        if user_id not in user_data:
            embed = discord.Embed(
                title='도박 실패',
                description='도박 서비스에 가입되지 않아 주사위를 던지지 못했어요! / `하니야 가입` 명령어로 가입할 수 있어요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return
        
        if 베팅액 <= 0:
            await ctx.respond("베팅액은 양수여야 해요!", ephemeral=True)
            return

        if 베팅액 < 1000:
            await ctx.respond("베팅액은 최소 1,000원 이상이어야 해요!", ephemeral=True)
            return

        if user_data[user_id]['money'] < 베팅액:
            embed = discord.Embed(
                title='도박 실패',
                description='소지한 금액보다 많은 금액을 베팅할 수 없어요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        dice_roll = random.randint(1, 6)
        if dice_roll == 베팅액:
            winnings = 베팅액 * 6
            user_data[user_id]['money'] += winnings
            description = f'주사위가 {dice_roll}이 나와서 {winnings}원을 얻었습니다!'
            color = discord.Color.green()
        else:
            user_data[user_id]['money'] -= 베팅액
            description = f'주사위가 {dice_roll}이 나와서 {베팅액}원을 잃었습니다..'
            color = discord.Color.red()

        save_user_data(user_data)
        embed = discord.Embed(
            title='베팅 결과',
            description=description,
            color=color
        )
        await ctx.respond(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title='오류 발생',
            description=f'명령어 처리 중 오류가 발생했습니다: {e}',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

@bot.slash_command(description="베팅한 금액으로 슬롯머신을 돌려요!")
@discord.option(name='베팅액', description='베팅할 금액을 입력해주세요!')
async def 슬롯머신(ctx, 베팅액: int):
    try:
        user_id = str(ctx.author.id)
        user_data = load_user_data()

        if user_id not in user_data:
            embed = discord.Embed(
                title='도박 실패',
                description='도박 서비스에 가입되지 않아 슬롯 머신을 플레이하지 못했어요! / `/가입` 명령어로 가입할 수 있어요!',
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        if 베팅액 <= 0:
            await ctx.respond("베팅액은 양수여야 해요!", ephemeral=True)
            return

        if 베팅액 < 1000:
            await ctx.respond("베팅액은 최소 1,000원 이상이어야 해요!", ephemeral=True)
            return

        if user_data[user_id]['money'] < 베팅액:
            embed = discord.Embed(
                title='도박 실패',
                description='소지한 금액보다 많은 금액을 베팅할 수 없어요!',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        symbols = ['🍒', '🍋', '🍇', '🍉', '🍊']
        slot1 = random.choice(symbols)
        slot2 = random.choice(symbols)
        slot3 = random.choice(symbols)

        if slot1 == slot2 == slot3:
            winnings = 베팅액 * 5
            user_data[user_id]['money'] += winnings
            description = f'슬롯 머신 결과: {slot1} {slot2} {slot3}. / 모두 동일하여 {winnings}원을 얻었습니다!'
            color = discord.Color.green()
        else:
            user_data[user_id]['money'] -= 베팅액
            description = f'슬롯 머신 결과: {slot1} {slot2} {slot3}. / 일치하지 않아서 {베팅액}원을 잃었습니다..'
            color = discord.Color.red()

        save_user_data(user_data)
        embed = discord.Embed(
            title='베팅 결과',
            description=description,
            color=color
        )
        await ctx.respond(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title='오류 발생',
            description=f'명령어 처리 중 오류가 발생했습니다: {e}',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed) 

class RouletteView(discord.ui.View):
    def __init__(self, ctx, amount):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.amount = amount
        self.result = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

    @discord.ui.button(label="빨간색", style=discord.ButtonStyle.red)
    async def red_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_bet("빨간색")

    @discord.ui.button(label="검은색", style=discord.ButtonStyle.grey)
    async def black_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_bet("검은색")

    @discord.ui.button(label="초록색", style=discord.ButtonStyle.green)
    async def green_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_bet("초록색")

    async def handle_bet(self, color):
        colors = ["빨간색", "검은색", "초록색"]
        result = random.choice(colors)

        guild_data = get_guild_data(self.ctx.guild.id)
        user_balance = guild_data["balances"].get(self.ctx.author.id, 1000)

        if result == color:
            winnings = self.amount * (14 if color == "초록색" else 2)
            guild_data["balances"][self.ctx.author.id] = user_balance + winnings
            await self.ctx.respond(f'룰렛 결과: {result}!ㅣ{winnings}원을 얻으셨어요!')
        else:
            guild_data["balances"][self.ctx.author.id] = user_balance - self.amount
            await self.ctx.respond(f'룰렛 결과: {result}!ㅣ{self.amount}원을 잃으셨어요.')

        self.stop()
# 룰렛
@bot.slash_command(description="룰렛을 돌려요!")
@discord.option(name='베팅액', description='베팅할 금액을 입력해주세요!')
async def 룰렛(ctx, 베팅액: int):
    guild_data = get_guild_data(ctx.guild.id)
    user_balance = guild_data["balances"].get(ctx.author.id, 10000)

    if 베팅액 > user_balance:
        await ctx.respond   (f'잔액이 부족해요! 현재 잔액: {user_balance}')
        return
    
    if 베팅액 <= 0:
        await ctx.respond("베팅액은 양수여야 해요!", ephemeral=True)
        return

    if 베팅액 < 1000:
        await ctx.respond("베팅액은 최소 1,000원 이상이어야 해요!", ephemeral=True)
        return
    
    view = RouletteView(ctx, 베팅액)
    await ctx.respond("베팅할 색깔을 선택해주세요!", view=view)

@bot.event
async def on_guild_join(guild):
    # 서버에 추가되었을 때 서버 수를 전송
    guild_count = len(bot.guilds)
    channel = bot.get_channel(1259363829058502746)  # 서버 수를 전송할 채널 ID를 넣으세요
    if channel:
        await channel.send(f'**> 현재 서버 수: `{guild_count}`**')

@bot.event
async def on_guild_remove(guild):
    # 서버에서 제거되었을 때 서버 수를 전송
    guild_count = len(bot.guilds)
    channel = bot.get_channel(1259363829058502746)  # 서버 수를 전송할 채널 ID를 넣으세요
    if channel:
        await channel.send(f'**> 현재 서버 수: `{guild_count}`**')

   
@tasks.loop(hours=3)
async def update_koreanbots():
    await bot.wait_until_ready()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://koreanbots.dev/api/v2/bots/{bot.user.id}/stats",
            json={"servers": len(bot.guilds), "shards": len(bot.shards)},
            headers={"Authorization": KOREANBOTS_AUTH},
        ) as res:
            if res.status != 200:
                error_message = (await res.json()).get('message', 'Unknown error')
                print(f":x: | 한디리 서버수 업데이트 실패 ({error_message})")
                channel = bot.get_channel(CHANNEL_ID)
                if channel:
                    await channel.send(f":x: | 한디리 서버수 업데이트 실패 (``{error_message}``)")
            else:
                success_message = (await res.json()).get('message', 'Success')
                print(f":white_check_mark: | 한디리 서버수 업데이트 성공")
                channel = bot.get_channel(CHANNEL_ID)
                if channel:
                    await channel.send(f":white_check_mark: | 한디리 서버수 업데이트 성공!")

@bot.slash_command(description="로또를 구매합니다!")
@discord.option(name='수량', description='구매할 로또 수를 입력해주세요!', type=int, min_value=1)
async def 로또(ctx, 수량: int):
    user_id = str(ctx.author.id)
    user_data = load_user_data()

    if user_id not in user_data:
        embed = discord.Embed(
            title='오류',
            description='도박 서비스에 가입되지 않은 상태입니다. `/가입` 명령어로 가입해주세요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return

    # 기본 값이 None일 수 있는 경우 처리
    user_money = user_data[user_id].get('money', 0)  # 기본값을 0으로 설정
    if user_money is None:
        user_money = 0

    total_cost = 1000 * 수량
    if user_money < total_cost:  # 로또 구매 최소 금액
        embed = discord.Embed(
            title='오류',
            description=f'잔액이 부족합니다. 최소 {total_cost}원부터 로또를 구매할 수 있습니다.',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return

    # 로또 번호 생성 (1부터 45까지 중복 없는 번호 6개 선택)
    all_lotto_numbers = []
    for _ in range(수량):
        lotto_numbers = random.sample(range(1, 46), 6)
        all_lotto_numbers.append(lotto_numbers)

    user_data[user_id].setdefault('lotto', []).extend(all_lotto_numbers)
    user_data[user_id]['money'] -= total_cost  # 로또 구매 금액 차감
    save_user_data(user_data)

    embed = discord.Embed(
        title='로또 구매 완료',
        description=f'로또를 {수량}개를 성공적으로 구매했습니다! / 구매한 번호:\n' + '\n'.join([str(numbers) for numbers in all_lotto_numbers]) +
                    f'\n\n구매 후 잔액: {user_data[user_id]["money"]}원',
        color=discord.Color.green()
    )

    await ctx.respond(embed=embed)

@bot.slash_command(description="로또를 추첨합니다!")
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 3600, commands.BucketType.user)  # 1시간 쿨타임 설정
async def 로또추첨(ctx):
    user_id = str(ctx.author.id)
    user_data = load_user_data()

    if user_id not in user_data or 'lotto' not in user_data[user_id]:
        embed = discord.Embed(
            title='오류',
            description='해당 서버에서 로또를 구매한 기록을 찾을 수 없어요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return

    # 실제 로또 번호 추첨 (1부터 45까지 중복 없는 번호 6개 선택)
    winning_numbers = random.sample(range(1, 46), 6)

    # 사용자가 구매한 모든 로또 번호와 비교하여 당첨 번호 개수 세기
    results = []
    for lotto_numbers in user_data[user_id]['lotto']:
        match_count = len(set(lotto_numbers) & set(winning_numbers))
        results.append({
            'lotto_numbers': lotto_numbers,
            'match_count': match_count
        })

    # 결과를 사용자에게 보여주기
    embed = discord.Embed(
        title='로또 추첨 결과',
        description=f'당첨 번호: {winning_numbers}',
        color=discord.Color.blue()
    )

    for result in results:
        embed.add_field(
            name=f'구매한 번호: {result["lotto_numbers"]}',
            value=f'일치 개수: {result["match_count"]} 개',
            inline=False
        )

    await ctx.respond(embed=embed)

    # 사용자 데이터에서 로또 정보 제거
    del user_data[user_id]['lotto']
    save_user_data(user_data)

# 쿨다운 예외 처리
@로또추첨.error
async def 로또추첨_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        retry_after = round(error.retry_after, 2)
        minutes, seconds = divmod(retry_after, 60)
        await ctx.respond(f"쿨타임이 적용중이에요 `{int(minutes)}`분 `{int(seconds)}`초 후에 다시 시도해주세요!")
    else:
        await ctx.respond("오류가 발생했습니다. 다시 시도해 주세요.")

def load_json(file):
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        return {}
    with open(file, 'r') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

user_blacklist = load_json(USER_BLACKLIST_FILE)
server_blacklist = load_json(SERVER_BLACKLIST_FILE)

def is_user_blacklisted(user_id):
    return str(user_id) in user_blacklist

def is_server_blacklisted(server_id):
    return str(server_id) in server_blacklist

def warn_user(user_id):
    if user_id not in user_blacklist:
        user_blacklist[user_id] = {'warnings': 0, 'reason': ''}
    user_blacklist[user_id]['warnings'] += 1
    save_json(USER_BLACKLIST_FILE, user_blacklist)

def clear_user_warnings(user_id):
    if user_id in user_blacklist:
        user_blacklist[user_id]['warnings'] = 0
        save_json(USER_BLACKLIST_FILE, user_blacklist)

async def log_blacklist_use(ctx, reason):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="Blacklisted User Attempted Command",
            description=f"User <@{ctx.author.id}> attempted to use a command but is blacklisted.",
            color=discord.Color.red()
        )
        await log_channel.send(embed=embed)

class ConfirmBlacklist(View):
    def __init__(self, server_id):
        super().__init__()
        self.server_id = server_id

    @discord.ui.button(label="블랙리스트 추가", style=discord.ButtonStyle.danger)
    async def confirm(self, button: Button, interaction: discord.Interaction):
        # 블랙리스트에 서버 ID가 이미 있는지 확인
        if str(self.server_id) in server_blacklist:
            await interaction.response.send_message(f"Server {self.server_id} is already blacklisted.", ephemeral=True)
        else:
            server_blacklist[str(self.server_id)] = {}
            save_json(SERVER_BLACKLIST_FILE, server_blacklist)
            await interaction.response.send_message(f"Server {self.server_id} has been blacklisted.", ephemeral=True)
            try:
                guild = await bot.fetch_guild(self.server_id)
                await guild.leave()
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to leave this server.", ephemeral=True)
            except discord.HTTPException as e:
                await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @discord.ui.button(label="취소", style=discord.ButtonStyle.secondary)
    async def cancel(self, button: Button, interaction: discord.Interaction):
        await interaction.response.send_message("Blacklist action cancelled.", ephemeral=True)

async def handle_warning(ctx):
    user_id = str(ctx.author.id)
    warn_user(user_id)
    warnings = user_blacklist[user_id]['warnings']

    if warnings >= 3:
        embed = discord.Embed(
            title="User Reached Maximum Warnings",
            description=f"User <@{ctx.author.id}> has reached the maximum number of warnings.",
            color=discord.Color.red()
        )
        admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
        invite = await ctx.channel.create_invite(max_age=300)
        embed.add_field(name="Server Invite", value=invite.url)
        view = ConfirmBlacklist(ctx.guild.id)
        await admin_channel.send(embed=embed, view=view)
        clear_user_warnings(user_id)

async def on_application_command(self, ctx):
        try:
            if is_user_blacklisted(ctx.author.id):
                await log_blacklist_use(ctx, "블랙리스트에 등록되어 있어 명령어를 사용하실 수 없습니다..")
                await handle_warning(ctx)
                return
            await self.process_application_commands(ctx)
        except Exception as e:
            await self.send_error_to_webhook(ctx, e)
            raise  # 원래의 예외를 다시 발생시켜 기본 오류 처리기가 처리할 수 있게 합니다

@bot.slash_command(description="Add a user to the blacklist")
async def add_blacklist(ctx, user: discord.User, reason: str):
    user_blacklist[str(user.id)] = {'warnings': 0, 'reason': reason}
    save_json(USER_BLACKLIST_FILE, user_blacklist)
    await ctx.respond(f"User {user.mention} has been added to the blacklist for: {reason}")

@bot.slash_command(description="Remove a user from the blacklist")
async def remove_blacklist(ctx, user: discord.User):
    if str(user.id) in user_blacklist:
        del user_blacklist[str(user.id)]
        save_json(USER_BLACKLIST_FILE, user_blacklist)
        await ctx.respond(f"User {user.mention} has been removed from the blacklist.")
    else:
        await ctx.respond(f"User {user.mention} is not in the blacklist.")

@bot.slash_command(description="블랙잭을 즐겨보세요!")
@discord.option(name='베팅액', type=int, description='베팅할 금액을 입력하세요.')
async def 블랙잭(ctx, 베팅액: int):
    user_id = str(ctx.author.id)
    user_data = load_user_data()

    if user_id not in user_data:
        embed = discord.Embed(
            title='게임 시작 실패',
            description='도박 서비스에 가입되지 않아 게임을 진행할 수 없습니다! `/가입` 명령어로 가입할 수 있어요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return

    if 베팅액 <= 0:
        await ctx.respond("베팅액은 양수여야 해요!", ephemeral=True)
        return

    if 베팅액 < 1000:
        await ctx.respond("베팅액은 최소 1,000원 이상이어야 해요!", ephemeral=True)
        return

    if user_data[user_id]['money'] < 베팅액:
        await ctx.respond("잔액이 부족해 베팅을 실패하였어요!")
        return

    # 블랙잭 게임 로직
    def draw_card(deck):
        return deck.pop()

    def calculate_hand(hand):
        value = 0
        aces = 0
        for card in hand:
            if card[0] in 'TJQK':
                value += 10
            elif card[0] == 'A':
                value += 11
                aces += 1
            else:
                value += int(card[0])
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    deck = [f'{rank}{suit}' for rank in '23456789TJQKA' for suit in 'CDHS']
    random.shuffle(deck)

    player_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]

    player_value = calculate_hand(player_hand)
    dealer_value = calculate_hand(dealer_hand)

    embed = discord.Embed(title="블랙잭")
    embed.add_field(name="플레이어의 핸드", value=f"{player_hand[0]} {player_hand[1]} (합: {player_value})")
    embed.add_field(name="딜러의 핸드", value=f"{dealer_hand[0]} ?")

    result = ""

    if player_value == 21:
        reward_amount = 베팅액 * 2
        user_data[user_id]['money'] += 베팅액  # 베팅액만 추가 (이미 가지고 있던 돈에 베팅액만큼 추가)
        result = f"플레이어 승리! / {reward_amount}원을 획득했어요!"
    else:
        while dealer_value < 17:
            dealer_hand.append(draw_card(deck))
            dealer_value = calculate_hand(dealer_hand)
        
        if dealer_value > 21 or player_value > dealer_value:
            reward_amount = 베팅액 * 2
            user_data[user_id]['money'] += 베팅액  # 베팅액만 추가
            result = f"유저 승리! / {reward_amount}원을 획득했어요!"
        elif player_value < dealer_value:
            user_data[user_id]['money'] -= 베팅액
            result = f"딜러 승리!  / {베팅액}원을 잃으셨어요.."
        else:
            result = "무승부!"

    embed.add_field(name="결과", value=result)
    embed.add_field(name="딜러의 최종 핸드", value=f"{' '.join(dealer_hand)} (합: {dealer_value})")
    embed.add_field(name="남은 금액", value=f"{user_data[user_id]['money']}원")

    save_user_data(user_data)

    await ctx.respond(embed=embed)

@bot.slash_command(description="포커를 즐겨보세요!")
@discord.option(name='베팅금액', type=int, description='베팅할 금액을 입력해주세요!')
async def 포커(ctx, 베팅액: int):
    user_id = str(ctx.author.id)
    user_data = load_user_data()

    if user_id not in user_data:
        embed = discord.Embed(
            title='게임 시작 실패',
            description='도박 서비스에 가입되지 않아 게임을 진행할 수 없네요! / `/가입` 명령어로 가입할 수 있어요!',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return

    if 베팅액 <= 0:
        await ctx.respond("베팅액은 양수여야 해요!", ephemeral=True)
        return

    if 베팅액 < 1000:
        await ctx.respond("베팅액은 최소 1,000원 이상이어야 해요!", ephemeral=True)
        return

    if user_data[user_id]['money'] < 베팅액:
        await ctx.respond("잔액이 부족해 베팅을 실패하였어요!")
        return

    deck = [f'{rank}{suit}' for rank in '23456789TJQKA' for suit in 'CDHS']
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop()]
    bot_hand = [deck.pop(), deck.pop()]
    community_cards = [deck.pop() for _ in range(5)]

    # 승리 여부를 판단하는 간단한 로직 추가 (예시로 무작위 승패 결정)
    player_wins = random.choice([True, False])

    if player_wins:
        reward_amount = 베팅액 * 2
        user_data[user_id]['money'] += 베팅액  # 베팅액만 추가 (이미 가지고 있던 돈에 베팅액만큼 추가)
        result = f"승리! / {reward_amount}원을 획득하셨어요!"
    else:
        user_data[user_id]['money'] -= 베팅액
        result = f"봇이 승리하였어요. / {베팅액}원을 잃으셨어요.."

    save_user_data(user_data)

    embed = discord.Embed(title="포커")
    embed.add_field(name="플레이어의 핸드", value=f"{player_hand[0]} {player_hand[1]}")
    embed.add_field(name="커뮤니티 카드", value=' '.join(community_cards))
    embed.add_field(name="결과", value=result)
    embed.add_field(name="남은 금액", value=f"{user_data[user_id]['money']}원")

    await ctx.respond(embed=embed)

@bot.slash_command(description="채널을 잠궈 채팅을 막아요!")
@discord.option(name='채널', type=discord.TextChannel, description='잠글 채널을 멘션해주세요!')
async def 채널잠금(ctx, 채널: discord.TextChannel):
    # 관리자 권한 확인
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="권한 부족",
            description="이 명령어를 사용하려면 관리자 권한이 필요해요.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)  # 에페메랄 응답으로 비공개
        return

    overwrite = 채널.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await 채널.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    # 채널 잠금 성공 메시지
    embed = discord.Embed(
        title="채널 잠금",
        description=f"{채널.mention} 채널을 성공적으로 잠궜어요!",
        color=discord.Color.blue()
    )
    await ctx.respond(embed=embed)

@bot.slash_command(description="버그를 제보하실수 있어요!")
@discord.option("타입", description="버그의 타입을 선택해주세요!", choices=["오류", "버그", "건의사항"])
@discord.option("내용", description="버그의 내용을 입력해주세요!")
async def 버그제보(ctx, 타입: str, 내용: str):
    developer = await bot.fetch_user(DEVELOPER_IDS)

    embed = discord.Embed(title="버그 제보", color=discord.Color.red(), timestamp=datetime.now())
    embed.add_field(name="제보한 유저", value=ctx.author.mention, inline=True)
    embed.add_field(name="버그 타입", value=타입, inline=True)
    embed.add_field(name="오류 내용", value=내용, inline=True)

    try:
        await developer.send(embed=embed)
        await ctx.respond("최대한 빠른 시일 내에 버그를 수정하도록 하겠습니다! / 버그를 제보해주셔서 감사합니다!", ephemeral=True)
    except discord.HTTPException:
        await ctx.respond("버그를 제보하는중 오류가 발생했어요...", kek=True)# 웹훅 URL 설정

async def send_error_to_webhook(error_message):
    async with aiohttp.ClientSession() as session:
        webhook_data = {
            "content": f"**Error**:\ns{error_message}"
        }
        async with session.post(WEBHOOK_URL, json=webhook_data) as response:
            if response.status != 204:
                print(f"Failed to send webhook. Status code: {response.status}")
                
@bot.event
async def on_presence_update(before, after):
    if before.status != after.status:
        if after.status == discord.Status.online:
            online_records[after.id] = {'start': int(time.time()), 'end': None}
        elif after.status == discord.Status.offline and after.id in online_records:
            online_records[after.id]['end'] = int(time.time())


# @bot.slash_command(name="온라인기록", description="사용자의 온라인 기록을 확인합니다.")
# async def check_online_record(ctx):
#     user_id = ctx.author.id
#     if user_id in online_records:
#         start = online_records[user_id]['start']
#         end = online_records[user_id]['end']
#         
#         embed = discord.Embed(title="온라인 기록", color=discord.Color.blue())
#         embed.add_field(name="시작", value=f"<t:{start}:F>", inline=True)
#         
#         if end:
#             embed.add_field(name="오프라인 시간", value=f"<t:{end}:F>", inline=True)
#             embed.add_field(name="오프라인 지속 시간", value=f"<t:{end}:R>", inline=True)
#         else:
#             current_time = int(time.time())
#             embed.add_field(name="현재 상태", value="온라인", inline=False)
#             embed.add_field(name="현재 온라인 지속 시간", value=f"<t:{start}:R}", inline=True)
#         
#         await ctx.respond(embed=embed)
#     else:
#         await ctx.respond("온라인 기록이 없습니다.")
# 
# @bot.slash_command(name="채널설정", description="입장 로그를 받을 채널을 설정해요!")
# async def set_channel(ctx: discord.ApplicationContext, channel: discord.TextChannel):
#     settings['notification_channel_id'] = channel.id
#     settings['notification_enabled'] = True  # 채널 설정 후 알림 활성화
#     save_settings(settings)  # 설정을 파일에 저장
#     await ctx.respond(f"입장 로그를 {channel.mention} 채널로 설정했어요!")
# 
# @bot.slash_command(name="입장로그", description="최근 입장 로그를 확인해요!")
# async def show_join_logs(ctx: discord.ApplicationContext):
#     if not join_logs:
#         await ctx.respond("현재 입장 로그가 없어요!")
#         return
# 
#     embed = discord.Embed(
#         title="최근 입장 로그",
#         description="최근 유저가 입장한 로그에요!",
#         color=discord.Color.blue()
#     )
#     
#     for log in join_logs:
#         embed.add_field(name=log['timestamp'], value=log['message'], inline=False)
# 
#     await ctx.respond(embed=embed)
# 
# @bot.event
# async def on_member_join(member: discord.Member):
#     # 설정된 채널이 있는 서버인지 확인
#     if settings['notification_channel_id'] and settings['notification_enabled']:
#         channel = bot.get_channel(settings['notification_channel_id'])
#         
#         if channel and channel.guild == member.guild:
#             # 현재 시간을 유닉스 타임스탬프로 변환
#             unix_timestamp = int(discord.utils.utcnow().timestamp())
#             
#             member_count = len(member.guild.members)
# 
#             # 아바타 URL 확인 및 기본 이미지 설정
#             avatar_url = member.display_avatar.url if member.display_avatar else 'https://cdn.discordapp.com/embed/avatars/0.png'
# 
#             embed = discord.Embed(
#                 title="{member_count}번째 유저가 입장했어요!",
#                 description=f"{member.display_name}님이 {member.guild.name} 서버에 입장하셨어요!",
#                 color=discord.Color.green()
#             )
#             embed.add_field(name="유저", value=member.display_name, inline=True)
#             embed.add_field(name="유저 ID", value=member.id, inline=True)
#             embed.add_field(name="서버에 입장한 시간", value=f"<t:{unix_timestamp}:F>", inline=True)  # 포맷 옵션: 'F' (전체 날짜)
#             embed.set_thumbnail(url=avatar_url)
# 
#             await channel.send(embed=embed)
# 
#             # 입장 로그를 기록합니다.
#             timestamp = int(discord.utils.utcnow().timestamp())
#             join_logs.append({
#                 'timestamp': f"<t:{timestamp}:F>",
#                 'message': (
#                     f"**유저 이름**: {member.display_name}\n"
#                     f"**유저 ID**: {member.id}\n"
#                     f"**입장 시간**: <t:{timestamp}:F>"
#                 )
#             })
# 
#             # 입장 로그가 너무 많아지지 않도록, 예를 들어 최근 10개의 로그만 보관합니다.
#             if len(join_logs) > 10:
#                 join_logs.pop(0)

@bot.event
async def on_error(event, *args, **kwargs):
    error = traceback.format_exc()
    await send_error_to_webhook(error)
    
bot.load_extension('jejudo')
bot.run(TOKEN)
