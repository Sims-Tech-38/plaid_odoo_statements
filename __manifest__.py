{
    'name': 'ST Plaid Link Statement Importer',
    'version': '1.0',
    'category': 'Accounting',
    'author': 'Jacob Sims',
    'depends': ['base', 'web'],
    'assets': {
        'web.assets_backend': [
            '/plaid_odoo_statements/static/src/js/plaid_link.js',
        ],
    },
    'qweb': [
        '/plaid_odoo_statements/static/src/xml/plaid_link_template.xml',
    ],
    'data': [
        'data/action.xml',
        'views/res_users.xml',
        'views/base_view.xml',
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}

