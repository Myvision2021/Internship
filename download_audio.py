import urllib.request
import re
import sys

url = 'https://commons.wikimedia.org/wiki/File:Vande_Mataram_on_Mohan_Veena.ogg'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'href="(https://upload.wikimedia.org/[^"]+\.ogg)"', html)
    if match:
        direct_url = match.group(1)
        print("Downloading from:", direct_url)
        req2 = urllib.request.Request(direct_url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req2).read()
        with open('vande_mataram.ogg', 'wb') as f:
            f.write(data)
        print("Success")
    else:
        print("Link not found in HTML.")
except Exception as e:
    print("Error:", e)
