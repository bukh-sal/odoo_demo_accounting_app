from odoo import models, fields, api

class Revenue(models.Model):
    _name = 'dm.accounting.revenue'
    _description = 'Revenue Model'

    account = fields.Many2one(
        "dm.accounting.account",
        ondelete="cascade",
        required=True,
        string="Account"
    )
    income_type = fields.Many2one(
        "dm.accounting.income.type",
        ondelete="cascade",
        required=True,
        string="Income Type"
    )
    customer = fields.Many2one(
        "res.partner",
        ondelete="cascade",
        required=True,
        string="Customer"
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

    @api.model
    def create(self, vals):
        obj = super(Revenue, self).create(vals)
        obj.account.balance += obj.amount
        return obj

    def write(self, vals):
        prv_amount = self.amount
        res = super(Revenue, self).write(vals)
        new_amount = self.amount
        # modify the parent account by delta to correct for the update
        self.account.balance += new_amount - prv_amount        
        return res

    def unlink(self):
        self.account.balance -= self.amount
        return super(Revenue, self).unlink()