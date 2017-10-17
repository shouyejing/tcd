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
    'name': 'TCD Website',
    'version': '0.1',
    'author': 'Nicolas de Moreau',
    'category': 'Website',
    'website': 'http://www.marsmoore.com',
    'summary': 'Website templates for TCD',
    'description': """
        Website templates for TCD
    """,

    'depends': [
        'website',
        'website_sale',
        'theme_graphene',
        'theme_tcd'
    ],
    'data': [
        'views/tcd_website_assets.xml',
        'views/home_template.xml',
        'views/entrepreneurs_template.xml',
        'views/investors_template.xml',
        'views/product_view.xml',
        #        'views/tcd_website_events.xml',
        'views/preset_theme_graphene.xml',
        'views/stor_it_template.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
