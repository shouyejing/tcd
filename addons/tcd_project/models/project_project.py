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

import logging


class Project(models.Model):
    _inherit = 'project.project'

    image = fields.Binary('Image')
    description = fields.Html('Description')
    clubber_ids = fields.One2many('tcd.clubbers', 'project_id',
                                  string='Clubbers')
    clubber_count = fields.Integer('Number of clubbers',
                                   compute='_count_clubber')
    indicator_ids = fields.One2many('tcd.indicator', 'project_id',
                                    string='Indicators')
    indicator_average = fields.Float(string="Average",
                                     compute='_compute_indicator_average')
    clubber_partner_ids = fields.Many2many('res.partner',
                                           compute='get_clubber_partner_ids',
                                           search='search_clubber_partner_ids')
    tag_ids = fields.Many2many('project.tags', 'project_tags_rel',
                               'project_id', 'tag_id', string="Tags")

    @api.depends('clubber_ids')
    def get_clubber_partner_ids(self):
        for project in self:
            partner_ids = set()
            for clubber in project.clubber_ids:
                partner_ids.add(clubber.partner_id.id)
            project.partner_ids = [(6, 0, partner_ids)]

    def search_clubber_partner_ids(self, operator, value):
        return [('clubber_ids.partner_id', operator, value)]

    @api.depends('clubber_ids')
    def _count_clubber(self):
        print 'debugging'
        return 999

    @api.depends('indicator_ids')
    def _compute_indicator_average(self):
        for project in self:
            average = 0
            if project.indicator_ids:
                rating_sum = 0.0
                for indicator in project.indicator_ids:
                    rating_sum += float(indicator.rating)
                average = round(rating_sum / len(project.indicator_ids), 1)
            project.indicator_average = average
