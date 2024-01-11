import json
from odoo import http
from odoo.http import Response
import datetime
import calendar

class AccountsAPI(http.Controller):
    @http.route('/hello', auth='public')
    def hello(self):
        return "Hello World"
    
    @http.route('/hello-rest', auth='public', methods=['GET'], csrf=False)
    def hello_rest(self):
        return json.dumps({'message': 'Hello World'})
    
    @http.route('/accounts', auth='user', methods=['GET'], csrf=False)
    def get_accounts(self):
        accounts = http.request.env['dm.accounting.account'].search([])
        data = []
        for account in accounts:
            data.append({
                'id': account.id,
                'name': account.name,
                'starting_balance': account.starting_balance,
                'balance': account.balance,
            })
        return json.dumps(data)
    
    # /api/cashflow/ by month (use current year)
    @http.route('/api/cashflow', auth='user', methods=['GET'], csrf=False)
    def get_cashflow(self):
        summary = {}

        year = datetime.datetime.now().year
        months = [
            f'January {year}',
            f'February {year}',
            f'March {year}',
            f'April {year}',
            f'May {year}',
            f'June {year}',
            f'July {year}',
            f'August {year}',
            f'September {year}',
            f'October {year}',
            f'November {year}',
            f'December {year}',
        ]

        for i in months:
            summary[i] = {
                'revenues': 0.00,
                'expenses': 0.00,
                'profits': 0.00,
            }

        # itterate over months and get the revenues for that month
        revenues = http.request.env['dm.accounting.revenue'].search([])
        for revenue in revenues:
            key = f'{revenue.date.strftime("%B")} {year}'
            summary[key]['revenues'] += revenue.amount

        # itterate over months and get the expenses for that month
        expenses = http.request.env['dm.accounting.expense'].search([])
        for expense in expenses:
            key = f'{expense.date.strftime("%B")} {year}'
            summary[key]['expenses'] += expense.amount

        # calculate profits
        for key in summary:
            summary[key]['profits'] = summary[key]['revenues'] - summary[key]['expenses']

        resp_body = json.dumps(summary)
        return Response(
            resp_body,
            status=200,
            mimetype='application/json'
        )

    @http.route('/api/cashflow/<string:start_date>/<string:end_date>', auth='user', methods=['GET'], csrf=False)
    def get_cashflow_by_date(self, start_date, end_date):
        summary = {}

        try:
            # start and end date are in the format YYYY-MM-DD
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response(
                'Invalid date format. Use YYYY-MM-DD',
                status=400,
                mimetype='application/json'
            )


        current_date = start_date

        while current_date <= end_date:

            m_start_date = current_date
            days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
            m_end_date = datetime.datetime(
                year=current_date.year,
                month=current_date.month,
                day=days_in_month,
            )
            
            if (current_date.month != start_date.month) and (current_date.year != start_date.year):
                m_start_date = datetime.datetime(
                    year=current_date.year,
                    month=current_date.month,
                    day=1,
                )

            if (current_date.month == end_date.month) and (current_date.year == end_date.year):
                m_end_date = end_date

            revenues = http.request.env['dm.accounting.revenue'].search([
                ('date', '>=', m_start_date),
                ('date', '<=', m_end_date),
            ])
            expenses = http.request.env['dm.accounting.expense'].search([
                ('date', '>=', m_start_date),
                ('date', '<=', m_end_date),
            ])
            r_sum = sum(revenues.mapped('amount'))
            e_sum = sum(expenses.mapped('amount'))
            summary[current_date.strftime('%B %Y')] = {
                'revenues': r_sum,
                'expenses': e_sum,
                'profits': r_sum - e_sum,
            }

            next_month = current_date.month + 1 if current_date.month < 12 else 1
            next_year = current_date.year + 1 if next_month == 1 else current_date.year
            current_date = datetime.datetime(
                year=next_year,
                month=next_month,
                day=1,
            )


        resp_body = json.dumps(summary)
        return Response(
            resp_body,
            status=200,
            mimetype='application/json'
        )