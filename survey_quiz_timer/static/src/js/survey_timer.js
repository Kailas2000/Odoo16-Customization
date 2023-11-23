odoo.define('survey_quiz_timer.survey_timer', function (require) {
"use strict";

var SurveyForm = require("survey.form");
var publicWidget = require('web.public.widget');

publicWidget.registry.SurveyForm = publicWidget.Widget.extend({
    selector: '.o_survey_form',

        start:function(){
            var self = this;
            self.datas = self.$el.find('#question_timer')
            self.question_time_value = self.datas.data('limited')
            if (self.question_time_value == 'True') {
                self.timer = self.datas.data('timer')
                let time = self.timer
                let  default_time = 5

                const timer_start = setInterval(start_timer, 1000);
                onkeydown = restart_time;
                onmousemove = restart_time;
                onclick = restart_time;

                /*  Function to start the timer, After the default_time
                    completes the timer starts counting */
                function start_timer() {
                    default_time --;
                    if (default_time <= 0 && time > 0){
                        time --;
                        $('#question_timer').text(time)
                        let element = $('.o_survey_review')
                        if(element['length']){
                            $('#question_timer').text('')
                        }
                        if (time == 0){
                            $('.btn-primary').click();
                        }
                    }
                }
                /*  Function to restart the timer,If the mouse or keyboard have
                    occured any actions then restart the timer and also setting
                    the default_time */
                function restart_time() {
                    default_time = 5
                    time = self.timer
                    $('#question_timer').text('')
                }
            }
        }
    })
})
