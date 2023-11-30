/** @odoo-module **/
import { registry } from "@web/core/registry"
import { FloatField } from "@web/views/fields/float/float_field";
const { useRef, useState } = owl

export class FloatToInt extends FloatField{
    setup(){
        this.datas = useRef("floatint")
        this.record = useState(this.props.record.data);
        this.values = this.record.expected_price;
    }
    UpdateFloat(e){
        let input_data = this.datas.el.value
        let int_value = Math.round(input_data);
        this.props.update(int_value)
    }
}
FloatToInt.template = "Float_To_Int";
registry.category("fields").add("float_int", FloatToInt)