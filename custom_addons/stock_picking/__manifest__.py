# -*- coding: utf-8 -*-

{
	'name' : "Stock Picking Batch",
    'author' : "Linta",
	'summary' : """Batches are Picked""",
	'sequence': -22,

	'description' : "Support in IoS and Android",

	'version' : "3.2",

	'category' : "Uncategorized",
	'depends' : ['base',
	             'contacts',
	             'stock',
	             'mail'],

	'data' : ['security/ir.model.access.csv',
	         'data/stock_picking_data.xml',
	         'views/stock_picking_views.xml',
	         'views/stock_batch_picking_views.xml',
	         'views/delivery_route_views.xml',
	         'report/batch_report.xml',
	         'report/batch_report_template.xml',
	         'data/mail_template.xml',]
}