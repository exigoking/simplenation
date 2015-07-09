import requests
url = 'http://dev.djangobook.com/snippets_app/snippets'
r = requests.get(url)
payload = {'code':'asdfasdfa'}
r = requests.post(url, payload)