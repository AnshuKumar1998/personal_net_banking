def save_google_credentials(strategy, details, response, *args, **kwargs):
    if 'access_token' in response:
        credentials = {
            'access_token': response['access_token'],
            'refresh_token': response.get('refresh_token'),
            'token_uri': response.get('token_uri'),
            'client_id': response.get('client_id'),
            'client_secret': response.get('client_secret'),
            'scope': response.get('scope')
        }
        strategy.session_set('google_oauth2_credentials', credentials)
        print("Credentials saved to session:", credentials)
    else:
        print("No access_token in response")


