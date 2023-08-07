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
            console.log('Fetching Plaid settings from server...');
                    
            rpc.query({
                model: 'plaid.link.settings',
                method: 'search_read',
                args: [[]],
                fields: ['plaid_client_id', 'client_name', 'plaid_link_token'],
                limit: 1,
            }).then(function (result) {
                console.log('Fetched Plaid settings:', result);
                if (result && result.length > 0) {
                    var settings = result[0];
                    var linkHandler = Plaid.create({
                        clientName: settings.client_name,
                        env: 'sandbox',
                        token: settings.plaid_link_token, // Make sure this value is correctly retrieved
                        product: ['auth', 'transactions'],
                        onSuccess: function (publicToken, metadata) {
                            console.log('Plaid Link onSuccess triggered:', publicToken, metadata);
                            self._onSuccess(publicToken, metadata);
                        },
                        onLoad: function() {
                            console.log('Plaid Link: Initialized inside iframe');
                        },
                        onExit: function(err, metadata) {
                            console.log('Plaid Link onExit triggered:', err, metadata);
                        },
                    });
        
                    linkHandler.open();
                } else {
                    console.log('No Plaid settings found.');
                    self.do_warn('Error', 'No Plaid settings found.');
                }
            }).guardedCatch(function (error) {
                console.log('Error retrieving Plaid settings:', error);
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
