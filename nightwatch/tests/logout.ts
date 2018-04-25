import { NightwatchBrowser } from 'nightwatch';

module.exports = {
    before: function (browser) {
        // console.log("Before working!");
        // login user with correct crednetials
        browser
            .url('http://localhost:8000')
            .waitForElementVisible('body', 1000)

            .assert.visible('input[id=id_username]')
            .setValue('input[id=id_username]', 'dev')

            .assert.visible('input[id=id_password]')
            .setValue('input[id=id_password]', 'dev')

            .assert.visible('button[type=submit]')
            .click('button[type=submit]')

            .waitForElementVisible('ul[class="right"] li a[href="/logout"]', 1000)
    },
    'Logout': (browser: NightwatchBrowser) => {
        browser
            // after login
            .click('a[href="/logout"]')

            // on logout page
            .waitForElementVisible('ul[class="right"] li a[href="/login"]', 1000)

            .assert.visible('div[id="modal-body-ajax"] h2')
            .assert.containsText('div[id="modal-body-ajax"] h2', 'You have been logged-out !')

            .assert.visible('div[id="modal-body-ajax"] p')
            .assert.containsText('div[id="modal-body-ajax"] p', 'Thanks for the time you spent with us today')

            .end();
    }

};