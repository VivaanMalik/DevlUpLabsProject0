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
from bs4 import BeautifulSoup
from datetime import datetime

load_dotenv()

sender = os.getenv("EMAIL_USER")
receiver = os.getenv("TEMP_RECIEVER")
password = os.getenv("EMAIL_PASS")
unsplashAccessKey = os.getenv("UNSPLASH_ACCESS_KEY")
imurlthing = os.getenv("IMAGE_URL")

url = "https://api.unsplash.com/photos/random"
retryCount = 3

def scrapeReddit(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    for _i in range(retryCount):
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            break
        if res.status_code != 200 and _i == retryCount:
            print("Error:", res.status_code, res.text)
            return None
    
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.find_all("div", {"class": "thing"}, limit=3)
    
    data = []
    for post in posts:
        title_tag = post.find("a", class_="title")
        title = title_tag.get_text(strip=True) if title_tag else "No title"

        post_url = title_tag['href'] if title_tag else None
        if post_url and post_url.startswith("/r/"):
            post_url = "https://old.reddit.com" + post_url

        # Visit the post URL to get full text
        description = "No description found"
        if post_url:
            res_post = requests.get(post_url, headers=headers)
            if res_post.status_code == 200:
                soup_post = BeautifulSoup(res_post.text, "html.parser")
                usertext_divs = soup_post.find_all("div", class_="usertext-body")
                if usertext_divs:
                    # print(len(usertext_divs))
                    usertext_div = usertext_divs[1]
                    md_div = usertext_div.find("div", class_="md")
                    if md_div:
                        paragraphs = md_div.find_all("p")
                        description = paragraphs[0].get_text(strip=True)
                        if len(paragraphs)>1:
                            description+="..."

        post_url = post_url.replace("https://old", "https://www")

        data.append([title, description, post_url])
    return data

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
        image_url = data["urls"]["regular"]  # raw, full, regular, small, thumb
        print("Random sleep landscape image URL:", image_url)
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
button_style = (
    "display:inline-block;"
    "padding:10px 20px;"
    "background-color:#FF4500;"
    "color:white;"
    "text-decoration:none;"
    "border-radius:5px;"
    "font-weight:bold;"
)

SubredditData = []
Subreddits = ["https://old.reddit.com/r/AmItheAsshole/top/?t=day", "https://old.reddit.com/r/pettyrevenge/top/?t=day", "https://old.reddit.com/r/relationships/top/?t=day"]
SubredditNames = ["r/AmItheAsshole", "r/pettyrevenge", "r/relationships"]
for Sr in Subreddits:
    SubredditData.append(scrapeReddit(Sr))

linktext = ""
for i in range(len(SubredditData)):
    linktext+=f"<h2>{SubredditNames[i]}</h2>\n"
    for j in SubredditData[i]:
        linktext += f""" 
                    <h3>{j[0]}</h3>
                    <p>{j[1]}</p>
                    <a href="{j[2]}" style="{button_style}">Read More</a>
                    <br>
                    """
    linktext+="\n<hr>\n"
print("Got links")

# Send mail
part1 = MIMEText("Hello! This is a test email.\n\n" + quote)

part2 = MIMEText(f"""
<html>
    <body>
        <h1>Its time to rest!</h1>
        <p>Kindly wait for image to load...
                 orem ipsum dolor sit amet, consectetur adipiscing elit. Integer consectetur magna in sollicitudin hendrerit. Curabitur pretium enim eget felis condimentum pulvinar. Donec luctus convallis est in vulputate. Proin pharetra aliquet velit vitae blandit. Mauris suscipit, libero a accumsan laoreet, nisl felis cursus ligula, dignissim aliquam lectus diam eget nibh. Sed porta enim ut massa tristique, vel congue nisi ullamcorper. Suspendisse vel urna id odio ultricies mattis. Cras sollicitudin elit sit amet purus lobortis, at vestibulum est fermentum. Ut congue eros sit amet ornare suscipit. Sed pulvinar molestie tellus, sed mollis dui ultrices at. Donec pharetra leo orci, feugiat mattis quam placerat nec. Fusce vehicula orci at tellus lobortis semper. Etiam eu egestas metus. Integer porta, diam at ullamcorper faucibus, tortor diam vestibulum velit, et fringilla justo magna a diam.

Phasellus et lectus varius, fermentum sem sed, scelerisque magna. Integer dignissim, dui eget interdum sollicitudin, tortor metus tincidunt erat, id aliquam est quam id sapien. Vivamus ut lacus pulvinar, lacinia nisl ut, faucibus augue. Phasellus nec diam vitae ante ultricies imperdiet. Aliquam mattis, libero ut vulputate convallis, arcu ante malesuada metus, at iaculis lacus ex non metus. Vestibulum vestibulum malesuada efficitur. Suspendisse tristique leo enim.

Vestibulum interdum odio elit, vel ullamcorper massa faucibus et. Praesent commodo elementum lacus in tristique. Donec sit amet vulputate enim. In ut tincidunt enim. Sed eu mauris sit amet justo tempor eleifend at nec nunc. Mauris ornare pretium nisl, ac dapibus ipsum efficitur et. Quisque posuere sagittis egestas. Ut porttitor, leo sed feugiat vehicula, erat orci pulvinar nulla, et iaculis sapien urna ut tellus. Donec placerat fermentum arcu vel feugiat. Maecenas at dapibus nulla. Donec at enim suscipit, dignissim nibh a, suscipit mi. Maecenas rutrum porta mauris. Donec molestie feugiat luctus.

Maecenas blandit nec odio nec congue. Quisque ut blandit diam. Suspendisse eu nibh quis urna ullamcorper malesuada. Mauris dapibus dolor in molestie facilisis. Sed pretium eros at feugiat aliquet. Duis id nulla et lorem ultricies sodales. Proin egestas justo eros, et vehicula nunc suscipit sed. Vestibulum euismod metus in turpis accumsan pharetra. Aenean tempor auctor ultrices. Quisque tincidunt sapien sit amet elit consectetur molestie. Sed in convallis mauris. Nam lobortis, mauris vel vestibulum tincidunt, justo orci dignissim ligula, id auctor neque augue quis eros. Aliquam nec mi velit. In blandit elementum tortor, sollicitudin egestas orci rhoncus ut. Sed urna odio, iaculis vel ultrices non, maximus nec arcu.

Mauris fringilla massa in felis maximus, eu finibus eros cursus. In vehicula nunc eget scelerisque vehicula. Morbi vitae ex vitae velit tristique dapibus vitae ac quam. Suspendisse vitae dolor condimentum, faucibus odio nec, tincidunt tortor. Integer vestibulum odio sollicitudin neque rutrum, non suscipit lectus placerat. Pellentesque rutrum, risus vitae euismod porta, libero purus laoreet orci, eget tempus leo velit vel metus. Praesent mattis dapibus erat congue tincidunt. Sed id nulla vulputate, vestibulum arcu vel, luctus eros. Curabitur gravida euismod felis, vitae viverra nulla ullamcorper vitae. In ullamcorper ipsum quis est convallis, at malesuada magna consectetur. Nam mattis leo sed mauris cursus hendrerit. Vivamus vitae erat ac elit interdum vestibulum. Phasellus odio turpis, tristique at arcu eget, dictum mollis augue.

Sed a porttitor odio, et scelerisque dolor. Nunc vitae lobortis massa, a viverra metus. Nam id sodales elit. Proin lacinia vestibulum vulputate. Mauris nec mollis justo. Integer ornare lorem nec elementum euismod. Vivamus vel gravida lacus, in rutrum orci. Integer mauris dui, accumsan non odio sit amet, dapibus pellentesque diam. Donec ornare elit metus, quis dignissim arcu commodo quis.

Nullam tincidunt vel nunc tristique gravida. Phasellus vestibulum, lectus in lacinia luctus, justo quam pulvinar arcu, ac consectetur justo nunc a justo. Ut eros ipsum, aliquam nec accumsan eu, tempor ac ex. Curabitur vel ipsum eget tortor aliquet bibendum id quis odio. Nullam pulvinar purus eget orci elementum dictum. Etiam sit amet suscipit libero, id lobortis nulla. Donec congue porttitor enim sit amet vestibulum. Ut finibus porttitor massa, a viverra metus hendrerit sed. Donec facilisis erat nisi, a ullamcorper erat vulputate eu.

Ut fermentum tellus mauris, at bibendum augue lacinia non. Mauris purus eros, dictum sit amet maximus eu, egestas et purus. Donec ut fermentum velit. Donec dignissim, mi et lacinia fringilla, magna velit pellentesque felis, et pulvinar tortor ipsum at nibh. Donec dui risus, pulvinar id eleifend blandit, hendrerit non ipsum. Donec ornare, arcu in fringilla auctor, mauris nisl blandit erat, vitae ultricies nulla purus a urna. Vestibulum sed viverra lectus. Fusce interdum nulla a dui venenatis suscipit et a arcu.

Curabitur sed pellentesque tortor. Sed neque elit, viverra ut euismod et, porta nec dui. Duis imperdiet nunc at placerat consequat. Suspendisse quis elit vel eros efficitur suscipit efficitur vitae augue. Pellentesque sodales porttitor nulla non placerat. Interdum et malesuada fames ac ante ipsum primis in faucibus. Phasellus sed porta mi.

Vestibulum imperdiet nunc vitae mi placerat bibendum. Curabitur eu ornare tortor. Morbi viverra efficitur lacus, ut rutrum ante molestie sed. Nunc porttitor quis nisi id lobortis. Phasellus rhoncus enim in purus gravida, vitae laoreet nisl placerat. Nullam sed vestibulum lorem. Integer viverra nisi ut sem gravida, et iaculis libero maximus. Sed vestibulum eleifend dolor ut pharetra. Pellentesque ac nunc in erat scelerisque auctor in at enim. Donec id dictum enim. Cras ornare velit sed malesuada pellentesque. Aliquam porta elementum arcu at pulvinar. Nam interdum neque fermentum sagittis congue. Duis lobortis feugiat tempor. Nulla eget varius diam. Vivamus viverra nisi eu pretium tincidunt.

Phasellus placerat lorem id leo tincidunt, a viverra dui fermentum. Vivamus pulvinar justo et tortor ornare dictum. Nullam quis mauris justo. Integer finibus ultricies arcu sed egestas. Praesent odio enim, semper et malesuada eget, bibendum vel turpis. Integer ullamcorper felis vitae diam pretium porttitor. Duis laoreet purus at vestibulum imperdiet. Ut placerat enim ut odio venenatis, nec interdum neque dapibus. Etiam vel dapibus magna, ut pharetra nisl.

Phasellus dictum sit amet dolor sit amet vestibulum. Suspendisse molestie, ligula eget eleifend varius, risus arcu feugiat neque, ac aliquet tellus nisi eu dui. In varius ultricies sem. Donec placerat sem eu arcu rutrum blandit. Sed faucibus pellentesque commodo. Mauris lobortis ornare sapien nec pharetra. Suspendisse mattis tortor sed. </p>
        <hr>
            <p><img src="cid:testimage" alt="Get better internet my guy."></p>
        <hr>
        <h1>Top articles across reddit [{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]</h1>
            <hr>
            {linktext}
        <br>
    </body>
</html>
""", "html")

part3 = MIMEImage(buffer.getvalue(), _subtype="png")
part3.add_header("Content-ID", "<testimage>")

msg = MIMEMultipart('related')
msg["Subject"] = "⚠️⚠️⚠️LOOK AT THIS VERY LEGIT LOOKING MAIL⚠️⚠️⚠️"
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