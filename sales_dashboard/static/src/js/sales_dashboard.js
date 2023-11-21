/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, useRef, onMounted, useState } = owl

export class SalesDashboard extends Component {
     setup(){
        this.state = useState({
            data : {},
            period:30,
            chart:[]
        })
        this.actionService = useService("action")
        this.orm = useService("orm")

        this.Teamchart = useRef("teamchart")
        this.Personchart = useRef("personchart")
        this.Customerchart = useRef("customerchart")
        this.Lowestchart = useRef("lowestchart")
        this.Highestchart = useRef("highestchart")
        this.Orderchart = useRef("orderchart")
        this.Invoicechart = useRef("invoicechart")

        onMounted(async ()=> {
            await this.onChangePeriod()
        });
    }

    async onChangePeriod(){
        const date_limit = this.state.period
        this.state.data = await this.orm.call("sales.dashboard", "get_sale_details", [date_limit]);

        this.charts(this.Teamchart.el, 'bar','Sales Team', this.state.data.teams, this.state.data.team_value)
        this.charts(this.Personchart.el, 'line','Sales Person', this.state.data.persons, this.state.data.persons_values)
        this.charts(this.Customerchart.el, 'bar', 'Top 10 Customers', this.state.data.customer_names, this.state.data.customer_values)
        this.charts(this.Lowestchart.el, 'doughnut', 'Lowest Selling Products', this.state.data.low_products_name, this.state.data.low_products_count)
        this.charts(this.Highestchart.el, 'pie', 'Highest Selling Products', this.state.data.top_products_name, this.state.data.top_products_count)
        this.charts(this.Orderchart.el, 'polarArea', 'Order State', this.state.data.state, this.state.data.state_count)
        this.charts(this.Invoicechart.el, 'polarArea', 'Invoice State', this.state.data.invoice_state, this.state.data.invoice_value)
    }

    async onChangePeriod_click(){
        if (this.state.chart.length != 0) {
            this.state.chart.forEach((item)=> {
                item.destroy()
            });
        }
        this.onChangePeriod()
    }

    async onClickQuotations(){
        return this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "sale.order",
            domain: [["id", "in", this.state.data.quotations]],
            view_mode: "list, form ",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }
    async onClickOrders(){
        return this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "sale.order",
            domain: [["id", "in", this.state.data.orders]],
            view_mode: "list, form ",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }
    charts(canvas,type,label,labels,data){
        this.state.chart.push(new Chart(
            canvas,
            {
                type,
                data: {
                    labels,
                    datasets: [
                        {
                        label,
                        data,
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
        ))
    }
}
SalesDashboard.template = "SalesDashboard"
registry.category("actions").add("sale_dash", SalesDashboard)

