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
    'name': 'TCD Profile',
    'version': '0.1',
    'author': 'Mars & Moore',
    'category': 'Generic Module',
    'website': 'http://www.Mars & Moore.com',
    'summary': 'TCD Profile',
    'description': """
        Installation module for TCD
    """,
    'depends': [
        'tcd_project',
        'theme_graphene',
        'website_crm',
        'tcd_website',
        'partner_firstname',
        'project_details_view',
    ],
    'data': [
        'data/company_data.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
