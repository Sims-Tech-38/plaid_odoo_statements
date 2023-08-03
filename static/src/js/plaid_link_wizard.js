odoo.define('st_odoo_statements.plaid_link_wizard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var PlaidLinkWizard = AbstractAction.extend({
        start: function () {
            var self = this;
            this.$('.btn-primary').on('click', function () {
                self._onLinkButtonClick();
            });
            return this._super();
        },

        _onLinkButtonClick: function () {
            console.log('Plaid Link Button clicked!'); // Check if this message appears in the browser console
            var self = this;
            rpc.query({
                model: 'plaid.link.settings',
                method: 'search_read',
                args: [[]], // Provide any domain or filter if needed
                fields: ['plaid_client_id', 'client_name'],
                limit: 1,
            }).then(function (result) {
                if (result && result.length > 0) {
                    // Assuming we only get one result, use the first record for link initialization
                    var settings = result[0];
                    var linkHandler = Plaid.create({
                        clientName: settings.client_name,
                        env: 'sandbox',  // Replace with 'development' or 'production' in the production environment
                        key: settings.plaid_client_id,
                        product: ['auth', 'transactions'], // or ['auth', 'identity', 'transactions'] for additional data
                        onSuccess: function (publicToken, metadata) {
                            self._onSuccess(publicToken, metadata);
                        },
                    });

                    // Open the Plaid Link interface
                    linkHandler.open();
                } else {
                    self.do_warn('Error', 'No Plaid settings found.');
                }
            }).guardedCatch(function (error) {
                self.do_warn('Error', 'Failed to retrieve Plaid settings.');
            });
        },

        _onSuccess: function (publicToken, metadata) {
            var self = this;
            // Send the publicToken and account data to the server
            this._rpc({
                route: '/plaid/token-exchange',
                params: {
                    public_token: publicToken,
                    accounts: metadata.accounts
                }
            }).then(function (result) {
                if (result.success) {
                    // Handle the success response from the server
                    // You can display a success message or perform additional actions
                    self.do_notify('Success', 'Plaid Link success!');

                    // Close the wizard after successful link
                    self.do_action({
                        type: 'ir.actions.act_window_close',
                    });
                } else {
                    // Handle the error response from the server
                    // You can display an error message or perform other actions
                    self.do_warn('Error', 'An error occurred during Plaid Link.');
                }
            });
        }
    });

    core.action_registry.add('plaid.link.wizard.action', PlaidLinkWizard);

    return PlaidLinkWizard;
});
