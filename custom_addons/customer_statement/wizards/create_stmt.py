# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CreateStatement(models.TransientModel):
   _name = 'create.statement.wizard'
   _description = 'Customer statement wizard'

   start_date = fields.Date("Start Date", required=True)
   end_date = fields.Date("End Date", required=True)
   p_id = fields.Many2many('res.partner', string="Recipients")


   def customer_statement(self):
     p_id = self.env['account.move'].search([
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date),
            ('state', 'in', ['open', 'paid'])
        ]).mapped('partner_id')

     report = self.env.ref('customer_statement.report_customer_statement_pdf')
     pdf_customer = p_id.filtered(lambda p: p.statement_method == 'pdf')
     return report.report_action(pdf_customer,data={
                'date_range': {
                    'd_from': self.start_date,
                    'd_to': self.end_date}
            })
        

       
