{
    'name': 'ST Plaid Link Statement Importer',
    'version': '1.0',
    'category': 'Accounting',
    'author': 'Jacob Sims',
    'depends': ['base', 'web'],
    'assets': {
        'web.assets_backend': [
            '/plaid_odoo_statements/static/src/js/plaid_link_wizard.js',
        ],
    },
    'qweb': [
        'static/src/xml/plaid_sdk_template.xml',
    ],
    'data': [
        'views/res_users.xml',
        'wizard/plaid_link_wizard.xml',
        # 'views/base_view.xml',
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}

