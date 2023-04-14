import json, requests, os

with open('downloadUserData.json', 'r') as f:
    downloadUserData = json.load(f)

posts = downloadUserData['posts']

for post in posts:
    if "screenshot" not in post and "painting" not in post:
        continue

    if post['screenshot'] != '':
        r = requests.get("https://pretendo-cdn.b-cdn.net/" + post['screenshot'])
        with open(f"images/{post['id']}.png", 'wb') as f:
            f.write(r.content)
    if post['painting'] != '':
        r = requests.get(f"https://pretendo-cdn.b-cdn.net/paintings/{post['pid']}/{post['id']}.png")
        with open(f"images/paintings/{post['id']}.png", 'wb') as f:
            f.write(r.content)

    mii_face = post['mii_face_url'].replace(f"https://mii.olv.pretendo.cc/mii/{post['pid']}/", '').replace(f"http://mii.olv.pretendo.cc/mii/{post['pid']}/", '')

    if not os.path.exists(f"images/mii_face/{mii_face}"):
        r = requests.get(post['mii_face_url'])
        with open(f"images/mii_face/{mii_face}", 'wb') as f:
            f.write(r.content)

    post['mii_face_url'] = mii_face

r = requests.get(f"https://juxt-web-cdn.b-cdn.net/images/banner.png")
with open(f"images/banner.png", 'wb') as f:
    f.write(r.content)

with open('downloadUserData.json', 'w') as f:
    json.dump(downloadUserData, f, indent=4)

'''

{% if post.body != '' %}
    <h4>{{ post.body }}</h4>
{% endif %}
{% if post.screenshot != '' %}
    <img id="{{ post.id }}" class="screenshot" src="https://pretendo-cdn.b-cdn.net/{{ post.screenshot }}">
{% endif %}
{% if post.painting != '' %}
    <img id="{{ post.id }}" class="painting" src="https://pretendo-cdn.b-cdn.net/paintings/{{ post.pid }}/{{ post.id }}.png">
{% endif %}
{% if post.url %}
    <iframe width="760" height="427.5" src="{{ post.url|replace('watch?v=', 'embed/') }}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
{% endif %}

'''