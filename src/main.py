from email.mime.multipart import MIMEMultipart
import random
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv
import io, base64
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import datetime
import json
import gspread
import sys

load_dotenv()

sender = os.getenv("EMAIL_USER")
# receiver = os.getenv("TEMP_RECIEVER")
password = os.getenv("EMAIL_PASS")
unsplashAccessKey = os.getenv("UNSPLASH_ACCESS_KEY")
imurlthing = os.getenv("IMAGE_URL")
REDDIT_API_SECRET = os.getenv("REDDIT_API_SECRET")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_USER = os.getenv("REDDIT_USER")
REDDIT_PASS = os.getenv("REDDIT_PASS")
SERVICE_ACC_KEY=os.getenv("SERVICE_ACC_KEY")
try:
    creds = json.loads(SERVICE_ACC_KEY)
    gc = gspread.service_account_from_dict(creds)
except:
    path = "./src/cred.json"
    if (os.path.isfile(path)):
        print("gang gang")
    else:
        print("no gang gang")
    gc = gspread.service_account(filename=path)

spreadsheet_id = os.getenv("SPREADSHEET_ID")
sh = gc.open_by_key(spreadsheet_id)
ws = sh.sheet1
records = ws.get_all_records()
print(records)

def get_reddit_token():
    auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_API_SECRET)
    data = {
        "grant_type": "password",
        "username": REDDIT_USER,
        "password": REDDIT_PASS
    }
    headers = {"User-Agent": "reddit-digest-script/0.1"}
    res = requests.post("https://www.reddit.com/api/v1/access_token",
                        auth=auth, data=data, headers=headers)
    res.raise_for_status()
    return res.json()["access_token"]

def fetch_subreddit(subreddit, token, limit=3):
    headers = {"Authorization": f"bearer {token}",
               "User-Agent": "reddit-digest-script/0.1"}
    url = f"https://oauth.reddit.com/{subreddit}/top?t=day&limit={limit}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    posts = []
    for post in res.json()["data"]["children"]:
        title = post["data"]["title"]
        selftext = post["data"].get("selftext", "")
        description = (selftext[:420] + "...") if selftext else "No description"
        post_url = "https://reddit.com" + post["data"]["permalink"]
        posts.append([title, description, post_url])
    return posts

url = "https://api.unsplash.com/photos/random"
retryCount = 3

quotes = [
    "Procrastinate now,\npay later.",
    "Sleep more,\ndo less.",
    "Tomorrow is\nthe productive day.",
    "Delay is\nthe only plan.",
    "Busy is\nthe new lazy.",
    "Work hard?\nNah, relax.",
    "Efficiency\nis overrated.",
    "Dreams work\nwhile you nap.",
    "Goals?\nForget them.",
    "Coffee first,\ndo nothing after.",
    "Time is\nmeant to waste.",
    "Progress?\nMaybe tomorrow.",
    "Laziness\nis underrated.",
    "Do it later,\ndo it never.",
    "Avoid tasks,\nembrace chaos.",
    "Deadlines\nare suggestions.",
    "Work smart?\nWhy bother?",
    "Chill now,\nstress later.",
    "Planning\nis exhausting.",
    "Rest is\nproductive too.",
    "Do nothing,\nfeel alive.",
    "Delay all,\nachieve nothing.",
    "Pause often,\nnever stop.",
    "Avoid work,\navoid worry.",
    "Distraction\nis an art.",
    "Nap hard,\ndream big.",
    "Rest beats\nproductivity.",
    "Time flies,\nso should you.",
    "Minimal effort,\nmaximum leisure.",
    "Today’s work\nis tomorrow’s problem.",
    "Avoid success,\nit’s stressful.",
    "Sit back,\nwatch life.",
    "Stop rushing,\nstart lounging.",
    "Idle minds\nare genius.",
    "Nothing done\nis perfect.",
    "Delay is\nstrategy.",
    "Relaxation\nis a talent.",
    "Avoid effort,\nembrace joy.",
    "Unproductive\nis a lifestyle.",
    "Nothing matters\nexcept naps.",
    "Lazy days\nare sacred.",
    "Do less,\nfeel more.",
    "Rest often,\nachieve never.",
    "Chill first,\nplan later.",
    "Time wasted\nis time earned.",
    "Avoid deadlines,\navoid stress.",
    "Procrastination\nis creativity.",
    "Do nothing,\nbe happy.",
    "Work less,\nlive more.",
    "Pause life,\nenjoy nothing.",
    "Delay daily,\nwin never.",
    "Leisure over\nlabor.",
    "Nothing now,\nnothing later.",
    "Avoid hurry,\navoid worry.",
    "Relax hard,\nstress soft.",
    "Unfinished work\nis art.",
    "Do it tomorrow,\ndo it late.",
    "Skip tasks,\ncollect peace.",
    "Lounge well,\nnap better.",
    "Procrastinate\nlike a pro.",
    "Stop trying,\nstart chilling.",
    "Avoid effort,\nembrace rest.",
    "Time is\na suggestion.",
    "Tomorrow works\nfor today’s work.",
    "Less hustle,\nmore peace.",
    "Avoid pressure,\navoid pleasure.",
    "Slow down,\ngo nowhere.",
    "Nap often,\ndream freely.",
    "Relaxation\nis underrated.",
    "Do it later,\ndo it lightly.",
    "Avoid focus,\nseek fun.",
    "Work is\noptional.",
    "Rest first,\nthink later.",
    "Pause often,\nact never.",
    "Do nothing,\nmaster everything.",
    "Time wasted\nis life gained.",
    "Idle hands\nare calm minds.",
    "Chill mode\nis eternal.",
    "Avoid stress,\nembrace laziness.",
    "Work less,\nnothing more.",
    "Laziness\nis self-care.",
    "Procrastinate\nwith style.",
    "Tomorrow’s work\nis today’s joy.",
    "Delay now,\nsmile later.",
    "Rest is\nan achievement.",
    "Do less,\nfeel good.",
    "Avoid responsibility,\ncollect freedom.",
    "Pause often,\nlive rarely.",
    "Nothing done\nis perfection.",
    "Skip work,\nfind happiness.",
    "Unproductivity\nis bliss.",
    "Chill today,\nignore tomorrow.",
    "Avoid plans,\nfind chaos.",
    "Relax hard,\navoid work.",
    "Time wasted\nis creativity gained.",
    "Do nothing,\nmaster chill.",
    "Postpone tasks,\ncollect peace.",
    "Idle today,\ngain calm.",
    "Avoid action,\nseek comfort.",
    "Less doing,\nmore being.",
    "Delay decisions,\navoid stress.",
    "Work less,\nrest more.",
    "Avoid urgency,\nembrace laziness.",
    "Nothing planned\nis everything gained.",
    "Chill first,\ndo later.",
    "Pause life,\nnap often."
]

#  Get Quote
quote = random.choice(quotes)
print("Got Quote")

# Get Image
headers = {
    "Authorization": f"Client-ID {unsplashAccessKey}"
}
params = {
    "query": "sleep",
    "orientation": "landscape"
}

image_url = None
response = requests.get(url, headers=headers, params=params)
for _i in range(retryCount):
    if response.status_code == 200:
        data = response.json()
        image_url = data["urls"]["raw"]  # raw, full, regular, small, thumb
        image_url = f"{image_url}&w=800&h=600&fit=crop&q=80"
        break
    if response.status_code != 200 and _i == retryCount-1:
        exit
    print("Error:", response.status_code, response.text)
print("Got Image")

# Save Image
img = None
for _i in range(retryCount):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content))
        # img.show()
        break
    if response.status_code != 200:
        exit
    print("Error:", response.status_code, response.text)

# Edit Image
img_array = np.array(img)
avg_color = tuple(np.average(img_array, axis=(0, 1)).astype(int))
img_width, img_height = img.size
midx = img_width / 2
midy = img_height / 2
text_color = (0, 0, 0)
border_color = (255, 255, 255)

if (avg_color[0]+avg_color[1]+avg_color[2]<128*3):
    text_color = (255, 255, 255)
    border_color = (0, 0, 0)

draw = ImageDraw.Draw(img)
font = None
size_f = img.height//10
try:
    font = ImageFont.truetype('times.ttf', size=size_f)
except IOError:
    font = ImageFont.load_default(size=size_f)
draw.text((midx, midy), quote, fill=text_color, font=font, anchor="mm", align="center", stroke_width=size_f//20, stroke_fill=border_color)
buffer = io.BytesIO()
img.save(buffer, format="PNG")
buffer.seek(0)
img_str = base64.b64encode(buffer.read()).decode("utf-8")
print("Edited Image")

# Get links/embeds
highlight_color = "FF4500"
button_style = f"background:#{highlight_color}; color:#FFFFFF; border-radius:5px; padding:8px 16px; text-decoration:none;"

SubredditData = []

SubredditNames = ["r/AmItheAsshole", "r/pettyrevenge", "r/relationships"]
token = get_reddit_token()
print("Got Token")
for Sr in SubredditNames:
    SubredditData.append(fetch_subreddit(Sr, token))

linktext = f"<p style='color:#888;'>Digest generated on {datetime.now().strftime('%d/%m/%Y at %H:%M:%S')}</p>"
for i in range(len(SubredditData)):
    linktext += f"""
    <h2 style="color:#{highlight_color};">{SubredditNames[i]}</h2>
    """
    for j in SubredditData[i]:
        linktext += f"""
        <div style="border:1px solid #D7DADC; border-radius:6px; padding-left:15px; padding-top:0px; padding-bottom:25px; margin:10px 20px 10px 20px;">
            <h3 style="color:#1A1A1B; margin-left:10px; margin-right:10px; margin-top: 10px;">{j[0]}</h3>
            <div style="margin-left:20px;">
                <p style="color:#7C7C7C;">{j[1]}</p>
                <a href="{j[2]}" style="{button_style}">Read More</a>
            </div>
        </div>
        """
    linktext += "<hr style='border:0; height:1px; background:#D7DADC;'>\n"

print("Got links")

# Send mail
part1 = MIMEText("Hello! This is a test email.\n\n" + quote)

part2 = MIMEText(f"""\
<html>
    <body style="margin:0; padding:0; background:#F8F9FA; font-family:Arial, Helvetica, sans-serif; color:#1A1A1B;">
        <div style="max-width:800px; margin:auto; background-color:transparent; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.1);">
                 
            <h1 style='color:#{highlight_color}; background-color:transparent;'>You deserve a break!</h1>
            <p style='color:#7C7C7C; background-color:transparent;'>Kindly wait for image to load...</p>
                 
            <hr style="border:0; height:1px; background-color:transparent;">
                <p><img src="cid:testimage" alt="Get better internet my guy." style="max-width: 100%; height: auto;"></p>
            <hr style="border:0; height:1px; background-color:transparent;">
                 
            <h1 style='color:#{highlight_color}; background-color:transparent;'>Daily Drama Digest</h1>
            <hr style="border:0; height:1px; background-color:transparent;">
            {linktext}
            <br>

            <div style="background:#F1F1F1; padding:15px; text-align:center; font-size:12px; color:#7C7C7C;">
                <p style="margin:0;">You're receiving this because you have subscribed to a service made by Vivaan (what were you thinking?)</p>
                <p style="margin:5px 0 0;">
                <a href="https://forms.gle/QUj4uw71MMHqEgJG9" style="color:#{highlight_color}; text-decoration:none;">Unsubscribe</a>
                </p>
            </div>
        </div>
    </body>
</html>
""", "html")

part3 = MIMEImage(buffer.getvalue(), _subtype="png")
part3.add_header("Content-ID", "<testimage>")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        records = [{"Email Address":sys.argv[1]}]

for i in records:
    # if i["Email Address"] in unsubscribed:
    #     continue

    msg = MIMEMultipart('related')
    msg["Subject"] = "⚠️⚠️⚠️LOOK AT THIS VERY LEGIT LOOKING MAIL⚠️⚠️⚠️"
    msg["From"] = sender
    msg["To"]=i["Email Address"]
    alt = MIMEMultipart('alternative')
    alt.attach(part1)
    alt.attach(part2)

    msg.attach(alt)
    msg.attach(part3)
    print("Prepped mail for "+i["Email Address"])
    for j in i["Email Address"]:
        print(j+" ", end="")
    print()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
    print("Sent mail to "+i["Email Address"])