# plaid_account.py

from odoo import fields, models

class PlaidAccount(models.Model):
    _name = 'st_odoo_statements.plaid_account'
    _description = 'Plaid Account'

    user_id = fields.Many2one('res.users', string='User', ondelete='cascade')
    name = fields.Char(string='Account Name')
    type = fields.Char(string='Account Type')
    number = fields.Char(string='Account Number')
    access_key = fields.Char(string='Access Key')
