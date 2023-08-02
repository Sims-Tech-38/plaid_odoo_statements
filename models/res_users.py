from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    plaid_access_token = fields.Char(string='Plaid Access Token', password=True, readonly=True)
    plaid_accounts = fields.One2many('st_odoo_statements.plaid_account', 'user_id', string='Plaid Accounts')