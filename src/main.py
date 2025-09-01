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

load_dotenv()

sender = os.getenv("EMAIL_USER")
receiver = os.getenv("TEMP_RECIEVER")
password = os.getenv("EMAIL_PASS")
unsplashAccessKey = os.getenv("UNSPLASH_ACCESS_KEY")

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

print("DEBUG unsplashAccessKey:", unsplashAccessKey is not None)
print("DEBUG sender:", sender)

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
        image_url = data["urls"]["regular"]  # raw, full, regular, small, thumb
        print("Random sleep landscape image URL:", image_url)
        break
    if response.status_code != 200:
        exit
    print("Error:", response.status_code, response.text)
print("Got Image")

# Save Image
response = requests.get(image_url)
img = None
for _i in range(retryCount):
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
size_f = 100
try:
    font = ImageFont.truetype('times.ttf', size=size_f)
except IOError:
    font = ImageFont.load_default(size=size_f)
draw.text((midx, midy), quote, fill=text_color, font=font, anchor="mm", align="center", stroke_width=5, stroke_fill=border_color)
buffer = io.BytesIO()
img.save(buffer, format="PNG")
buffer.seek(0)
img_str = base64.b64encode(buffer.read()).decode("utf-8")
print("Edited Image")

# Send mail
part1 = MIMEText("Hello! This is a test email.\n\n" + quote)

part2 = MIMEText(f"""
<html>
  <body>
    <p>
      Hi!<br>
      <img src="cid:testimage">
    </p>
  </body>
</html>
""", "html")

part3 = MIMEImage(buffer.getvalue(), _subtype="png")
part3.add_header("Content-ID", "<testimage>")

msg = MIMEMultipart('related')
msg["Subject"] = "Test"
msg["From"] = sender
msg["To"] = receiver
alt = MIMEMultipart('alternative')
alt.attach(part1)
alt.attach(part2)

msg.attach(alt)
msg.attach(part3)
print("Prepped mail")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.send_message(msg)
print("Sent mail")