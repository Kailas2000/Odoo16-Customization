from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.addons.survey.controllers.main import Survey


class SurveyContact(Survey):
    """Inherit survey submit route"""
    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>',
                type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        """Checking the state of survey is it done
            or on-processing. This function will work only when the state becomes done."""
        res = super(SurveyContact, self).survey_submit(survey_token=survey_token,
                                                       answer_token=answer_token,
                                                       **post)
        access_data = self._get_access_data(survey_token, answer_token,
                                            ensure_token=True)
        answer_sudo = access_data['answer_sudo']

        partner_details = {}
        if answer_sudo.state == 'done':
            user_input = request.env['survey.user_input'].search([], limit=1)
            # looping the user_input_line and accessing single line
            for line in user_input.user_input_line_ids:
                content = request.env['survey.contact'].search([
                    ('question_id', '=', line.question_id.id)
                ])
                if content:
                    field_id = content.contact_fields_id
                    field_name = request.env['ir.model.fields'].search([
                        ('id', '=', field_id.id)
                    ]).name
                    # It works when it have the country name
                    if field_name == 'country_id':
                        country_name = line.display_name.lower()
                        country_code = request.env['res.country'].search([
                            ('name'.lower(), 'ilike', country_name)
                        ]).id
                        line.display_name = country_code
                        if not country_code:
                            raise ValidationError("Please provide an existing country name!"
                                                  "Refresh the page")
                    # storing the partner details in the dict partner_details based on the contact relation
                    partner_details[field_name] = line.display_name
            # Creating the partner
            request.env['res.partner'].sudo().create(partner_details)
        return res

