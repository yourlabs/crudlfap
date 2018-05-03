import { NightwatchBrowser } from 'nightwatch';
import {CONSTANTS} from './../shared/CONSTANTS';
module.exports = {
    before: (browser) => {
        browser
            .url(CONSTANTS.BASE_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
    },
    'Before Login: Menu should visible when click on the menu icon': (browser: NightwatchBrowser) => {
        browser
            .assert.visible('span[data-action="click->sidenav#click"]')
            .isVisible('ul[id="slide-out"]', (result) => {
                browser.assert.equal(result.value, false)
            })
            .click('span[data-action="click->sidenav#click"]')
            .waitForElementVisible('ul[id="slide-out"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .isVisible('ul[id="slide-out"]', (result) => {
                browser.assert.equal(result.value, true)
            })
            .click('ul#slide-out li.no-padding a[href="/"]')
    },

    'Before Login: Menu should contains "login" option': (browser: NightwatchBrowser) => {
        browser
            .waitForElementVisible('span[data-action="click->sidenav#click"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
        
            .assert.visible('span[data-action="click->sidenav#click"]')
            .click('span[data-action="click->sidenav#click"]')
            .waitForElementVisible('ul#slide-out li.no-padding a[href="/login"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .elements('css selector', 'ul#slide-out li.no-padding a[href="/login"]', (result) => {
                browser.assert.equal(result.value.length, 1)
            });
    },

    'After Login: Menu should contains the "logout" option': (browser: NightwatchBrowser) => {
        browser
            .assert.visible('ul#slide-out li.no-padding a[href="/login"]')
            .click('ul#slide-out li.no-padding a[href="/login"]')
            .waitForElementVisible('input[id=id_username]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .assert.visible('input[id=id_username]')
            .setValue('input[id=id_username]', CONSTANTS.USER_CREDENTIALS.RIGHT.USERNAME)
            .assert.visible('input[id=id_password]')
            .setValue('input[id=id_password]', CONSTANTS.USER_CREDENTIALS.RIGHT.PASSWORD)

            .assert.visible('button[type=submit]')
            .click('button[type=submit]')
            .waitForElementVisible('ul[class="right"] li a[href="/logout"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

        browser
            .assert.visible('span[data-action="click->sidenav#click"]')
            .click('span[data-action="click->sidenav#click"]')
            .waitForElementVisible('ul[id="slide-out"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .assert.visible('ul[id="slide-out"]')

            .elements('css selector', 'ul#slide-out li.no-padding a[href="/logout"]', (result) => {
                browser.assert.equal(result.value.length, 1)
            })
            .click('ul#slide-out li.no-padding a[href="/logout"]')
            .waitForElementVisible('ul[class="right"] li a[href="/login"]', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
    },
    'After Logout: Menu should contains "login" option': (browser: NightwatchBrowser) => {
        browser
            .assert.visible('span[data-action="click->sidenav#click"]')
            .isVisible('ul[id="slide-out"]', (result) => {
                browser.assert.equal(result.value, false)
            })
            .click('span[data-action="click->sidenav#click"]')
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