odoo.define('st_odoo_statements.plaid_link_wizard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var PlaidLinkWizard = AbstractAction.extend({
        start: function () {
            this.displayPlaidDialog();
            return this._super();
        },

        displayPlaidDialog: function () {
            var self = this;

            var dialog = new Dialog(this, {
                title: 'Connect to Plaid',
                size: 'medium',
                buttons: [{text: 'Close', close: true}]
            });

            dialog.opened().then(function() {
                self.initializePlaid(dialog.$el);  // Pass the content element of the dialog to the Plaid initialization.
            });

            dialog.open();
        },

        initializePlaid: function($contentElement) {
            console.log('Initializing Plaid!'); 
            var self = this;
            rpc.query({
                model: 'plaid.link.settings',
                method: 'search_read',
                args: [[]],
                fields: ['plaid_client_id', 'client_name'],
                limit: 1,
            }).then(function (result) {
                if (result && result.length > 0) {
                    var settings = result[0];
                    var linkHandler = Plaid.create({
                        clientName: settings.client_name,
                        env: 'sandbox',
                        key: settings.plaid_client_id,
                        product: ['auth', 'transactions'],
                        onSuccess: function (publicToken, metadata) {
                            self._onSuccess(publicToken, metadata);
                        },
                        onLoad: function() {
                            console.log('Plaid Link: Initialized inside iframe');
                        },
                    });

                    linkHandler.open();
                } else {
                    self.do_warn('Error', 'No Plaid settings found.');
                }
            }).guardedCatch(function (error) {
                self.do_warn('Error', 'Failed to retrieve Plaid settings. Error: ' + error.message);
            });
        },

        _onSuccess: function (publicToken, metadata) {
            // Rest of your code for handling success...
        }
    });

    core.action_registry.add('plaid.link.wizard.action', PlaidLinkWizard);
    return PlaidLinkWizard;
});
