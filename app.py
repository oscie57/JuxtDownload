from flask import Flask, render_template, send_file
import json, os, sys

app = Flask(__name__)

if not os.path.exists('pretendo.json'):
    print("I can't find your pretendo.json file! Starting setup...")

    mii_name = input("What's your Mii name? ")
    access_level = int(input("What's your access level? (0 = User, 1 = Tester, 2 = Mega, 3 = Dev) "))
    username = input("What's your PNID username? ")
    country = input("What's your country? ")
    language = input("What's your language? ")
    birthday = input("What's your birthday? (YYYY-MM-DD) ")

    if language not in ['de', 'en', 'es', 'fr', 'it', 'ja', 'ko', 'nl', 'pt', 'pt_br', 'ru', 'zh']:
        print("Invalid language! Please try again.")
        sys.exit()

    if access_level not in [1, 2, 3]:
        print("Invalid access level! Please try again.")
        sys.exit()

    if len(birthday) != 10:
        print("Invalid birthday! Please try again.")
        sys.exit()

    json_data = {
        "mii_name": mii_name,
        "access_level": access_level,
        "username": username,
        "country": country,
        "language": language,
        "birthday": birthday
    }

    with open('pretendo.json', 'w') as f:
        json.dump(json_data, f, indent=4)

    print("Setup complete!")

if not os.path.exists('downloadUserData.json'):
    print("downloadUserData.json not found! Make sure you've downloaded your data from your Juxtaposition profile page.")
    sys.exit()

if not os.path.exists('lang.json'):

    print("Language files not detected, downloading...")

    with open('pretendo.json', 'r') as f:
        pretendo = json.load(f)

        lang = pretendo['language']

    import requests

    r = requests.get(f'https://raw.githubusercontent.com/PretendoNetwork/juxt-web/ui-redesign/src/translations/{lang}.json')

    with open('lang.json', 'w') as f:
        f.write(r.text)

    print("Language files downloaded!")
    
with open('pretendo.json', 'r') as f:
    pnid = json.load(f)
with open('downloadUserData.json', 'r') as f:
    downloadUserData = json.load(f)
with open('lang.json', 'r') as f:
    lang = json.load(f)

userSettings = downloadUserData['user_settings']
userContent = downloadUserData['user_content']
newPosts = downloadUserData['posts']

@app.route('/')
def index():
    #request_dump(request)

    return render_template('user_page.html', pnid=pnid, lang=lang, userSettings=userSettings, userContent=userContent, newPosts=newPosts)

@app.route('/web.css')
def css():
    return send_file('./static/web.css')

if __name__ == '__main__':
    app.run("127.0.0.1", 80, debug=True)