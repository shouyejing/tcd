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

import json
from werkzeug.exceptions import Forbidden

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.base.ir.ir_qweb.fields import nl2br
from odoo.addons.website.models.website import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import ValidationError
from odoo.addons.website_form.controllers.main import WebsiteForm

PPG = 20  # Products Per Page
PPR = 4   # Products Per Row
from openerp.addons.tcd_project.models.project_indicator \
    import INDICATOR_RATINGS

#Import logger
import logging, json
#Get the logger
_logger = logging.getLogger(__name__)

class TCDWebsite(http.Controller):

    def get_clubbers(self, user):
        clubber_obj = http.request.env['tcd.clubbers']
        clubbers = clubber_obj.search([
            ('partner_id', '=', user.partner_id.id)
        ])
        return clubbers

    def get_indicators(self, project):
        indicator_obj = http.request.env['tcd.indicator.budget']
        indicators = indicator_obj.search([
            ('indicator_id', 'in', project.indicator_ids.ids)
        ])
        return indicators

    def get_indicator_details(self, indicator):
        indicator_obj = http.request.env['tcd.indicator.budget']
        indicators = indicator_obj.search([
            ('indicator_id', '=', indicator.id)
        ])
        return indicators
    def update_func(self):
        values = {}
        return http.request.render(
            'tcd_website.project_indicator_details_template2', values)

    def get_projects(self, clubbers):
        project_obj = http.request.env['project.project']
        projects = project_obj.search([
            ('clubber_ids', 'in', clubbers.ids),
        ], order="name asc")
        return projects

    def get_project_tasks_categories(self, clubbers):
        project_tasks_categories = {}
        task_category_obj = http.request.env['project.task.category']
        for clubber in clubbers:
            tasks = clubber.project_id.task_ids
            if clubber.role == 'board':
                # Board members can see tasks with 'Board Member' and
                # 'Investor' categories
                tasks = tasks.filtered(
                    lambda t: t.category_id.role in ['board', 'investor'])
            elif clubber.role == 'investor':
                # Investors can only see tasks with 'Investor' category
                tasks = tasks.filtered(
                    lambda t: t.category_id.role in ['investor'])
            categories = task_category_obj.browse(
                set([task.category_id.id for task in tasks])
            )

            project_tasks_categories[clubber.project_id.id] = categories
        return project_tasks_categories

    def get_project_category_tasks(self, project, task_category):
        """
        Return recordset of tasks for the given project that have the given
        category
        """
        task_obj = http.request.env['project.task']
        tasks = task_obj.search([
            ('project_id', '=', project.id),
            ('category_id', '=', task_category.id)
        ])

        return tasks

    def get_indicator_labels(self):
        """
        Get indicator labels used for the project.indicator model in its
        rating selection field
        """
        indicator_labels = {}
        for rating in INDICATOR_RATINGS:
            indicator_labels.update({
                rating[0]: rating[1],
            })
        return indicator_labels

    @http.route('/stor_it/', type='http', auth="user", website=True,
                multilang=True)
    def stor_it(self, **kwargs):
        user = request.env.user
        clubbers = self.get_clubbers(user)
        projects = self.get_projects(clubbers)

        project_clubber = {}
        for clubber in clubbers:
            project_clubber[clubber.project_id.id] = clubber

        values = {
            'projects': projects,
            'project_clubber': project_clubber,
        }
        return request.render("tcd_website.stor_it_template", values)

    @http.route('/stor_it/projects/<model("project.project"):project>',
                type='http', auth="user", website=True, multilang=True)
    def project(self, project):
        _logger.debug("Use _logger.debug for debugging purposes, nothing else ")
        user = request.env.user
        clubbers = self.get_clubbers(user)
        projects = self.get_projects(clubbers)

        project_tasks_categories = self.get_project_tasks_categories(clubbers)
        values = {
            'projects': projects,
            'current_project': project,
            'current_indicator': False,
            'project_tasks_categories': project_tasks_categories,
        }
        return http.request.render(
            'tcd_website.project_general_info_template', values)

    @http.route(
        '/stor_it/projects/<model("project.project"):project>/club_members',
        type='http', auth="user", website=True, multilang=True)
    def club_members(self, project):
        user = request.env.user
        clubbers = self.get_clubbers(user)
        projects = self.get_projects(clubbers)

        project_tasks_categories = self.get_project_tasks_categories(clubbers)
        values = {
            'projects': projects,
            'current_project': project,
            'project_tasks_categories': project_tasks_categories,
            'club_members_menu': True
        }
        return http.request.render(
            'tcd_website.project_club_members_template', values)

    @http.route(
        '/stor_it/projects/<model("project.project"):project>/indicators',
        type='http', auth="user", website=True, multilang=True)
    def indicators(self, project):
        user = request.env.user
        clubbers = self.get_clubbers(user)
        indicators = self.get_indicators(project)
        projects = self.get_projects(clubbers)

        project_tasks_categories = self.get_project_tasks_categories(clubbers)
        values = {
            'projects': projects,
            'current_project': project,
            'project_tasks_categories': project_tasks_categories,
            'indicators': indicators,
            'indicators_menu': True,
            'user': user,
        }
        return http.request.render(
            'tcd_website.project_indicators_template', values)

    @http.route(
        '/stor_it/projects/<model("project.project"):project>/indicators/<model("tcd.indicator"):indicator>',
        type='http', auth="user", website=True, multilang=True)
    def indicator_details(self, project, indicator):
        user = request.env.user
        clubbers = self.get_clubbers(user)
        indicators = self.get_indicator_details(indicator)
        projects = self.get_projects(clubbers)
        indicator_labels = self.get_indicator_labels()

        project_tasks_categories = self.get_project_tasks_categories(clubbers)
        values = {
            'projects': projects,
            'current_project': project,
            'current_indicator': indicator,
            'indicator_labels': indicator_labels,
            'project_tasks_categories': project_tasks_categories,
            'indicators_menu': True,
            'indicators': indicators,
            'user': user,
        }
        return http.request.render(
            'tcd_website.project_indicator_details_template', values)

    @http.route(
        '/stor_it/projects/<model("project.project"):project>/'
        '<model("project.task.category"):task_category>',
        type='http', auth="user", website=True, multilang=True)
    def task_category(self, project, task_category):
        user = request.env.user
        clubbers = self.get_clubbers(user)
        projects = self.get_projects(clubbers)


        project_tasks_categories = self.get_project_tasks_categories(clubbers)
        tasks = self.get_project_category_tasks(project, task_category)

        current_clubber = clubbers.filtered(lambda c: c.project_id == project)

        # Investors can only see task categories with 'Investor' role and
        # Board members can see task categories with 'Board Member' and
        # 'Investor' role
        if current_clubber.role == 'investor' and \
                task_category.role != 'investor':
            return request.render("website.403")
        elif current_clubber.role == 'board' and \
                task_category.role not in ['board', 'investor']:
            return request.render("website.403")

        values = {
            'projects': projects,
            'current_project': project,
            'current_indicator': project.indicator_ids[0],
            'current_category':  task_category,
            'project_tasks_categories': project_tasks_categories,
            'tasks': tasks,
        }

        return http.request.render(
            'tcd_website.project_task_category_template', values)

    @http.route(
        '/page/catalog-form/<model("product.template"):product>/',
        type='http', auth="public", website=True, multilang=True)
    def catalog_form(self, product):
        _logger.info("Current product: " + str(product.id))
        values = {
            'product': product,
        }

        return http.request.render(
            'tcd_website.catalog-form', values)
