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
from openerp import models, api


class BaseLanguageInstall(models.TransientModel):
    _inherit = "base.language.install"

    @api.model
    def install_language(self, lang_code):
        self = self.create({
            'lang': lang_code,
            'overwrite': True,
        })
        result = self.lang_install()
        return result


class WebsiteConfigSettings(models.TransientModel):
    _inherit = "website.config.settings"

    @api.model
    def update_website_settings(self):
        languages_ids = self.env['res.lang'].search([]).ids

        # Set all installed languages as available on the website
        self = self.create({
            'language_ids': [(6, 0, [languages_ids])],
        })
        self.execute()
