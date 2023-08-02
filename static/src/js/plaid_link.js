
odoo.define('st_odoo_statements.plaid_link', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var PlaidLink = Widget.extend({
        template: 'st_odoo_statements.plaid_link_template',

        start: function () {
            this.$('#link-button').click(this._onLinkButtonClick.bind(this));
            return this._super();
        },

        _onLinkButtonClick: function () {
            // Initialize Plaid Link
            var linkHandler = Plaid.create({
                clientName: 'ST Odoo Statements',
                env: 'sandbox',  // Replace with 'development' or 'production' in production environment
                key: 'your_plaid_public_key',
                product: ['auth', 'transactions'], // or ['auth', 'identity', 'transactions'] for additional data
                onSuccess: this._onSuccess.bind(this),
            });

            // Open the Plaid Link interface
            linkHandler.open();
        },

        _onSuccess: function (publicToken, metadata) {
            // Handle the Plaid Link success event here
            // You can send the publicToken to the server for token exchange
            // Also, you can access account data in metadata.accounts and process it
            var self = this;
            this._rpc({
                route: '/plaid/token-exchange',
                params: {
                    public_token: publicToken,
                    accounts: metadata.accounts
                }
            }).then(function (result) {
                if (result.success) {
                    // Refresh the view to show updated account information
                    self.reload();
                } else {
                    // Handle error if needed
                }
            });
        }
    });

    core.action_registry.add('st_odoo_statements.plaid_link_action', PlaidLink);
    return PlaidLink;
});