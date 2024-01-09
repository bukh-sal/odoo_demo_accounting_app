# validation
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api


# recalculates all accounts balances based on 
# starting balance, revenues, expenses, transfers_from, transfers_to
def _recalculate_balances(self):
    for account in self:
        account.balance = account.starting_balance
        revenues = self.env['dm.accounting.revenue'].search([('account', '=', account.id)])
        for revenue in revenues:
            account.balance += revenue.amount
        expenses = self.env['dm.accounting.expense'].search([('account', '=', account.id)])
        for expense in expenses:
            account.balance -= expense.amount
        transfers_from = self.env['dm.accounting.transfer'].search([('from_account', '=', account.id)])
        for transfer in transfers_from:
            account.balance -= transfer.amount
        transfers_to = self.env['dm.accounting.transfer'].search([('to_account', '=', account.id)])
        for transfer in transfers_to:
            account.balance += transfer.amount


class Transfer(models.Model):
    _name = 'dm.accounting.transfer'
    _description = 'Transfer Model'

    from_account = fields.Many2one(
        "dm.accounting.account",
        ondelete="cascade",
        required=True,
        string="From Account"
    )
    to_account = fields.Many2one(
        "dm.accounting.account",
        ondelete="cascade",
        required=True,
        string="To Account"
    )
    amount = fields.Float(
        required=True,
        default=0.00,
        string="Amount"
    )
    date = fields.Date(
        default=fields.Datetime.now,
        required=True,
        string="Date"
    )
    description = fields.Text(
        required=False,
        string="Description"
    )
    attachment = fields.Binary(
        string="File",
        required=False
    )

    def _valid_transfer(self, vals):
        if vals['from_account'] == vals['to_account']:
            raise ValidationError("From and To accounts must be different.")
        
        if vals['amount'] <= 0:
            raise ValidationError("Transfer amount must be greater than zero.")
        
        if vals['from_account'].balance < vals['amount']:
            raise ValidationError("From account balance is less than the transfer amount.")
        
        return True
    
    @api.model
    def create(self, vals):
        self._valid_transfer(vals)
        obj = super(Transfer, self).create(vals)
        obj.from_account.balance -= obj.amount
        obj.to_account.balance += obj.amount
        return obj
    
    def write(self, vals):
        self._valid_transfer(vals)
        prv_amount = self.amount
        prv_from_account = self.from_account
        prv_to_account = self.to_account
        res = super(Transfer, self).write(vals)
        new_amount = self.amount
        new_from_account = self.from_account
        new_to_account = self.to_account
        # modify the from_account by delta to correct for the update
        prv_from_account.balance += prv_amount
        new_from_account.balance -= new_amount
        # modify the to_account by delta to correct for the update
        prv_to_account.balance -= prv_amount
        new_to_account.balance += new_amount
        return res
    
    def unlink(self):
        self.from_account.balance += self.amount
        self.to_account.balance -= self.amount
        return super(Transfer, self).unlink()