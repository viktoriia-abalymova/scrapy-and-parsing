import requests
import json
from pprint import pprint
request = requests.get('https://api.vk.com/method/groups.get?v=5.52&access_token=a8aa9605fc4aafa100ee492c0827b4d0bf7535adafde29d7731db2d4af4cba7671482245617edd030e271&expires_in=86400&user_id=133991942')
j_data = request.json()
pprint(j_data)

import json
with open('j_data.json', 'w') as outfile:
    json.dump(j_data, outfile)
