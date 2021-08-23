# -*- coding: utf-8 -*-

from odoo import models, fields


class Respartner(models.Model):

    _inherit = 'res.partner'
    
    stmt = fields.Selection([('email', 'Email'), ('pdf_report', 'Pdf')])
    

    