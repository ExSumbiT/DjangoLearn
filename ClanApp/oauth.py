import requests
from urllib.parse import parse_qsl


class OAuth(object):
    client_id = '726712071932346388'
    client_secret = 'Z5DRWc_Lgg089x3ey6JnOoMRG-zoz9zF'
    scope = 'email%20identify%20guilds'
    redirect_uri = 'http://10.10.10.103:8080/profile'
    discord_login_url = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}' \
                        f'&response_type=code&scope={scope}'
    discord_token_url = 'https://discord.com/api/oauth2/token'

    @staticmethod
    def get_access_token(code):
        data = {
            'client_id': OAuth.client_id,
            'client_secret': OAuth.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': OAuth.redirect_uri,
            'scope': 'identify email connections'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(OAuth.discord_token_url, data=data, headers=headers)
        r.raise_for_status()
        return r.json().get('access_token')
