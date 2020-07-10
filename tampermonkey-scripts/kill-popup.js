// ==UserScript==
// @name         kill-popup
// @namespace    https://github.com/refraction-ray
// @version      0.1
// @description  close xueqiu popups
// @author       refraction-ray
// @match        https://xueqiu.com/
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function fkoff() {
        var close = $("#app > div.modals.dimmer.js-shown > div:nth-child(2) > div.modal.modal__confirm.modal--sm > a > i")
        if (close.length > 0) {
            close[0].click();
            console.log("already close")
        } else { console.log("nothing to close") }
    };

    window.setTimeout(function() {
        fkoff();
    }, 1000)

    $(document).on('click', function() {
        window.setTimeout(function() {
            console.log("close in 100ms");
            fkoff();
        }, 100);
    });
    $(document).on('click', function() {
        window.setTimeout(function() {
            console.log("backup close in 300ms");
            fkoff();
        }, 300);
    });
})();