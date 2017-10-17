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
    'name': 'TCD Website Event',
    'version': '0.1',
    'author': 'Nicolas de Moreau',
    'category': 'Website',
    'website': 'http://www.marsmoore.com',
    'summary': 'Website Events on Invitation',
    'description': """
        Website Events on Invitation
    """,

    'depends': [
        'event',
        'website',
        'link_tracker',
        'website_event',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/tcd_website_event_assets.xml',
        #'views/tcd_website_event_security.xml',
        'views/tcd_event_invitee_view.xml',
        'views/tcd_event_view.xml',
        'views/tcd_website_events.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
