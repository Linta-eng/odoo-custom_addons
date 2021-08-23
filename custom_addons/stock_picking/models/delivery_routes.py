# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.fields import Many2one


class DeliveryRoute(models.Model):
	_name = 'delivery.routes'

	name = fields.Char(string="Delivery")

	address = fields.Char(string="Address")
	country_id: Many2one = fields.Many2one('res.country', string="Country")