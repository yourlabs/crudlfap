import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
    'Group : create group : without Permission': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            // after login go to group create page direct
            .url(CONSTANTS.GROUP.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // name input
            .assert.visible('input[id=id_name]')
            .setValue('input[id=id_name]', CONSTANTS.GROUP.INPUT)

            // submit button
            .assert.visible('#form-object-group .modal-footer button[type=submit]')
            .click('#form-object-group .modal-footer button[type=submit]')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            // check toast-container
            // .waitForElementVisible('#toast-container', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // .assert.visible('#toast-container > div')
            // .assert.containsText('#toast-container > div', 'Create: ' + CONSTANTS.GROUP.INPUT + ' ')

            // verify it created or not
            .url(CONSTANTS.GROUP.CREATE)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            // .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td.name a', CONSTANTS.GROUP.INPUT)
            
            .end();
    }
};
