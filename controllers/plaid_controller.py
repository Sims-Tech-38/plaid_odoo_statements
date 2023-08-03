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
        WizardModel = request.env['plaid.link.wizard']  # Replace 'your.wizard.model' with the actual model name
        wizard = WizardModel.create({})  # Create a new wizard record
        wizard.account_lines = [(0, 0, line) for line in account_data]  # Add account lines

        return {'success': True}

    @http.route('/plaid/link/settings', auth='user')
    def get_plaid_settings(self, **kw):
        # Retrieve Plaid settings from the server
        SettingsModel = request.env['plaid.link.settings']  # Replace 'plaid.link.settings' with the actual model name
        settings = SettingsModel.sudo().search([], limit=1)  # Assuming there's only one record

        if settings:
            return {
                'plaid_client_id': settings.plaid_client_id,
                'client_name': settings.client_name,
            }
        else:
            return {'error': 'No Plaid settings found.'}
