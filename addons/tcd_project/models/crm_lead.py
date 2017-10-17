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


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    website = fields.Char(string='Website')
    opportunity_type = fields.Selection([
        ('Investor', 'Investor'),
        ('Entrepreneur', 'Entrepreneur')
    ])
    investment_type = fields.Selection([
        ('seed_capital', 'Seed Capital'),
        ('a_serie', 'A serie'),
        ('b_serie', 'B serie'),
        ('c_serie', 'C serie'),
    ])
    investment_size = fields.Float("Investment size")
    sector_ids = fields.Many2many('tcd.sector', string="Sectors")
    general_conditions_accepted = fields.Boolean("General Conditions Accepted")

    @api.constrains('investment_size')
    def _check_investment(self):
        if self.investment_size < 0:
            raise Warning("Investment can't be a negative number")

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        partner_id = super(CRMLead, self)._lead_create_contact(
            lead, name, is_company, parent_id)

        partner = self.env['res.partner'].browse(partner_id)
        values = {
            'investment_type': lead.investment_type,
            'investment_size': lead.investment_size,
            'website': lead.website,
        }
        if lead.sector_ids:
            values['sector_ids'] = [(4, lead.sector_ids.ids)]
        if lead.opportunity_type == 'Investor':
            values['is_investor'] = True
        elif lead.opportunity_type == 'Entrepreneur':
            values['is_entrepreneur'] = True

        partner.write(values)
        return partner_id
