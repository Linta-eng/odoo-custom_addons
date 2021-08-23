# -*- coding: utf-8 -*-

from odoo import models, fields, api
from itertools import groupby

class CustomerReport(models.AbstractModel):
	_name="customer_statement.customer_statement_pdf"
	_description = "Customer Statement"

	

    def _get_report_values(self, docids, data=None):   
        d = { }
        partner = self.env['res.partner'].browse(docids)  
        for key, inv in groupby(p_id.sorted(key=lambda r: r.partner_id.id)):
            inv = list(inv)
            if key[1]:     
                d.setdefault(str(key[0].id), {}).setdefault('open_invoices', []).extend([{
                    'ref': i.number,
                    'amount_total': i.amount_total,
                    'invoice_date': i.date_invoice,
                    'due_date': i.date_due
                } for i in inv if i.state == 'open'])

                d.setdefault(str(key[0].id), {}). setdefault('paid_invoices', []).extend([{
                    'ref': i.number,
                    'amount_paid': p_move.credit,
                    'invoice_date': p_move.date,
                } for i in inv if i.state == 'paid'])
           
        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'data' : data,
            'docs': partner,
            'company_id': self.env.user.company_id,
            'report_date': '%s / %s' % (start_date, end_date)
                   }