from odoo import http
from odoo.http import request
from odoo import api

class DashboardController(http.Controller):
    @http.route('/dm_acct/dashboard', auth='user', website=True)
    def index(self, **kw):
        return request.render('demo_accounting_app.dashboard', {})
