# -*- coding: utf-8 -*-
{
    'name': "survey_quiz_timer",
    'summary': """
    Survey timer for quiz""",
    'description': """
        Setting timer for each question in survey, If the mouse and keyboard 
        is in the idle state.
    """,
    'author': "Kailas",
    'category': 'Category',
    'version': '16.0.1.0.0',
    'depends': ['survey'],
    "assets": {
        "web.assets_frontend": [
            "survey_quiz_timer/static/src/js/survey_timer.js"
        ],
    },
    'data': [
        'views/survey_timer_count.xml',
        'views/quiz_idle_timer_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
