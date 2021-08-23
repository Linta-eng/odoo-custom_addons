# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Invoices(models.Model):
    _inherit = 'account.move'
    
