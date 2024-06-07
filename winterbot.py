from asyncio import tasks
import discord
from discord.ext import commands, tasks
import random
import datetime
import asyncio

intents = discord.Intents.all()
client = discord.Client(intents=intents)

start_time = datetime.datetime.now()

# 에스파의 곡 목록
aespa_songs = [
    "Black Mamba",
    "Supernova",
    "Long chat",
    "목소리 (Melody)",
    "Live My Life",
    "Prologue",
    "BAHAMA",
    "Licorice",
    "Mine",
    "Set The Tone",
    "자각몽",
    "I'll Make You Cry",
    "Lucid Dream",
    "ICONIC",
    "Jingle Bell Rock",
    "Salty & Sweet",
    "Thirsty",
    "ICU (쉬어가도 돼)",
    "We GO",
    "With you",
    "ZOOM ZOOM",
    "Get Coin",
    "시대유감 (時代遺憾) (2024 aespa Remake Ver.)",
    "Trick or Trick",
    "Hot Air Balloon",
    "Don't Blink",
    "YOLO",
    "You",
    "I'm Unhappy",
]

# 초대 링크를 여기에 입력합니다.
INVITE_LINK = 'https://discord.gg/UfHSqhcj2j'

# 특정 유저의 ID를 여기에 입력합니다.
SPECIFIC_USER_IDS = ['837570564536270848', '1234356435']

@client.event # 봇 로그인
async def on_ready():
    print(f"봇에 로그인을 성공했습니다!")
    print(f"봇 이름: {client.user.name}")
    print(f"봇 아이디: {client.user.id}")
    update_status.start()  # 상태 업데이트 작업 시작
    
status_index = 0  # 상태 메시지를 번갈아 표시하기 위한 인덱스

@tasks.loop(seconds=20)  # 10초마다 상태 메시지를 변경
async def update_status():
    global status_index
    server_count = len(client.guilds)
    
    status_messages = [
        discord.Game('접두사: 민정아'),
        discord.Game(f'{server_count}개의 서버에서 일')
    ]
    
    await client.change_presence(activity=status_messages[status_index])
    status_index = (status_index + 1) % len(status_messages)  # 인덱스를 순환
@client.event
async def on_message(message):
    if message.author == client.user:  # 봇이 자신의 메시지에는 반응하지 않음
        return
    
    if message.content == '민정아': # 봇 명령어 도움말
        embed = discord.Embed(title="윈터봇에는 다양한 기능이 있어요!", description="윈터봇에 대한 여러 가지 명령어를 알려드릴게요!", color=0x00b9ff)
        embed.add_field(name="민정아 소개해", value="윈터에 대한 소개를 해요!", inline=False)
        embed.add_field(name="민정아 개발자", value="저를 만드신 개발자의 정보를 알려드려요!", inline=False)
        embed.add_field(name="민정아 최신곡", value="에스파의 최신곡 뮤비 링크를 보내요!", inline=False)
        embed.add_field(name="민정아 이전곡", value="최신곡의 바로 이전 곡의 뮤비 링크를 보내요!", inline=False)
        embed.add_field(name="민정아 데뷔곡", value="에스파의 데뷔 곡 뮤비 링크를 보내요!", inline=False)
        embed.add_field(name="민정아 데뷔일", value="에스파의 데뷔일을 알려드려요!", inline=False)
        embed.add_field(name="민정아 사진", value="사진을 보내드려요!", inline=False)
        embed.add_field(name="민정아 토레타", value="윈터가 출연한 토레타의 CF의 링크를 보내드려요!", inline=False)
        embed.add_field(name="민정아 추천해줘", value="에스파의 노래 중 하나의 곡을 추천해드려요!", inline=False)
        embed.add_field(name="민정아 아마겟돈", value="아마겟돈 퍼포먼스 영상 링크를 보내드려요!", inline=False)
        embed.add_field(name="민정아 부팅시간", value="윈터봇의 부팅시간을 표시해요!")
        await message.channel.send(embed=embed)
    elif message.content == '민정아 소개해': # 에스파 윈터 소개
        embed = discord.Embed(title="에스파 윈터 소개", description="윈터의 대한 소개에요!", color=0xff0000)
        embed.add_field(name="활동명", value="윈터 (Winter)", inline=False)
        embed.add_field(name="본명", value="김민정 (金旼炡, Kim Min-jeong)", inline=False)
        embed.add_field(name="소속 그룹", value="에스파 (aespa)", inline=False)
        embed.add_field(name="출생", value="2001년 1월 1일 (23세)", inline=False)
        embed.add_field(name="본관", value="김해 김씨")
        embed.add_field(name="신체", value="164cm, A형", inline=False)
        embed.add_field(name="소속사", value="SM 엔터테인먼트", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == '민정아 개발자': # 개발자
        user_id = '837570564536270848'  # 여기에 유저의 ID를 넣어주세요
        user_mention = f'<@{user_id}>'
        embed = discord.Embed(title="윈터봇 개발자", description=f"저는 {user_mention}님이 개발하였어요!", color=0xfdfdfd)
        embed.add_field(name="문의 및 제안", value="[ 서포트 서버 ](https://discord.gg/Rcde2azr3X)", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == '민정아 최신곡':
        embed = discord.Embed(title="에스파 최신곡", description="에스파의 최신 곡 뮤비의 링크에요! (Performance Ver)", color=0xff0700)
        embed.add_field(name="뮤비 링크", value="https://www.youtube.com/watch?v=0nPniUvUBfUc", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == '민정아 이전곡':
        embed = discord.Embed(title="에스파 이전곡", description=" 아마겟돈 발매 전 나온 드라마의 뮤비에요! (Performance Ver)", color=0xffffff)
        embed.add_field(name="뮤비 링크", value="https://www.youtube.com/watch?v=3CvJKTChsl4", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == '민정아 데뷔곡':
        embed = discord.Embed(title="데뷔곡", description="에스파의 데뷔 곡을 알려드릴게요!", color=0x030303)
        embed.add_field(name="데뷔 곡 뮤비 링크", value="https://www.youtube.com/watch?v=ZeerrnuLi5E", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == '민정아 데뷔일':
        embed = discord.Embed(title="데뷔일", description="에스파의 데뷔일을 알려드려요!", color=0x00bffd)
        embed.add_field(name="데뷔일", value="2020년 11월 17일에 디지털 싱글 앨범 Black Mamba로 데뷔했어요!", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == '민정아 아마겟돈':
        embed = discord.Embed(title="에스파 아마겟돈", description="에스파의 아마겟돈 퍼포먼스 영상이에요!!", color=0xfd0000)
        embed.add_field(name="뮤비 링크", value="https://www.youtube.com/watch?v=0nPniUvUBfU", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == '민정아 컴백일':
        embed = discord.Embed(title="에스파 컴백일", description="에스파의 컴백일을 알려드릴게요!", color=0xfd0000)
        embed.add_field(name="컴백일", value="(KST 기준) 에스파는 2024년 5월 27일에 Armageddon으로 컴백했어요!", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == '민정아 사진':
        response = "윈터의 인스타에 올라온 사진이에요!\n"
        response += "사진: https://media.discordapp.net/attachments/1101166187146137630/1245753530342707312/imwinter_2024-05-30T235346-05.jpg?ex=665e8322&is=665d31a2&hm=37b21dd79df7c70dacb77b4556b373ad3c0ed289b8a5b251adf7ef67ec2a7780&=&format=webp&width=501&height=627"
        await message.channel.send(response)
    elif message.content == '민정아 토레타':
        response = "토레타 CF 링크에요!\n"
        response += "CF 링크: https://www.youtube.com/watch?v=jHzOQQhA2S8"
        await message.channel.send(response)
    elif message.content.startswith('민정아 추천해줘'):
        recommended_song = random.choice(aespa_songs)
        embed = discord.Embed(title="추천하는 곡", description=f"에스파의 노래 중에서 하나를 추천해 드릴게요!", color=0x00ff00)
        embed.add_field(name="오늘은 이 노래 어떠세요?", value=recommended_song, inline=False)
        await message.channel.send(embed=embed)
    elif message.content.startswith('민정아 청소해'):
        if message.author.guild_permissions.manage_messages:  # 메시지 관리 권한을 가진 사용자만 실행 가능
            try:
                amount = int(message.content.split()[2])  # 삭제할 메시지 수
                await message.channel.purge(limit=amount + 1)  # 메시지 삭제 (명령어 메시지 포함)
                embed = discord.Embed(description=f'{amount}개의 메시지가 삭제되었습니다. 이 메세지는 5초 뒤 삭제돼요!', color=0x00ff00)
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

client.run('MTIzNTA4OTcwODk5MjY5NjM5MQ.GFk9br.80qaF1K1C_bwI3qojN1RkcXnN8CX5kkaRu3Htg')
