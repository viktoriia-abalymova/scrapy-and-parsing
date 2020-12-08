import requests
username = input("Введите имя пользоватаеля:")
request = requests.get('https://api.github.com/users/'+username+'/repos')
data = request.json()
print(data)

import json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
