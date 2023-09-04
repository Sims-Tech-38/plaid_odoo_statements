from odoo import fields, models
import plaid
from plaid.api import plaid_api
import logging
_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    plaid_access_token = fields.Char(string='Plaid Access Token', password=True, readonly=True)
    plaid_accounts = fields.One2many('st_odoo_statements.plaid_account', 'user_id', string='Plaid Accounts')
    plaid_settings_id = fields.Many2one('plaid.link.settings', string='Plaid Settings')

    def open_plaid_link_wizard(self):
        wizard = self.env['plaid.link.wizard'].create({})
        return wizard.open_wizard()

    def update_plaid_info(self, public_token, metadata):
        # _logger.info(f"Type of plaid module: {type(plaid)}")
        # _logger.info(f"Attributes of plaid module: {dir(plaid)}")
        accounts = metadata.get('accounts', [])
        _logger.info('Accounts: %s', accounts)
        account_names = self.create_plaid_accounts(accounts)
        access_token = self.get_access_key(public_token)

        for acc_name in account_names:
            account_obj = self.env['st_odoo_statements.plaid_account'].search([('name', '=', acc_name), ('user_id', '=', self.id)])
            if account_obj:
                account_obj.write({
                    'access_key': access_token
                })

    def get_access_key(self, public_token):
        client_id = self.plaid_settings_id.plaid_client_id
        secret = self.plaid_settings_id.plaid_secret
        environment = self.plaid_settings_id.plaid_environment

            # Initialize Plaid client
        configuration = plaid.configuration(
            host=plaid.environment[environment],
            api_key={
                'clientId': client_id,
                'secret': secret,
            }
        )

        api_client = plaid.ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)
        exchange_response = client.Item.public_token.exchange(public_token)
        return exchange_response['access_token']

    def create_plaid_accounts(self, accounts):
        created_account_names = []
        for acc in accounts:
            created_account = self.env['st_odoo_statements.plaid_account'].create({
                'user_id': self.id,
                'name': acc['name'],
                'type': acc['subtype'],  # Assuming that 'subtype' exists
                'number': acc['id'],  # Assuming that 'account_id' exists
            })
            created_account_names.append(created_account.name)
        return created_account_names