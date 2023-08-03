import requests
from odoo import api, fields, models

class PlaidLinkSettings(models.Model):
    _name = 'plaid.link.settings'
    _description = 'Plaid Link Settings'

    # Add any fields you need for Plaid settings here
    plaid_client_id = fields.Char(string='Plaid Client ID', required=True)
    plaid_secret = fields.Char(string='Plaid Secret', required=True)
    plaid_link_token = fields.Char(string='Plaid Link Token')
    client_name = fields.Char(string='Client Name', default='Your Client Name')

    def create_plaid_link_token(self):
        # Set your Plaid credentials here
        client_id = self.plaid_client_id
        secret = self.plaid_secret
        client_name = self.client_name

        # Set any other required parameters for the token creation
        # For example, you might want to pass the user_id or other relevant data
        user_id = self.env.user.id

        # Make a request to Plaid's /link/token/create endpoint to get the link_token
        payload = {
            'client_id': client_id,
            'secret': secret,
            'user': {
                'client_user_id': str(user_id)
                # Add any other relevant user data if required
            },
            'client_name': client_name,  # This can be any name you want to display to the user
            'products': ['auth', 'transactions'],  # or ['auth', 'identity', 'transactions'] for additional data
            'country_codes': ['US'],  # Replace with the relevant country code
            'language': 'en',  # Replace with the relevant language code
        }

        response = requests.post('https://sandbox.plaid.com/link/token/create', json=payload)

        if response.status_code == 200:
            data = response.json()
            link_token = data.get('link_token')
            if link_token:
                self.plaid_link_token = link_token
            else:
                raise ValueError('Failed to get link_token from Plaid API')
        else:
            raise ValueError('Failed to obtain link_token from Plaid API: {}'.format(response.text))