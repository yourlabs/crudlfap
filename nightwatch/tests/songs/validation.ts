import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
    'Song : create songs validation': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            // after login go to group create page direct
            .url(CONSTANTS.GROUP.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // name input
            .assert.containsText('#id_name_container > label', 'Name')
            .assert.visible('input[id=id_name]')
            // permission input //select-dropdown dropdown-trigger
            .assert.containsText('#id_permissions_container > label', 'Permissions')
            .elements('css selector', 'div#id_permissions_container ul.multiple-select-dropdown', (result) => {
                browser.assert.equal(result.value.length, 1, "Testing if element multiple select box is visible")
            })
            .elements('css selector', 'div#id_permissions_container ul.multiple-select-dropdown li', (result) => {
                browser.assert.notEqual(result.value.length, 0, "Testing if element multiple select box have option is visible") // have 31 option
            })

            // submit button
            .assert.visible('#form-object-group .modal-footer button[type=submit]')
            .click('#form-object-group .modal-footer button[type=submit]')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .assert.visible('#id_name_container > div > small')
            .assert.containsText('#id_name_container > div > small', 'This field is required.')

            .end();
    }
};