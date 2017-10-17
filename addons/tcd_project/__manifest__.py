# -*- encoding: utf-8 -*-
# ############################################################################
#
#    Copyright Mars & Moore (C) 2016
#    Author: Mars & Moore
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'TCD Project',
    'version': '0.1',
    'author': 'Mars & Moore',
    'category': 'Project Management',
    'website': 'http://www.Mars & Moore.com',
    'summary': 'Project customization for TCD',
    'description': """
        Project customization for TCD
    """,

    'depends': [
        'project',
        'crm',
        'document',
    ],
    'data': [
        'security/tcd_security.xml',
        'security/ir.model.access.csv',
        'data/sectors_data.xml',
        'data/crm_data.xml',
        'views/resources.xml',
        'views/project_view.xml',
        'views/project_task_category_view.xml',
        'views/project_task_view.xml',
        'views/tcd_clubbers_view.xml',
        'views/tcd_indicator_view.xml',
        'views/tcd_indicator_budget_view.xml',
        'views/crm_lead_view.xml',
        'views/res_partner_view.xml',
    ],
    'css': ['static/src/css/tcd_project.css'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
