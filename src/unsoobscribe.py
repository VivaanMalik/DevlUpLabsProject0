import os
from dotenv import load_dotenv
import json
import gspread
import sys

load_dotenv()

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

if len(sys.argv) > 1:
    EmailToDelet = sys.argv[1]
    cell = ws.find(EmailToDelet)
    if cell:
        ws.delete_rows(cell.row)
        print("Deleted " + EmailToDelet)
    else:
        print("ERROROROROROROOR 1")
else:
    print("ERROROROROROROOR 2")