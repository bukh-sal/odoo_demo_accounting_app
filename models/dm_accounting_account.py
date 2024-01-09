from odoo import models, fields, api

class Account(models.Model):
    _name = 'dm.accounting.account'
    _description = 'Account Model'

    name = fields.Char(
        string="Name",
        required=True,
    )
    starting_balance = fields.Float(
        string="Starting Balance",
        required=True,
        default=0.00,
    )
    balance = fields.Float(
        string="Balance",
        required=True,
        default=0.00,
    )

    @api.model
    def create(self, vals):
        obj = super(Account, self).create(vals)
        obj.balance = obj.starting_balance
        return obj

    def write(self, vals):
        if 'starting_balance' in vals:
            current_balance = self.balance
            currnet_starting_balance = self.starting_balance
            new_starting_balance = vals['starting_balance']
            diff = new_starting_balance - currnet_starting_balance
            new_balance = current_balance + diff
            vals['balance'] = new_balance
        return super(Account, self).write(vals)
    
