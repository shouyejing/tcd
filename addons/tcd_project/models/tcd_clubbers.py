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
from openerp import models, fields, api
from openerp.exceptions import Warning


class Clubber(models.Model):
    _name = 'tcd.clubbers'

    project_id = fields.Many2one('project.project', string="Project",
                                 required=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 required=True)
    role = fields.Selection([
        ('investor', 'Investor'),
        ('board', 'Board member'),
        ('tcd', 'The Club Deal'),
    ], string='Role', required=True)
    investment = fields.Float('Investment')
    ownership = fields.Float('Ownership in %')
    shares = fields.Integer('Nbr of Shares')

    @api.constrains('investment')
    def _check_investment(self):
        if self.investment <= 0:
            raise Warning('Investment must be more than zero')

    _sql_constraints = [
        ('partner_project_unique', 'unique (project_id, partner_id)',
         "A Clubber with the same Project and Partner already exists"),
    ]
