import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime

bot = commands.Bot(intents=discord.Intents.all(),command_prefix='--') #Dont Change The Prefix
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="TikTok Accounts"))
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
                            # Channel ID here ↓
    if message.channel.id == 1132459388213395549 and "tiktok.com" in message.content:
        tiktok_username = extract_tiktok_username(message.content)
        if tiktok_username:
            await send_user_info_and_delete(message, tiktok_username)

    await bot.process_commands(message)

def extract_tiktok_username(url):
    try:
        return url.split("@")[1].split("/")[0]
    except IndexError:
        return None

async def send_user_info_and_delete(message, username):
    try:
        server_log = send_request(username)
        data_json = to_json(server_log)

        user_id = get_user_id(data_json)
        name = get_name(data_json)
        verification_status = get_verification_status(data_json)
        privacy_status = get_privacy_status(data_json)
        sec_uid = get_sec_uid(data_json)
        followers_count = get_followers_count(data_json)
        following_count = get_following_count(data_json)
        create_time = get_user_create_time(data_json)
        change_name_time = get_last_change_name(data_json)
        region = get_account_region(data_json)

        embed = discord.Embed(title=f"User Info for @{username}", color=int("9508d8", 16))
        embed.add_field(name="Nickname", value=name, inline=False)
        embed.add_field(name="User ID", value=user_id, inline=False)
        embed.add_field(name="Account Region", value=region, inline=False)
        embed.add_field(name="Verified?", value=verification_status, inline=False)
        embed.add_field(name="Priavte?", value=privacy_status, inline=False)
        embed.add_field(name="Followers", value=followers_count, inline=False)
        embed.add_field(name="Following", value=following_count, inline=False)
        embed.add_field(name="User Created Time", value=f"||{create_time}||", inline=False)
        embed.add_field(name="Last Time Change Nickname", value=f"||{change_name_time}||", inline=False)
        embed.add_field(name="secUid", value=f"||{sec_uid}||", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1132114368528666777/1133248161813626990/Banners_ideas.jpeg")
        embed.set_footer(text="Developed With 🤍By IDA", icon_url="https://cdn.discordapp.com/attachments/999170633546080357/1128721137489170555/cdf34faa832a5efeb9330c17b9c43699.png")


        await message.channel.send(embed=embed, reference=message)

        # Delete the original message
        await message.delete()

    except:
        pass

def send_request(username):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    r = requests.get(f"https://www.tiktok.com/@{username}", headers=headers)
    return r.text


# Other functions remain the same...
def to_json(server_log):
    try:
        soup = BeautifulSoup(server_log, 'html.parser')
        script = soup.find(id='SIGI_STATE').contents
        data = str(script).split('},"UserModule":{"users":{')[1]
        return data
    except IndexError:
        return ""

def get_user_id(data_json):
    try:
        return data_json.split('"id":"')[1].split('",')[0]
    except IndexError:
        return "Unknown"


def get_name(data_json):
    try:
        return data_json.split(',"nickname":"')[1].split('",')[0]
    except IndexError:
        return "Unknown"

def get_verification_status(data_json):
    try:
        check = data_json.split('"verified":')[1].split(',')[0]
        return "Yes" if check == "true" else "No"
    except IndexError:
        return "Unknown"

def get_privacy_status(data_json):
    try:
        check = data_json.split('"privateAccount":')[1].split(',')[0]
        return "Yes" if check == "true" else "No"
    except IndexError:
        return "Unknown"

def get_sec_uid(data_json):
    try:
        return data_json.split(',"secUid":"')[1].split('"')[0]
    except IndexError:
        return "Unknown"

def get_followers_count(data_json):
    try:
        return data_json.split('"followerCount":')[1].split(',')[0]
    except IndexError:
        return "Unknown"

def get_following_count(data_json):
    try:
        return data_json.split('"followingCount":')[1].split(',')[0]
    except IndexError:
        return "Unknown"

def get_user_create_time(data_json):
    try:
        url_id = int(get_user_id(data_json))
        binary = "{0:b}".format(url_id)
        bits = binary[:31]
        timestamp = int(bits, 2)
        dt_object = datetime.fromtimestamp(timestamp)
        return str(dt_object)
    except:
        return "Unknown"

def get_last_change_name(data_json):
    try:
        time = data_json.split('"nickNameModifyTime":')[1].split(',')[0]
        check = datetime.fromtimestamp(int(time))
        return str(check)
    except IndexError:
        return "Unknown"

def get_account_region(data_json):
    try:
        check = data_json.split('"region":"')[1].split('"')[0]
        return check
    except IndexError:
        return "Unknown"

bot.run('') #Add The Bot Token Here