{
    'name': 'ST Plaid Link Statement Importer',
    'version': '1.0',
    'category': 'Accounting',
    'author': 'Jacob Sims',
    'depends': ['base', 'web'],
    'assets': {
        'web.assets_backend': [
            'static/src/js/plaid_link.js',
        ],
    },
    'data': [
        'views/plaid_link_template.xml',
        'views/base_view.xml',
        # 'security/ir.model.access.csv',
    ],
    'qweb': [
        'static/src/xml/plaid_link_template.xml',
    ],
    'installable': True,
    'application': True,
}

