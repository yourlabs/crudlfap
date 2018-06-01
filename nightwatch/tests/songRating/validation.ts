import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
    'SongRating : create song-rating validation': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            // after login go to song-rating create page direct
            .url(CONSTANTS.SONGRATING.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // song selection
            .assert.containsText('#id_song_container > label', 'Song')
            // DUE TO IE
            // .assert.visible('#id_song_container > div.select-wrapper > input')

            // name input
            .assert.containsText('#id_rating_container > label', 'Rating')
            .assert.visible('input[id=id_rating]')

            // submit button
            .assert.visible('#form-object-songrating > div.modal-footer > button[type=submit]')
            .click('#form-object-songrating > div.modal-footer > button[type=submit]')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .assert.visible('#id_song_container > div > small')
            .assert.containsText('#id_song_container > div > small', 'This field is required.')

            .assert.visible('#id_rating_container > div > small')
            .assert.containsText('#id_rating_container > div > small', 'This field is required.')

            .end();
    }
};