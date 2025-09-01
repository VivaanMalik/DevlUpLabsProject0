import random
import requests
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image

load_dotenv()

sender = os.getenv("EMAIL_USER")
receiver = os.getenv("TEMP_RECIEVER")
password = os.getenv("EMAIL_PASS")
unsplashAccessKey = os.getenv("UNSPLASH_ACCESS_KEY")
imageURL = os.getenv("https://api.unsplash.com/photos/random?query=sleep&orientation=landscape")

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
        print("Random sleep landscape image URL:", image_url)
        break
    if response.status_code != 200:
        exit
    print("Error:", response.status_code, response.text)

# Save Image
response = requests.get(image_url)
img = None
for _i in range(retryCount):
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.show()
        break
    if response.status_code != 200:
        exit
    print("Error:", response.status_code, response.text)

# Edit Image

msg = MIMEText("Hello! This is a test email.\n\n"+quote)
msg["Subject"] = "Test"
msg["From"] = sender
msg["To"] = receiver

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    # server.send_message(msg)