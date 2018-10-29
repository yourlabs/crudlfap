import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
    'Artist : create artist validation': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            // after login go to song create page direct
            .url(CONSTANTS.ARTIST.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            // name input
            .assert.containsText('#id_name_container > label', 'Name')
            .assert.visible('input[id=id_name]')

            .assert.visible('#form-object-artist > div.modal-footer > button[type=submit]')
            .click('#form-object-artist > div.modal-footer > button[type=submit]')

            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .assert.visible('#id_name_container > div > small')
            .assert.containsText('#id_name_container > div > small', 'This field is required.')

            .end();
    }
};