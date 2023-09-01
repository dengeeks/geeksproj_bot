import requests

url = "https://www.mashina.kg/search/all/"

payload = {}
headers = {
  'Cookie': 'PHPSESSID=6bd72hgcjmvm6gdjaojff7ha51; device_view=full; hl=ru',
}

response = requests.request("GET", url, headers=headers, data=payload)

