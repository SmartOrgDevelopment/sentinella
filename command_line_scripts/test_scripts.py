import requests

token1 = ""

uri = "https://api.travis-ci.com"
github_token = {"github_token": token1}

# For github authentication
HEADERS1 = {
    'User-Agent': 'MyClient/1.0.0',
    'Accept': 'application/vnd.travis-ci.2+json',
    'Host': 'api.travis-ci.com',
    'Content-Type': 'application/json'
}

r1 = requests.post(uri + "/auth/github",
                   headers=HEADERS1,
                   params=github_token)
r1.json()

# For travis authentication
HEADER2 = {
    'User-Agent': 'MyClient/1.0.0',
    'Accept': 'application/vnd.travis-ci.2+json',
    'Host': 'api.travis-ci.com',
    'Authorization': 'token %s' % r1.json()["access_token"]
}

r2 = requests.get(uri + "/users", headers=HEADER2)
r2.json()

r3 = requests.get(uri + "/repos/smartorg", headers=HEADER2)
r3.json()

r4 = requests.get(uri + "/repos/smartorg/Chomolongma", headers=HEADER2)
r4.json()
