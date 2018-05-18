import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
    'Song : create song validation': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            // after login go to song create page direct
            .url(CONSTANTS.SONGS.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // artist selection
            .assert.containsText('#id_artist_container > label', 'Artist')
            .assert.visible('#id_artist_container > div.select-wrapper > input')

            // name input
            .assert.containsText('#id_name_container > label', 'Title')
            .assert.visible('input[id=id_name]')

            // duration input
            .assert.containsText('#id_duration_container > label', 'Duration')
            .assert.visible('input[id=id_duration]')
            .clearValue('input[id=id_duration]')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            // owner selection
            .assert.containsText('#id_owner_container > label', 'Owner')
            .assert.visible('#id_owner_container > div.select-wrapper > input')

            // submit button
            .assert.visible('#form-object-song > div.modal-footer > button[type=submit]')
            .click('#form-object-song > div.modal-footer > button[type=submit]')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .assert.visible('#id_artist_container > div > small')
            .assert.containsText('#id_artist_container > div > small', 'This field is required.')

            .assert.visible('#id_name_container > div > small')
            .assert.containsText('#id_name_container > div > small', 'This field is required.')

            .assert.visible('#id_duration_container > div > small')
            .assert.containsText('#id_duration_container > div > small', 'This field is required.')

            .assert.visible('#id_owner_container > div > small')
            .assert.containsText('#id_owner_container > div > small', 'This field is required.')

            .end();
    }
};