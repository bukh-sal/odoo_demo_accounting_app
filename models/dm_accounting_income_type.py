from odoo import models, fields, api

class IncomeType(models.Model):
    _name = 'dm.accounting.income.type'
    _description = 'Income Type'

    name = fields.Char(required=True)