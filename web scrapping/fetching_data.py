import requests


def fetchAndSaveToFile(url, path):
    r = requests.get(url)
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)


url = "https://www.walmart.com/"
fetchAndSaveToFile(url, "data1.html")
