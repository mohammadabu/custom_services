# -*- coding: utf-8 -*-
{
    'name': "Custom services",
    'author': "Mohammad abusubhia",
    'version': '1.1',
    'depends': ['base','crm','services','hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'data/ir_sequence_data.xml',
        # 'data/cron.xml',
        # 'data/delete_rules.xml',
        'data/data_projects_stages.xml',
        'data/mail_template.xml',
        'views/custom_main_project.xml',
        'views/custom_risk_project.xml',
        'views/custom_issue_register.xml',
        'views/custom_change_log.xml',
        # 'views/custom_tasks.xml',
        # 'reports/internal_project_detail_qweb_report.xml',
        # 'reports/report.xml',
    ],
}