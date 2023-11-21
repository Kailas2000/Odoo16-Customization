/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
class SystrayIcon extends Component {
    setup() {
        super.setup(...arguments);
    }
    //  Function for generating the QR code based on the user input
    _onClick_generate() {
        var input_data = $('#data').val()
        if (input_data.trim() != '') {
            $('#qrcode').empty();
            $('#qrcode').css("display","block")
            $('#download').css("display","block")
            var qrcode = new QRCode(self.$('#qrcode')[0], {
                text: input_data,
                width: 128,
                height: 128,
            });
        }
    }
    //  Function for reset the value in the user input field
    _onClick_reset() {
        $('#data').val('')
        $('#qrcode').empty();
        $('#download').css("display","none")
    }
    //  Function for downloading the QR code generated as png
    _onClick_download() {
        var img_src = $('#qrcode')[0].childNodes[1].src;
        var image = $('<a>')
            .attr('href', img_src)
            .attr('download', 'qrcode.png');
        image[0].click();
        $('#data').val('')
        $('#qrcode').empty();
         $('#download').css("display","none")
    }
}
SystrayIcon.template = "qr_icon";
export const systrayItem = { Component: SystrayIcon,};
registry.category("systray").add("SystrayIcon", systrayItem);
