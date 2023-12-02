/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, onMounted, useRef, useState } = owl

export class WorkReport extends Component {
     setup(){
        this.state = useState({
            data : {},
            period: 'date',
            chart: null
        })
        this.actionService = useService("action")
        this.orm = useService("orm")
        this.Reportchart = useRef("workreport")
        onWillStart(async () => {
            this.state.data = await this.orm.call("daily.work.report", "get_work_report", ['date']);
        })
        onMounted(async ()=> {
            await this.createchart()
        });
     }

     async onChangePeriod(){
        this.state.chart.destroy()
        const input_data = this.state.period
        this.state.data = await this.orm.call("daily.work.report", "get_work_report", [input_data]);
        this.createchart()
     }

     createchart(){
         this.state.chart = new Chart(
            this.Reportchart.el,
            {
                type: 'bar',
                data: {
                    labels: this.state.data.value,
                    datasets: [
                        {
                        label: 'Employee Daily Work Report',
                        data: this.state.data.count,
                        }
                    ]
                },
                options: {
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        title: {
                            display: true,
                        }
                    }
                }
            }
        )
     }
     canvasClick(evt){
        const res = this.state.chart.getElementsAtEventForMode(
            evt,
            'nearest',
            { intersect: true },
            true
        );
        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        console.log(this.state.chart.data.labels[res[0].index])
        if (res.length === 0) {
            return;
        }
        // check the date valid in regular expression
        if (dateRegex.test(this.state.chart.data.labels[res[0].index]))
        {
            return this.actionService.doAction({
                name: "Date",
                type: "ir.actions.act_window",
                res_model: "daily.work.report",
                domain: [["date", "=", this.state.chart.data.labels[res[0].index]]],
                view_mode: "list, form ",
                views: [[false, "list"], [false, "form"]],
                target: "current",
            });
        }
        else{
            return this.actionService.doAction({
                name: "Employee",
                type: "ir.actions.act_window",
                res_model: "daily.work.report",
                domain: [["employee", "=", this.state.chart.data.labels[res[0].index]]],
                view_mode: "list, form ",
                views: [[false, "list"], [false, "form"]],
                target: "current",
            });
        }
     };
}
WorkReport.template = "WorkReportDashboard"
registry.category("actions").add("work_report_dashboard", WorkReport)
