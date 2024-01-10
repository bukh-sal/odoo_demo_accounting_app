{
    'name': "Accounting Demo",
    'version': '1.23',
    'depends': [
        'base',
    ],
    'author': "Salman",
    'category': 'Tools',
    'description': """
    A Simple recreation of etamid's accounting in odoo
    """,
    # data files always loaded at installation
    'data': [
        'views/dm_acct_dashboard.xml',
        'views/dm_acct_accounts.xml',
        'views/dm_acct_revenues.xml',
        'views/dm_acct_expenses.xml',
        'views/dm_acct_transfers.xml',
        'views/dm_acct_income_types.xml',
        'views/dm_acct_categories.xml',
        'views/dm_acct_menu.xml',
    ],
    'application': True,
    'installable': True,
}
