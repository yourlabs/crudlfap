import { CONSTANTS } from './CONSTANTS';

export module CommonFunction {
    export function loginByDev(browser) {
        browser
            .url(CONSTANTS.BASE_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .assert.visible('input[id=id_username]')
            .setValue('input[id=id_username]', CONSTANTS.USER_CREDENTIALS.RIGHT.USERNAME)

            .assert.visible('input[id=id_password]')
            .setValue('input[id=id_password]', CONSTANTS.USER_CREDENTIALS.RIGHT.PASSWORD)

            .assert.visible('button[type=submit]')
            .click('button[type=submit]')

            // after login
            .waitForElementVisible('.container .orange-text', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // .assert.title('Home - CRUDLFA+')
            .assert.visible('a[class=waves-effect]')

        return true;
    }

    export function login() {

    }

    // export class bar { }
}