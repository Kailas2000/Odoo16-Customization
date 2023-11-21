/** @odoo-module **/
import { registry } from "@web/core/registry"
const { Component, useState } = owl

class Increment extends Component{
    setup(){
        this.state = useState({
            value: 0
        })
    }
    onValueChange(val){
        this.state.value += val
    }
}

Increment.template = 'Increment';
const Systray = {
    Component: Increment,
//    isDisplayed: (env) => true    "default true"
}
registry.category("systray").add("increment", Systray)