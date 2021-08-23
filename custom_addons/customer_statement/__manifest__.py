{
	'name' : 'Customer Statement',
	'summary' : 'Statement',
	'version' : '1.1',
	'description' : 'This is a customer statement',
	'category' : 'Statement',
	'website' : 'http://www.mystatement.com',
	'author' : 'My statement',
	'depends' : ['base','account','mail'],
	'data' : [
		'security/ir.model.access.csv',
		'views/res_partner.xml',
		'wizards/create_smt.xml',
		'reports/custom_report.xml',
		'data/mail_template.xml'
		 ]
}