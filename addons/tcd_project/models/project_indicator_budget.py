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


class ProjectIndicatorBudget(models.Model):
    _name = 'tcd.indicator.budget'

    date = fields.Date(string="date", required=True)
    budget = fields.Float(string="budget", required=True)
    actual = fields.Float(string="actual")
    indicator_id = fields.Many2one('tcd.indicator', string="Indicator")
    difference_in_percent = fields.Float(
        'Difference %',
        compute="_compute_difference_in_percent",
    )
    difference_in_cash = fields.Float(
        'Difference €',
        compute="_compute_difference_in_cash",
    )
    difference_in_percent_formatted = fields.Text(
        'Difference %',
        compute="_compute_difference_in_percent_formatted"
    )
    difference_in_cash_formatted = fields.Text(
        'Difference €',
        compute="_compute_difference_in_cash_formatted"
    )
    total_budget = fields.Float("Total Budget")
    total_actual = fields.Float("Total Actual")


    @api.onchange('budget')
    def on_change_budget(self):
#       budget = fields.Float(self.budget)
        if self.actual == 0:
           self.actual = self.budget

    @api.one
    def _compute_difference_in_percent(self):
        if self.budget > 0:
            self.difference_in_percent = (self.actual / self.budget -1)

    @api.one
    def _compute_difference_in_cash(self):
        self.difference_in_cash = self.actual - self.budget

    @api.one
    def _compute_difference_in_percent_formatted(self):
        percent = round(self.difference_in_percent * 100, 2)
        self.difference_in_percent_formatted = str(percent) + " %"

    @api.one
    def _compute_difference_in_cash_formatted(self):
        self.difference_in_cash_formatted = str(self.difference_in_cash) + " €"

    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False, lazy=True):
        res = super(ProjectIndicatorBudget, self).read_group(cr, uid, domain, fields, groupby, offset, limit=limit, context=context, orderby=orderby, lazy=lazy)
        if 'difference_in_percent' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(cr, uid, line['__domain'], context=context)
                    total = 0.0
                    counter = 0
                    for indicator_value in self.browse(cr, uid, lines, context=context):
                        total += indicator_value.difference_in_percent
                        counter += 1
                    line['difference_in_percent'] = total/counter
        if 'difference_in_cash' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(cr, uid, line['__domain'], context=context)
                    total = 0.0
                    for current_indicator in self.browse(cr, uid, lines, context=context):
                        total += current_indicator.difference_in_cash
                    line['difference_in_cash'] = total
        return res