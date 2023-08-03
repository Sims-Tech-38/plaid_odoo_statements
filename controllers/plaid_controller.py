from odoo import http
from odoo.http import request

class PlaidController(http.Controller):

    @http.route('/plaid/link', type='json', auth='user')
    def plaid_link(self, public_token, accounts, **kw):
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

        # Create the wizard model and add account lines
        WizardModel = request.env['your.wizard.model']  # Replace 'your.wizard.model' with the actual model name
        wizard = WizardModel.create({})  # Create a new wizard record
        wizard.account_lines = [(0, 0, line) for line in account_data]  # Add account lines

        return {'success': True}