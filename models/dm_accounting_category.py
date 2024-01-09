from odoo import models, fields, api

class Category(models.Model):
    _name = 'dm.accounting.category'
    _description = 'Category'

    name = fields.Char(required=True)