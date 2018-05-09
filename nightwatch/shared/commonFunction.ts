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

    export function deleteByGrpId(browser, contentId) {
        browser
            .click('a[data-target="row-actions-' + contentId + '"]', () => {
                // open menu
                browser.expect.element('#row-actions-' + contentId).to.have.css('display').which.equal('block')
            })

            // click on edit
            .assert.visible('#row-actions-' + contentId + ' > li:nth-child(1) > a')

            .click('#row-actions-' + contentId + ' > li:nth-child(1) > a', () => {
                // popup opened
                browser
                    .pause(CONSTANTS.PAUSE_TIMEOUT)
                    .expect.element('#modal').to.have.css('display').which.equal('block');
                // click on delete
                browser
                    .click('#main-form > div.modal-footer > button[type="submit"]', () => {
                        browser
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            // verified delete
                            .getText('#render-table > div > div > div > table > tbody > tr > td.id', (tdContentNew) => {
                                browser.assert.notEqual(tdContentNew.value, contentId, 'Group has been deleted');
                            })
                    })
            })
    }

    // export class bar { }
}