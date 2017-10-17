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

INDICATOR_RATINGS = [
    ('0', 'Very bad'),
    ('1', 'Bad'),
    ('2', 'Sufficient'),
    ('3', 'Good'),
    ('4', 'Very Good'),
]


class ProjectIndicator(models.Model):
    _name = 'tcd.indicator'

    name = fields.Char(string="Name", required=True)
    rating = fields.Selection(INDICATOR_RATINGS, required=True)
    project_id = fields.Many2one('project.project', string="Project",
                                 required=True)
    budget_ids = fields.One2many(
           'tcd.indicator.budget',    # related model
           'indicator_id',     # field for "this" on related model
           string='Budgets')
    unit = fields.Char(string="Units")
    total_budget = fields.Float('Total Budget')
    total_actual = fields.Float('Total Actual')

    @api.onchange('budget_ids')
    def _compute_totals(self):
        for indicator in self:
            total_budget = 0
            total_actual = 0
            if indicator.budget_ids:
                for budget in indicator.budget_ids:
                    total_budget += budget.budget
                    total_actual += budget.actual
            indicator.total_budget = total_budget
            indicator.total_actual = total_actual
