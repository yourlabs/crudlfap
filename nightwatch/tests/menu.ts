import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from './../shared/CONSTANTS';
module.exports = {
    'Before Login: Menu should visible when click on the menu icon': (browser: NightwatchBrowser) => {
        browser
            .url(CONSTANTS.LOGIN_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .assert.visible('span[class="sidenav-trigger"]')
            .element('id', 'slide-out', function (result) {
                browser.assert.equal(result.status, false)
            })
            .click('span[class="sidenav-trigger"]')
            .waitForElementVisible('ul[id="slide-out"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .isVisible('ul[id="slide-out"]', (result) => {
                browser.assert.equal(result.value, true)
            })
            .click('ul#slide-out li.no-padding a[href="/"]')
            .end();
    },

    'Before Login: Menu should contains "login" option': (browser: NightwatchBrowser) => {
        browser
            .url(CONSTANTS.LOGIN_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .waitForElementVisible('span[class="sidenav-trigger"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .assert.visible('span[class="sidenav-trigger"]')
            .click('span[class="sidenav-trigger"]')
            .waitForElementVisible('ul#slide-out li.no-padding a[href="/login"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .elements('css selector', 'ul#slide-out li.no-padding a[href="/login"]', (result) => {
                browser.assert.equal(result.value.length, 1)
            })
            .end();
    },

    'After Login: Menu should contains the "logout" option': (browser: NightwatchBrowser) => {
        browser
            .url(CONSTANTS.LOGIN_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .elements('css selector', 'ul#slide-out li.no-padding a[href="/login"]', (result) => {
                browser.assert.equal(result.value.length, 1)
            })

            .click('ul#slide-out li.no-padding a[href="/login"]')

            .waitForElementVisible('input[id=id_username]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .assert.visible('input[id=id_username]')
            .setValue('input[id=id_username]', CONSTANTS.USER_CREDENTIALS.RIGHT.USERNAME)
            .assert.visible('input[id=id_password]')
            .setValue('input[id=id_password]', CONSTANTS.USER_CREDENTIALS.RIGHT.PASSWORD)

            .assert.visible('button[type=submit]')
            .click('button[type=submit]')
            .waitForElementVisible('ul[class="right"] li a[href="/logout"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .assert.visible('span[class="sidenav-trigger"]')
            .click('span[class="sidenav-trigger"]')
            .waitForElementVisible('ul[id="slide-out"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .assert.visible('ul[id="slide-out"]')

            .elements('css selector', '#slide-out > li:nth-child(4) > a[href="/logout"]', (result) => {
                browser.assert.equal(result.value.length, 1)
            })
            .end();
    },
    'After Logout: Menu should contains "login" option': (browser: NightwatchBrowser) => {
        browser
            .url(CONSTANTS.BASE_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .assert.visible('span[class="sidenav-trigger"]')
            .element('id', 'slide-out', function (result) {
                browser.assert.equal(result.status, false)
            })
            .click('span[class="sidenav-trigger"]')
            .waitForElementVisible('ul[class="right"] li a[href="/login"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .isVisible('ul[id="slide-out"]', (result) => {
                browser.assert.equal(result.value, true)
            })

            .elements('css selector', 'ul#slide-out li.no-padding a[href="/login"]', (result) => {
                browser.assert.equal(result.value.length, 1)
            })
            .end();
    }
};
