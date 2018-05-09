import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

const groupNameForDuplicate = Math.random() + CONSTANTS.GROUP.INPUT + Math.random();

module.exports = {
    'Group : create group : without Permission': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        const groupName = groupNameForDuplicate;

        browser
            // after login go to group create page direct
            .url(CONSTANTS.GROUP.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // name input
            .assert.visible('input[id=id_name]')
            .setValue('input[id=id_name]', groupName)

            // submit button
            .assert.visible('#form-object-group .modal-footer button[type=submit]')
            .click('#form-object-group .modal-footer button[type=submit]')

            // verify it created or not
            .url(CONSTANTS.GROUP.LIST + "?q=" + groupName)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td.name a', groupName, "Testing if group list contains new added group")
            .end();
    },

    'Group : Not create same name group': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        const groupName = groupNameForDuplicate;

        browser
            // after login go to group create page direct
            .url(CONSTANTS.GROUP.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // name input
            .assert.visible('input[id=id_name]')
            .setValue('input[id=id_name]', groupName)

            // submit button
            .assert.visible('#form-object-group .modal-footer button[type=submit]')
            .click('#form-object-group .modal-footer button[type=submit]')

            // verify error message
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .assert.containsText('#id_name_container > div > small', 'Group with this Name already exists.')
            .end();
    },

    'Group : create group : with Permission': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        const groupName = Math.random() + CONSTANTS.GROUP.INPUT2 + Math.random();

        browser
            // after login go to group create page direct
            .url(CONSTANTS.GROUP.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            // name input
            .assert.visible('input[id=id_name]')
            .setValue('input[id=id_name]', groupName)

            // permission input
            .assert.visible('#id_permissions_container > div > input')
            .click('#id_permissions_container > div > input', () => {
                browser
                    .expect.element('#id_permissions_container > div > ul').to.have.css('display').which.equal('block')
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            // click on option
            .click('#id_permissions_container > div > ul > li:nth-child(4)')
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .click('#id_permissions_container > div > ul > li:nth-child(6)')
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .click('body')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            // submit button
            .assert.visible('#form-object-group .modal-footer button[type=submit]')
            .click('#form-object-group .modal-footer button[type=submit]')

            // verify it created or not
            .url(CONSTANTS.GROUP.LIST + "?q=" + groupName)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td.name a', groupName, "Testing if group list contains new added group")
            .end();
    },

    'Group : Detail group': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            .url(CONSTANTS.GROUP.LIST)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td.name > a', (tdContentName) => {
                const contentName = tdContentName.value;
                browser
                    .getText('#render-table > div > div > div > table > tbody > tr > td.id', (tdContentID) => {
                        const contentId = tdContentID.value;
                        browser
                            .click('a[data-target="row-actions-' + contentId + '"]', () => {
                                // open menu
                                browser.expect.element('#row-actions-' + contentId).to.have.css('display').which.equal('block')
                            })

                            // click on edit
                            .assert.visible('#row-actions-' + contentId + ' > li:nth-child(3) > a')
                            .click('#row-actions-' + contentId + ' > li:nth-child(3) > a', () => {
                                browser
                                    .assert.urlEquals(CONSTANTS.GROUP.BASE_URL + '/' + contentId, 'Group Detail url is the correct')
                                    .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                                    // check get data Id is correct 
                                    .assert.visible('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(1) > td')
                                    .assert.containsText('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(1) > td', contentId, 'Group Id matched')
                                    .assert.visible('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(2) > td')
                                    .assert.containsText('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(2) > td', contentName, 'Group Name matched')
                            })
                    })
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .end();
    },

    'Group : Edit group': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        const groupName = Math.random() + CONSTANTS.GROUP.EDIT_INPUT + Math.random();
        let contentId;
        browser
            .url(CONSTANTS.GROUP.LIST)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .getText('#render-table > div > div > div > table > tbody > tr > td.id', (tdContentID) => {
                contentId = tdContentID.value;
                browser
                    .click('a[data-target="row-actions-' + contentId + '"]', () => {
                        // open menu
                        browser.expect.element('#row-actions-' + contentId).to.have.css('display').which.equal('block')
                    })

                    // click on edit
                    .assert.visible('#row-actions-' + contentId + ' > li:nth-child(2) > a')

                    .click('#row-actions-' + contentId + ' > li:nth-child(2) > a', () => {
                        // popup opened
                        browser
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            // name input
                            .assert.visible('input[id=id_name]')
                            .clearValue('input[id=id_name]')
                            .setValue('input[id=id_name]', groupName)
                            // permission input
                            .assert.visible('#id_permissions_container > div > input')
                            .click('#id_permissions_container > div > input', () => {
                                browser
                                    .expect.element('#id_permissions_container > div > ul').to.have.css('display').which.equal('block');
                                browser
                                    .pause(CONSTANTS.PAUSE_TIMEOUT)
                                    // click on option
                                    .click('#id_permissions_container > div > ul > li:nth-child(5)')
                                    .click('#id_permissions_container > div > ul > li:nth-child(9)')
                                    .element('css selector', '#id_permissions_container > div > ul > li.selected', (result) => {
                                        if (result.value.ELEMENT) {
                                            browser.click('#id_permissions_container > div > ul > li.selected')
                                        }
                                    })
                                    .click('input[id=id_name]')
                                    // click on update
                                    .click('#form-object-group > div.modal-footer > button[type="submit"]', () => {
                                        console.log("update button clicked");
                                        browser
                                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                                            // verified update
                                            .getText('#render-table > div > div > div > table > tbody > tr > td.name > a', (tdContentName) => {
                                                browser.assert.equal(tdContentName.value, groupName, 'Group name has been updated');
                                            })
                                    })
                            })
                    })
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .end();
    },

    'Group : Delete group': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        let contentId;
        browser
            .url(CONSTANTS.GROUP.LIST)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .getText('#render-table > div > div > div > table > tbody > tr > td.id', async (tdContentID) => {
                contentId = tdContentID.value;
                await CommonFunction.deleteByGrpId(browser, contentId);
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .end();
    }
};
