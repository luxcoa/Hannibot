import discord
from discord.ext import commands, tasks
from discord.ui import Select, View
import random
import datetime
from datetime import datetime, timedelta
import time
import re
import os

intents = discord.Intents.default()
intents.message_content = True # 사용자의 메세지를 읽고 처리하려면 필요
intents.presences = True # 봇 상태 업데이트 때문에 필요
intents.guild_messages = True # 청소 기능 때문에 필요
intents.guilds = True # 상태에 서버 수 업데이트를 위해 필요
intents.members = True # 개발자 ID 때문에 필요
client = discord.Client(intents=intents)
start_time = datetime.datetime.now()
client = commands.AutoShardedBot(command_prefix='민정아', intents=intents)

# 봇이 부팅한 시간 기록
boot_time = datetime.datetime.now()

# 에스파의 곡 목록
aespa_songs = [
    "Black Mamba", "Supernova", "Long chat", "목소리 (Melody)",
    "Live My Life", "Prologue", "BAHAMA", "Licorice", "Mine",
    "Set The Tone", "자각몽", "I'll Make You Cry", "Lucid Dream",
    "ICONIC", "Jingle Bell Rock", "Salty & Sweet", "Thirsty",
    "ICU (쉬어가도 돼)", "We GO", "With you", "ZOOM ZOOM", "Get Coin",
    "시대유감 (時代遺憾) (2024 aespa Remake Ver.)", "Trick or Trick",
    "Hot Air Balloon", "Don't Blink", "YOLO", "You", "I'm Unhappy"
]

# 초대 링크와 특정 유저 ID를 여기에 입력합니다.
INVITE_LINK = 'https://discord.gg/UfHSqhcj2j'
SPECIFIC_USER_IDS = ['837570564536270848', '3231313312']

# 개발자 정보
DEVELOPER_ID = '837570564536270848'
BOT_VERSION = '2.0.9'

@client.event
async def on_ready():
    print(f"봇에 로그인을 성공했습니다!")
    print(f"봇 이름: {client.user.name}")
    print(f"봇 아이디: {client.user.id}")
    update_status.start()

status_index = 0

@tasks.loop(seconds=20)
async def update_status():
    global status_index
    server_count = len(client.guilds)
    
    status_messages = [
        discord.Game('접두사: 민정아'),
        discord.Game(f'{server_count}개의 서버에서 일')
    ]
    
    await client.change_presence(activity=status_messages[status_index])
    status_index = (status_index + 1) % len(status_messages)

class CommandSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="정보", description="다양한 정보 명령어들입니다."),
            discord.SelectOption(label="뮤비", description="다양한 뮤비 관련 명령어들입니다."),
            discord.SelectOption(label="유틸리티", description="다양한 유틸리티 명령어들입니다.")
        ]
        super().__init__(placeholder="명령어 카테고리를 선택하세요.", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "정보":
            embed = discord.Embed(title="정보 명령어", description="윈터봇의 다양한 소개 명령어들입니다.", color=0x0082ff)
            embed.add_field(name="민정아 소개해", value="윈터에 대한 소개를 해요!", inline=True)
            embed.add_field(name="민정아 개발자", value="저를 만드신 개발자의 정보를 알려드려요!", inline=True)
            embed.add_field(name="민정아 데뷔일", value="에스파의 데뷔일을 알려드려요!", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif self.values[0] == "뮤비":
            embed = discord.Embed(title="뮤비 명령어", description="에스파의 다양한 뮤비 명령어들입니다.", color=0x0082ff)
            embed.add_field(name="민정아 최신곡", value="에스파의 최신곡 뮤비 링크를 보내요!", inline=True)
            embed.add_field(name="민정아 이전곡", value="최신곡의 바로 이전 곡의 뮤비 링크를 보내요!", inline=True)
            embed.add_field(name="민정아 데뷔곡", value="에스파의 데뷔 곡 뮤비 링크를 보내요!", inline=True)
            embed.add_field(name="민정아 아마겟돈", value="아마겟돈 퍼포먼스 영상 링크를 보내요!", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "유틸리티":
            embed = discord.Embed(title="유틸리티 명령어", description="윈터봇의 다양한 유틸 명령어들입니다.", color=0x0082ff)
            embed.add_field(name="민정아 핑", value="윈터봇의 핑을 전송해요!")
            embed.add_field(name="민정아 추천해줘", value="에스파의 노래 중 하나의 곡을 추천해드려요!", inline=True)
            embed.add_field(name="민정아 컴백일", value="에스파의 컴백일을 알려드려요!", inline=True)
            embed.add_field(name="민정아 청소해 (청소할 메세지)", value="지정한 갯수의 메세지를 청소해요! ( 봇 멈출수도 있음 )", inline=True)
            embed.add_field(name="민정아 귀여워", value=">_<", inline=True)
            embed.add_field(name="민정아 서버정보", value="서버의 정보를 알려드려요", inline=True)
            embed.add_field(name="민정아 부팅시간", value="윈터봇의 부팅시간을 전송해요!", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)

class CommandView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CommandSelect())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '민정아':
       embed = discord.Embed(title="카테고리를 선택하여 주세요!", description="원하시는 명령어 카테고리를 선택해주세요!", color=0x0082ff)
       view = CommandView()
       await message.channel.send(embed=embed, view=view)

    elif message.content == '민정아 소개':
        embed = discord.Embed(title="에스파 윈터 소개", description="윈터의 대한 소개에요!", color=0x0082ff)
        embed.add_field(name="활동명", value="윈터 (Winter)", inline=True)
        embed.add_field(name="본명", value="김민정 (金旼炡, Kim Min-jeong)", inline=True)
        embed.add_field(name="소속 그룹", value="에스파 (aespa)", inline=True)
        embed.add_field(name="출생", value="2001년 1월 1일 (23세)", inline=True)
        embed.add_field(name="본관", value="김해 김씨", inline=True)
        embed.add_field(name="신체", value="164cm, A형", inline=True)
        embed.add_field(name="소속사", value="SM 엔터테인먼트", inline=True)
        await message.channel.send(embed=embed)
        
    elif message.content == '민정아 개발자':
        user_id = '837570564536270848'
        user_mention = f'<@{user_id}>'
        embed = discord.Embed(title="윈터봇 개발자", description=f"저는 {user_mention}님이 개발하였어요!", color=0x0082ff)
        embed.add_field(name="문의 및 제안", value="[ 서포트 서버 ](https://discord.gg/Rcde2azr3X)", inline=True)
        await message.channel.send(embed=embed)
        
    elif message.content == '민정아 최신곡':
        embed = discord.Embed(title="에스파 최신곡", description="", color=0x030303)
        embed.add_field(name="", value="[최신곡](https://www.youtube.com/watch?v=0nPniUvUBfUc)", inline=True)
       
       # 썸네일 가져오기
        video_id = re.search(r'v=([^&]+)', embed.fields[0].value).group(1)
        Image_url = f"https://i.ytimg.com/vi/{'0nPniUvUBfUc'}/mqdefault.jpg"
        embed.set_image(url=Image_url)
        await message.channel.send(embed=embed)
        
    elif message.content == '민정아 이전곡':
        embed = discord.Embed(title="드라마", description=" 아마겟돈 발매 전 나온 드라마의 뮤비에요!", color=0xff0000)
        embed.add_field(name="뮤비 링크", value="[이전곡](https://www.youtube.com/watch?v=3CvJKTChsl4)", inline=True)
        
        # 썸네일 가져오기
        video_id = re.search(r'v=([^&]+)', embed.fields[0].value).group(1)
        Image_url = f"https://i.ytimg.com/vi/{'3CvJKTChsl4'}/mqdefault.jpg"
        embed.set_image(url=Image_url)
        await message.channel.send(embed=embed)

        
    elif message.content == '민정아 데뷔곡':
        embed = discord.Embed(title="데뷔곡", description="에스파의 데뷔 곡을 알려드릴게요!", color=0x030303)
        embed.add_field(name="데뷔 곡 뮤비 링크", value="[에스파 데뷔곡](https://www.youtube.com/watch?v=ZeerrnuLi5E)", inline=True)
        # 썸네일 가져오기
        video_id = re.search(r'v=([^&]+)', embed.fields[0].value).group(1)
        Image_url = f"https://i.ytimg.com/vi/{'ZeerrnuLi5E'}/mqdefault.jpg"
        embed.set_image(url=Image_url)
        await message.channel.send(embed=embed)

    elif message.content == '민정아 데뷔일':
        embed = discord.Embed(title="데뷔일", description="에스파의 데뷔일을 알려드려요!", color=0x00bffd)
        embed.add_field(name="데뷔일", value="2020년 11월 17일에 디지털 싱글 앨범 Black Mamba로 데뷔했어요!", inline=False)
        await message.channel.send(embed=embed)
        
    elif message.content == '민정아 노래추천':
        song = random.choice(aespa_songs)
        embed = discord.Embed(title="에스파 노래 추천", description=f"오늘은 **{song}** 이 곡 어떠세요?", color=0x0082ff)
        await message.channel.send(embed=embed)

    elif message.content == '민정아 컴백일':
        embed = discord.Embed(title="컴백일", description="에스파의 컴백일을 알려드릴게요!", color=0xffff00)
        embed.add_field(name="컴백일", value="2024년 5월 27일에 컴백했어요!", inline=True)
        await message.channel.send(embed=embed)
    
    elif message.content.startswith('민정아 청소해'):
        if message.author.guild_permissions.manage_messages:  # 메시지 관리 권한을 가진 사용자만 실행 가능
            try:
                amount = int(message.content.split()[2])  # 삭제할 메시지 수
                await message.channel.purge(limit=amount + 1)  # 메시지 삭제 (명령어 메시지 포함)
                embed = discord.Embed(description=f'{amount}개의 메시지가 삭제되었습니다. 이 메세지는 5초 뒤 삭제돼요!', color=0x0082ff)
                await message.channel.send(embed=embed, delete_after=5)  # 삭제 안내 메시지 전송 후 5초 후 삭제
            except ValueError:
                embed = discord.Embed(description='올바른 숫자를 입력해주세요!', color=0xff0000)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(description='아앗.. 메세지 관리 권한이 없으시네요!', color=0xff0000)
            await message.channel.send(embed=embed)
    
    elif message.content == '!tester':
        if str(message.author.id) in SPECIFIC_USER_IDS:
            try:
                embed = discord.Embed(title="Early Access Server Invite Link", description=f"[초대링크]({INVITE_LINK})", color=discord.Color.green())
                await message.author.send(embed=embed)
                await message.channel.send(f'{message.author.mention}님, DM을 확인해주세요!', delete_after=10)
            except discord.Forbidden:
                await message.channel.send(f'{message.author.mention}님, DM을 보낼 수 없습니다. DM이 열려 있는지 확인해주세요.', delete_after=10)
        else:
            await message.channel.send(f'{message.author.mention}님은 테스터로 지정되어 있지 않습니다.', delete_after=10)

        await message.delete(delay=10)  # 보낸 메시지를 10초 후에 삭제
    elif message.content == '!dash':
        if str(message.author.id) in SPECIFIC_USER_IDS:
            try:
                embed = discord.Embed(title="개발자 웹패널", description=f"[웹패널](http://wssdashboard.kro.kr/#)", color=discord.Color.green())
                await message.author.send(embed=embed)
                await message.channel.send(f'{message.author.mention}님, DM을 확인해주세요!', delete_after=10)
            except discord.Forbidden:
                await message.channel.send(f'{message.author.mention}님, DM을 보낼 수 없습니다. DM이 열려 있는지 확인해주세요.', delete_after=10)
        else:
            await message.channel.send(f'{message.author.mention}님은 개발자로 지정되어 있지 않습니다.', delete_after=10)

        await message.delete(delay=10)  # 보낸 메시지를 10초 후에 삭제
    
    elif message.content == '민정아 에스파':
        embed = discord.Embed(title='에스파 소개', description='에스파(AESPA)는 대한민국의 걸그룹으로, SM 엔터테인먼트 소속이에요!', color=0xbca5e6)
        embed.add_field(name='멤버', value='윈터, 카리나, 닝닝, 지젤', inline=True)
        embed.add_field(name='리더', value='카리나', inline=True)
        embed.add_field(name='데뷔일', value='2020년 11월 17일', inline=True)
        embed.add_field(name='데뷔곡', value='디지털 싱글 앨범 Black Mamba로 데뷔하였어요!', inline=True)
        embed.add_field(name='소속사', value='SM 엔터테인먼트', inline=True)
        embed.add_field(name='공식 색', value='Aurora (오로라)', inline=True)
        embed.add_field(name='기타 설명', value='에스파는 SM 엔터테인먼트의 가상 세계 "æ"에서 활동하는 그룹이에요!', inline=True)
        await message.channel.send(embed=embed)
    
    elif message.content == '민정아 핑':
        latency = round(client.latency * 1000)  # 지연 시간을 밀리초로 변환하여 계산
        embed = discord.Embed(title="핑", description=f"핑: {latency}ms", color=0x0082ff)
        await message.channel.send(embed=embed)
    elif message.content == '민정아 샤드':
        shard_id = message.guild.shard_id
        total_shards = client.shard_count

        embed = discord.Embed(title="샤드 정보", color=0x0082ff)
        embed.add_field(name="샤드 ID", value=f"{shard_id}", inline=True)
        embed.add_field(name="총 샤드 수", value=f"{total_shards}", inline=True)

        # 봇 객체 초기화 상태 확인
        if client.user is not None:
            # 봇의 아바타 URL이 없을 경우 기본 값으로 설정
            icon_url = client.user.avatar.url if client.user.avatar else discord.Embed.Empty
            embed.set_footer(text=f"{client.user.name}", icon_url=icon_url)
        else:
            embed.set_footer(text="Winterbot", icon_url="https://cdn.discordapp.com/attachments/1101166187146137630/1251163667324735618/GQCBuFQbEAYwjCE.png?ex=6670e037&is=666f8eb7&hm=2711df464b5825bd7a60525c190067fa5575fd10ca62d4523bc349104bf42874&")
        await message.channel.send(embed=embed)
    
    elif message.content == '민정아 부팅시간':
        interaction: discord.Interaction
        now = datetime.datetime.now()
        delta = now - boot_time
        boot_timestamp = int(time.mktime(boot_time.timetuple()))

        # 시간 경과 계산
        years, remainder = divmod(delta.days, 365)
        months, remainder = divmod(remainder, 30)
        days = remainder
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # 경과 시간 형식화
        if years > 0:
            elapsed_time = f"{years}년"
        elif months > 0:
            elapsed_time = f"{months}달"
        elif days > 0:
            elapsed_time = f"{days}일"
        elif hours > 0:
            elapsed_time = f"{hours}시간"
        elif minutes > 0:
            elapsed_time = f"{minutes}분"
        else:
            elapsed_time = f"{seconds}초"

        response = (
            f'봇이 부팅된 시간: <t:{boot_timestamp}>\n'
            f'부팅 후 흐른 시간: `{elapsed_time}`'
        )
        await message.channel.send(response)
    elif message.content == "민정아 서버정보":
        guild = message.guild
        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count
        
        if boost_level == 0:
            boost_tier = "부스트 없음"
        elif boost_level == 1:
            boost_tier = "레벨 1"
        elif boost_level == 2:
            boost_tier = "레벨 2"
        elif boost_level == 3:
            boost_tier = "레벨 3"
        else:
            boost_tier = "알 수 없음"
        
        server_icon_url = guild.icon.url if guild.icon else discord.Embed.Empty
        
        embed = discord.Embed(title=f'{guild.name} 서버 정보', color=discord.Color.blue())
        embed.set_thumbnail(url=server_icon_url)
        embed.add_field(name='서버 이름', value=guild.name, inline=True)
        embed.add_field(name='멤버 수', value=guild.member_count, inline=True)
        embed.add_field(name='부스트 레벨', value=boost_tier, inline=True)
        embed.add_field(name='부스트 횟수', value=boost_count, inline=True)
        embed.add_field(name='역할', value=len(guild.roles), inline=True)
        embed.add_field(name='텍스트 채널', value=len(guild.text_channels), inline=True)
        embed.add_field(name='음성 채널', value=len(guild.voice_channels), inline=True)
        embed.add_field(name='서버 ID', value=guild.id, inline=True)
        
        await message.channel.send(embed=embed)

    elif message.content == '민정아 봇정보':
        # 봇의 기본 정보
        bot_name = client.user.name
        bot_id = client.user.id
        server_count = len(client.guilds)
        boot_time_formatted = boot_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 코드 길이 측정
        code_file_path = os.path.abspath(__file__)
        with open(code_file_path, 'r', encoding='utf-8') as file:
            code_length = len(file.readlines())
        
        # 개발자 멘션
        developer_mention = f'<@{DEVELOPER_ID}>'

        # 봇 정보 Embed 생성
        bot_info_embed = discord.Embed(title='봇 정보', color=discord.Color.blue())
        bot_info_embed.set_thumbnail(url=client.user.avatar.url if client.user.avatar else discord.Embed.Empty)
        bot_info_embed.add_field(name='봇 이름', value=bot_name, inline=T)
        bot_info_embed.add_field(name='봇 ID', value=bot_id, inline=True)
        bot_info_embed.add_field(name='접속된 서버 수', value=server_count, inline=True)
        bot_info_embed.add_field(name='부팅 시간', value=boot_time_formatted, inline=True)
        bot_info_embed.add_field(name='코드 길이', value=f'{code_length} lines', inline=True)
        bot_info_embed.add_field(name='봇 버전', value=BOT_VERSION, inline=True)
        bot_info_embed.add_field(name='개발자', value=developer_mention, inline=True)
        await message.channel.send(embed=bot_info_embed)

client.run('MTIzNTA4OTcwODk5MjY5NjM5MQ.G0b3fB.VLtFNtqsu6Jif32wH2A4NArAcoH-bxtPsL_IGg')
