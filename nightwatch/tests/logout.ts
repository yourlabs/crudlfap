import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../shared/CONSTANTS';

module.exports = {
    before: function (browser) {
        // console.log("Before working!");
        // login user with correct crednetials
        browser
            .url(CONSTANTS.LOGIN_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .assert.visible('input[id=id_username]')
            .setValue('input[id=id_username]', CONSTANTS.USER_CREDENTIALS.RIGHT.USERNAME)

            .assert.visible('input[id=id_password]')
            .setValue('input[id=id_password]', CONSTANTS.USER_CREDENTIALS.RIGHT.PASSWORD)

            .assert.visible('button[type=submit]')
            .click('button[type=submit]')

            .waitForElementVisible('ul[class="right"] li a[href="/logout"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
    },
    'Logout': (browser: NightwatchBrowser) => {
        browser
            // after login
            .click('a[href="/logout"]')

            // on logout page
            .waitForElementVisible('ul[class="right"] li a[href="/login"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .assert.urlEquals(CONSTANTS.LOGOUT_URL, 'Logout url is the correct')

            .end();
    }

};