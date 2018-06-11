import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
    'Group : create group validation': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            // after login go to group create page direct
            .url(CONSTANTS.GROUP.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // name input
            .assert.containsText('#id_name_container > label', 'Name')
            .assert.visible('input[id=id_name]')
            // submit button
            .assert.visible('#form-object-group .modal-footer button[type=submit]')
            .click('#form-object-group .modal-footer button[type=submit]')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .assert.visible('#id_name_container > div > small')
            .assert.containsText('#id_name_container > div > small', 'This field is required.')

            .end();
    }
};