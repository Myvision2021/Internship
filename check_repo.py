import urllib.request
import json

try:
    req = urllib.request.Request('https://api.github.com/repos/Myvision2021/Internship/contents', headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode())
    
    print("Files in repo:")
    for item in data:
        print(f" - {item['name']} ({item['type']})")
except Exception as e:
    print(f"Error checking contents: {e}")

try:
    req = urllib.request.Request('https://api.github.com/repos/Myvision2021/Internship', headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode())
    print(f"\nRepo details:\nName: {data.get('name')}\nPrivate: {data.get('private')}\nSize: {data.get('size')}\nDefault Branch: {data.get('default_branch')}\nHas Pages: {data.get('has_pages')}")
except Exception as e:
    print(f"Error checking repo details: {e}")
