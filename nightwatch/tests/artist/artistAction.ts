import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
    'Artist : create artist': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        const artistName = Math.random() + CONSTANTS.ARTIST.INPUT + Math.random();;

        browser
            // after login go to artist create page direct
            .url(CONSTANTS.ARTIST.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .assert.containsText('#modal-title-ajax', 'Artist: create', "Testing if heading is Artist: create")
            // name input
            .assert.visible('input[id=id_name]')
            .setValue('input[id=id_name]', artistName)

            // submit button
            .assert.visible('#form-object-artist > div.modal-footer > button[type=submit]')
            .click('#form-object-artist > div.modal-footer > button[type=submit]')

            // verify it created or not
            .url(CONSTANTS.ARTIST.BASE_URL + "?q=" + artistName)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td.name a', artistName, "Testing if artist list contains new added artist")


            .url(CONSTANTS.ARTIST.BASE_URL + "?q=" + artistName)
            // get id and delete that one
            .getText('#render-table > div > div > div > table > tbody > tr > td.id', async (tdContentId) => {
                const groupId = tdContentId.value;
                browser
                    .getText('#render-table > div > div > div > table > tbody > tr > td.name', async (tdContentName) => {
                        await CommonFunction.deleteByArtistId(browser, tdContentId.value);
                    })
            })
            .end();
    },

    'Artist : create artist by popup': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        const artistName = Math.random() + CONSTANTS.ARTIST.INPUT2 + Math.random();

        browser
            // after login go to artist create page direct
            .url(CONSTANTS.ARTIST.BASE_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .assert.visible('body > div.fixed-actions > a[href="/artist/create"]')
            .click('body > div.fixed-actions > a[href="/artist/create"]', () => {
                browser
                    .waitForElementVisible('#modal', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                    .pause(CONSTANTS.PAUSE_TIMEOUT)
                    .expect.element('#modal').to.have.css('display').which.equal('block');
                browser
                    .assert.containsText('#modal #modal-title-ajax', 'Artist: create', "Testing if heading is Artist: create")
                    // name input
                    .assert.visible('input[id=id_name]')
                    .setValue('input[id=id_name]', artistName)

                    .pause(CONSTANTS.PAUSE_TIMEOUT)

                    // submit button
                    .assert.visible('#modal #form-object-artist > div.modal-footer > button[type=submit]')
                    .click('#modal #form-object-artist > div.modal-footer > button[type=submit]', () => {
                        // verify it created or not
                        browser
                            .url(CONSTANTS.ARTIST.BASE_URL + "?q=" + artistName)
                            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td.name a', artistName, "Testing if artist list contains new added artist")
                    })
            })
            .end();
    },

    'Artist : Detail Artist': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            .url(CONSTANTS.ARTIST.BASE_URL)
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
                                    .assert.urlEquals(CONSTANTS.ARTIST.BASE_URL + '/' + contentId, 'Artist Detail url is the correct')
                                    .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                                    // check get data Id is correct 
                                    .assert.visible('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(1) > td')
                                    .assert.containsText('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(1) > td', contentId, 'Artist Id matched')
                                    .assert.visible('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(2) > td')
                                    .assert.containsText('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(2) > td', contentName, 'Artist Name matched')
                            })
                    })
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .end();
    },

    'Artist : Edit artist': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        const artistName = Math.random() + CONSTANTS.ARTIST.EDIT_INPUT + Math.random();
        let contentId;
        browser
            .url(CONSTANTS.ARTIST.BASE_URL)
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
                            .setValue('input[id=id_name]', artistName)

                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            // click on update
                            .click('#form-object-artist > div.modal-footer > button[type="submit"]', () => {
                                console.log("update button clicked");
                                browser
                                    .pause(CONSTANTS.PAUSE_TIMEOUT)
                                    // verified update
                                    .getText('#render-table > div > div > div > table > tbody > tr > td.name > a', (tdContentName) => {
                                        browser.assert.equal(tdContentName.value, artistName, 'Artist name has been updated');
                                    })
                            })
                    })
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .end();
    },

    'Artist : Delete artist': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        let contentId;
        browser
            .url(CONSTANTS.ARTIST.BASE_URL)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .getText('#render-table > div > div > div > table > tbody > tr > td.id', async (tdContentID) => {
                contentId = tdContentID.value;
                await CommonFunction.deleteByArtistId(browser, contentId);
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .end();
    }

}