from odoo import fields, models

class PlaidLinkWizard(models.TransientModel):
    _name = 'plaid.link.wizard'
    _description = 'Plaid Link Wizard'

    # Add fields for the account lines in the wizard
    account_lines = fields.One2many('plaid.link.wizard.line', 'wizard_id', string='Account Lines')

    def save_selected_accounts(self):
        user = self.env.user
        selected_accounts = self.account_lines.filtered(lambda line: line.selected)
        account_data = []
        for account in selected_accounts:
            account_data.append({
                'account_name': account.account_name,
                'account_type': account.account_type,
                'account_number': account.account_number,
            })
        user.write({'plaid_accounts': account_data})

    def open_wizard(self):
        # Add any necessary logic to perform when opening the wizard
        # For example, you can set default values for fields, etc.
        return {
            'name': 'Plaid Link Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'plaid.link.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self.env.context,
        }

class PlaidLinkWizardLine(models.TransientModel):
    _name = 'plaid.link.wizard.line'
    _description = 'Plaid Link Wizard Line'

    # Define fields for the account line data
    wizard_id = fields.Many2one('plaid.link.wizard', string='Wizard')
    account_name = fields.Char(string='Account Name')
    account_type = fields.Char(string='Account Type')
    account_number = fields.Char(string='Account Number')
    selected = fields.Boolean(string='Selected')
