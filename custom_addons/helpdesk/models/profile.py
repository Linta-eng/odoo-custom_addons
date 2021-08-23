#-*- coding: utf-8 -*-


from odoo import fields,models,api,_
from odoo.exceptions import ValidationError
from datetime import datetime

AVAILABLE_PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High')]
	
class Profile(models.Model):
	_name = "new.profile"
	_description = "User System"
	_rec_name = 'customer'

	help_team = fields.Selection([('purchase','Purchase Team'),('development','Development Team'),('debug','Debug Team')],default='development')
	assigned = fields.Many2one('res.users', string="Assigned To")
	customer = fields.Many2one('res.partner', string='CUSTOMER')
	cust_name = fields.Char(related='customer.name',string='CUSTOMER Name')
	cust_email = fields.Char(related='customer.email',string='CUSTOMER EMAIL')
	date_from = fields.Date(string='Date', default=datetime.today())
	set_priority=fields.Selection(AVAILABLE_PRIORITIES, string='Priority', select=True)
	state = fields.Selection([('new','New'),('inprogress','InProgress'),('solved','Solved'),('closed','Closed'),('completed','Completed')],default='new')
	description = fields.Text()

	@api.onchange('state')
	def change_state(self):
		if self.state=='inprogress':
			template_id = self.env.ref('helpdesk.customer_templatee').id
			print("template_id",template_id)
			self.env.ref('helpdesk.customer_templatee').send_mail(['self.id'], force_send=True)

		elif self.state=='solved':
			print("Solved")


	def btn(self):
		print("InProgress")
		template_id = self.env.ref('helpdesk.customer_templatee').id
		print("template_id",template_id)
		self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

	def solbtn(self):
		self.state = 'solved'
		print("Solved")
		solved_id = self.env.ref('helpdesk.solved_templatee').id
		print("solved_id",solved_id)
		self.env['mail.template'].browse(solved_id).send_mail(self.id, force_send=True)