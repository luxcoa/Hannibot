import discord
from discord.ext import commands, tasks
from discord.ui import Select, View
import random
import datetime
import re

intents = discord.Intents.all()
client = discord.Client(intents=intents)

start_time = datetime.datetime.now()

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
SPECIFIC_USER_IDS = ['837570564536270848', '1221449577828188265']

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
            embed.add_field(name="민정아 소개해", value="윈터에 대한 소개를 해요!", inline=False)
            embed.add_field(name="민정아 개발자", value="저를 만드신 개발자의 정보를 알려드려요!", inline=False)
            embed.add_field(name="민정아 데뷔일", value="에스파의 데뷔일을 알려드려요!", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif self.values[0] == "뮤비":
            embed = discord.Embed(title="뮤비 명령어", description="에스파의 다양한 뮤비 명령어들입니다.", color=0x0082ff)
            embed.add_field(name="민정아 최신곡", value="에스파의 최신곡 뮤비 링크를 보내요!", inline=False)
            embed.add_field(name="민정아 이전곡", value="최신곡의 바로 이전 곡의 뮤비 링크를 보내요!", inline=False)
            embed.add_field(name="민정아 데뷔곡", value="에스파의 데뷔 곡 뮤비 링크를 보내요!", inline=False)
            embed.add_field(name="민정아 아마겟돈", value="아마겟돈 퍼포먼스 영상 링크를 보내요!", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "유틸리티":
            embed = discord.Embed(title="유틸리티 명령어", description="윈터봇의 다양한 유틸 명령어들입니다.", color=0x0082ff)
            embed.add_field(name="민정아 핑", value="윈터봇의 핑을 전송해요!")
            embed.add_field(name="민정아 사진", value="사진을 보내드려요!", inline=False)
            embed.add_field(name="민정아 추천해줘", value="에스파의 노래 중 하나의 곡을 추천해드려요!", inline=False)
            embed.add_field(name="민정아 컴백일", value="에스파의 컴백일을 알려드려요!", inline=False)
            embed.add_field(name="민정아 청소해 (청소할 메세지)", value="지정한 갯수의 메세지를 청소해요! ( 봇 멈출수도 있음 ) ", inline=False)
            embed.add_field(name="민정아 부팅시간", value="윈터봇의 부팅시간을 표시해요!", inline=False)
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

    elif message.content == '민정아 소개해':
        embed = discord.Embed(title="에스파 윈터 소개", description="윈터의 대한 소개에요!", color=0x0082ff)
        embed.add_field(name="활동명", value="윈터 (Winter)", inline=False)
        embed.add_field(name="본명", value="김민정 (金旼炡, Kim Min-jeong)", inline=False)
        embed.add_field(name="소속 그룹", value="에스파 (aespa)", inline=False)
        embed.add_field(name="출생", value="2001년 1월 1일 (23세)", inline=False)
        embed.add_field(name="본관", value="김해 김씨")
        embed.add_field(name="신체", value="164cm, A형", inline=False)
        embed.add_field(name="소속사", value="SM 엔터테인먼트", inline=False)
        await message.channel.send(embed=embed)
        
    elif message.content == '민정아 개발자':
        user_id = '837570564536270848'
        user_mention = f'<@{user_id}>'
        embed = discord.Embed(title="윈터봇 개발자", description=f"저는 {user_mention}님이 개발하였어요!", color=0x0082ff)
        embed.add_field(name="문의 및 제안", value="[ 서포트 서버 ](https://discord.gg/Rcde2azr3X)", inline=False)
        await message.channel.send(embed=embed)
        
    elif message.content == '민정아 최신곡':
        embed = discord.Embed(title="에스파 최신곡", description="", color=0x030303)
        embed.add_field(name="", value="[최신곡](https://www.youtube.com/watch?v=0nPniUvUBfUc)", inline=False)
        # 썸네일 가져오기
        video_id = re.search(r'v=([^&]+)', embed.fields[0].value).group(1)
        Image_url = f"https://i.ytimg.com/vi/{'0nPniUvUBfUc'}/mqdefault.jpg"
        embed.set_image(url=Image_url)
        await message.channel.send(embed=embed)
        await message.channel.send(embed=embed)

    elif message.content == '민정아 이전곡':
        embed = discord.Embed(title="드라마", description=" 아마겟돈 발매 전 나온 드라마의 뮤비에요!", color=0xff0000)
        embed.add_field(name="뮤비 링크", value="[이전곡](https://www.youtube.com/watch?v=3CvJKTChsl4)", inline=False)
        
        # 썸네일 가져오기
        video_id = re.search(r'v=([^&]+)', embed.fields[0].value).group(1)
        Image_url = f"https://i.ytimg.com/vi/{'3CvJKTChsl4'}/mqdefault.jpg"
        embed.set_image(url=Image_url)
        await message.channel.send(embed=embed)

        
    elif message.content == '민정아 데뷔곡':
        embed = discord.Embed(title="데뷔곡", description="에스파의 데뷔 곡을 알려드릴게요!", color=0x030303)
        embed.add_field(name="데뷔 곡 뮤비 링크", value="[에스파 데뷔곡](https://www.youtube.com/watch?v=ZeerrnuLi5E)", inline=False)
        # 썸네일 가져오기
        video_id = re.search(r'v=([^&]+)', embed.fields[0].value).group(1)
        Image_url = f"https://i.ytimg.com/vi/{'ZeerrnuLi5E'}/mqdefault.jpg"
        embed.set_image(url=Image_url)
        await message.channel.send(embed=embed)

    elif message.content == '민정아 데뷔일':
        embed = discord.Embed(title="데뷔일", description="에스파의 데뷔일을 알려드려요!", color=0x00bffd)
        embed.add_field(name="데뷔일", value="2020년 11월 17일에 디지털 싱글 앨범 Black Mamba로 데뷔했어요!", inline=False)
        await message.channel.send(embed=embed)
        
    elif message.content == '민정아 사진':
        embed = discord.Embed(title="윈터 사진", description="윈터의 인스타그램에 최근 올라온 사진입니다.", color=0xff0000)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1101166187146137630/1244136042148139049/IMG_9773.png?ex=6663d57b&is=666283fb&hm=a973c90766edc160907c5d1e065a13e3a7e788c3e349ef44af2ebb00b42bf650&")  # 실제 이미지 URL을 넣으세요
        await message.channel.send(embed=embed)

    elif message.content == '민정아 노래추천':
        song = random.choice(aespa_songs)
        embed = discord.Embed(title="에스파 노래 추천", description=f"오늘은 **{song}** 이 곡 어떠세요?", color=0x0082ff)
        await message.channel.send(embed=embed)

    elif message.content == '민정아 컴백일':
        embed = discord.Embed(title="컴백일", description="에스파의 컴백일을 알려드릴게요!", color=0xffff00)
        embed.add_field(name="컴백일", value="2023년 5월 8일에 컴백했어요!", inline=False)
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
    
    elif message.content == '민정아 에스파':
        embed = discord.Embed(title='에스파 소개', description='에스파(AESPA)는 대한민국의 걸그룹으로, SM 엔터테인먼트 소속이에요!', color=0xbca5e6)
        embed.add_field(name='멤버', value='윈터, 카리나, 닝닝, 지젤', inline=False)
        embed.add_field(name='리더', value='카리나', inline=False)
        embed.add_field(name='데뷔일', value='2020년 11월 17일', inline=False)
        embed.add_field(name='데뷔곡', value='디지털 싱글 앨범 Black Mamba로 데뷔하였어요!', inline=False)
        embed.add_field(name='소속사', value='SM 엔터테인먼트', inline=False)
        embed.add_field(name='공식 색', value='Aurora (오로라)', inline=False)
        embed.add_field(name='기타 설명', value='에스파는 SM 엔터테인먼트의 가상 세계 "æ"에서 활동하는 그룹이에요!', inline=False)
        await message.channel.send(embed=embed)
    
    elif message.content == '민정아 핑':
        latency = round(client.latency * 1000)  # 지연 시간을 밀리초로 변환하여 계산
        embed = discord.Embed(title="핑", description=f"핑: {latency}ms", color=0x0082ff)
        await message.channel.send(embed=embed)

client.run('MTIzNTA4OTcwODk5MjY5NjM5MQ.GFk9br.80qaF1K1C_bwI3qojN1RkcXnN8CX5kkaRu3Htg')
