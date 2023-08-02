from odoo import http
from odoo.http import request

class PlaidController(http.Controller):

    @http.route('/plaid/token-exchange', type='json', auth='user')
    def plaid_token_exchange(self, public_token, accounts, **kw):
        # Your token exchange and user settings update logic here

        # Assuming accounts is a list of dictionaries containing account information
        if not accounts:
            return {'error': 'No accounts linked'}

        # Extract relevant account information (customize this based on your needs)
        account_data = []
        for account in accounts:
            account_data.append({
                'account_name': account.get('name'),
                'account_type': account.get('type'),
                'account_number': account.get('mask')
            })

        # Update the user's res.users settings with the account information
        user = request.env.user
        user.write({'plaid_accounts': account_data})

        return {'success': True}