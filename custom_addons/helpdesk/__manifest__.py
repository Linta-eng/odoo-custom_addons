# -*- coding: utf-8 -*-
{
	'name':'HELP-DESK',
	'author':'Aarshit',
	'version':'1.1',
	
	'summary':'HelpDesk system',
	
	'sequence':-2,
	'description':'This is a Helpdesk system',
	'category':'Uncategorized',
	
	'depends':['base',
			   'mail'],
	
	'data':[
			"security/ir.model.access.csv",
			"views/customer_views.xml",
			"views/profile_views.xml",
			"reports/report.xml",
			"reports/report_card.xml",
			"data/data.xml",
			"data/mail_template.xml"

			]

}
