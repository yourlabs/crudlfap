import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
    'Post : create post validation': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            // after login go to post create page direct
            .url(CONSTANTS.POST.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // name input
            .assert.containsText('#id_name_container > label', 'Title')
            .assert.visible('input[id=id_name]')
            // publish input
            .assert.containsText('#id_publish_container > label', 'Publish')
            .assert.visible('input[id=id_publish]')
            .clearValue('input[id=id_publish]')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            // owner selection
            .assert.containsText('#id_owner_container > label', 'Owner')
            .assert.visible('#id_owner_container > div.select-wrapper > input')

            // submit button
            .assert.visible('#form-object-post .modal-footer button[type=submit]')
            .click('#form-object-post .modal-footer button[type=submit]')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .assert.visible('#id_name_container > div > small')
            .assert.containsText('#id_name_container > div > small', 'This field is required.')

            .assert.visible('#id_publish_container > div > small')
            .assert.containsText('#id_publish_container > div > small', 'This field is required.')

            .assert.visible('#id_owner_container > div > small')
            .assert.containsText('#id_owner_container > div > small', 'This field is required.')

            .end();
    }
};