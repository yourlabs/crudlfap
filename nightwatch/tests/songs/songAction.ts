import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

let artistName;
module.exports = {
    'Song : create song': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        // create song for that.
        artistName = await CommonFunction.createdSampleData('artist', browser);
        const songName = Math.random() + CONSTANTS.SONGS.INPUT + Math.random();
        const songDuration = CONSTANTS.SONGS.INPUT_DURATION;

        browser
            // after login go to song create page direct
            .url(CONSTANTS.SONGS.CREATE)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .assert.containsText('#modal-title-ajax', 'Song: create', "Testing if heading is Song: create")

            // artist selection
            .assert.visible('#id_artist_container > div > input')
            .click('#id_artist_container > div > input', () => {
                browser
                    .expect.element('#id_artist_container > div > ul').to.have.css('display').which.equal('block')
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            // click on option
            .click('#id_artist_container > div > ul > li:nth-child(2)')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            // name input
            .assert.visible('input[id=id_name]')
            .click('input[id=id_name]')
            .setValue('input[id=id_name]', songName)

            // duration input 
            .assert.visible('input[id=id_duration]')

            // owner selection
            .assert.visible('#id_owner_container > div > input')
            .click('#id_owner_container > div > input', () => {
                browser
                    .expect.element('#id_owner_container > div > ul').to.have.css('display').which.equal('block')
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            // click on option
            .click('#id_owner_container > div > ul > li:nth-child(2)')
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            // submit button
            .assert.visible('#form-object-song > div.modal-footer > button[type=submit]')
            .click('#form-object-song > div.modal-footer > button[type=submit]')

            // verify it created or not
            .url(CONSTANTS.SONGS.BASE_URL + "?q=" + songName)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .assert.containsText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) a', songName, "Testing if songs list contains new added songs")

            .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1)', async (tdContentId) => {
                browser
                    .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) a', async (tdContentName) => {
                        await CommonFunction.deleteBySongId(browser, tdContentId.value, tdContentName.value);
                    })
            })

            .end();
    },

    'Song : create song by popup': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        const songName = Math.random() + CONSTANTS.SONGS.INPUT2 + Math.random();

        browser
            // after login go to song create page direct
            .url(CONSTANTS.SONGS.BASE_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

            .assert.visible('body > div.fixed-actions > a[href="/song/create"]')
            .click('body > div.fixed-actions > a[href="/song/create"]', () => {
                browser
                    .waitForElementVisible('#modal', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                    .pause(CONSTANTS.PAUSE_TIMEOUT)
                    .expect.element('#modal').to.have.css('display').which.equal('block');
                browser
                    .assert.containsText('#modal #modal-title-ajax', 'Song: create', "Testing if heading is Song: create")
                    // artist selection
                    .assert.visible('#modal #id_artist_container > div > input')
                    .click('#modal #id_artist_container > div > input', () => {
                        browser
                            .expect.element('#modal #id_artist_container > div > ul').to.have.css('display').which.equal('block')
                    })
                    .pause(CONSTANTS.PAUSE_TIMEOUT)
                    // click on option
                    .click('#modal #id_artist_container > div > ul > li:nth-child(2)')
                    .pause(CONSTANTS.PAUSE_TIMEOUT)

                    // name input
                    .assert.visible('input[id=id_name]')
                    .click('input[id=id_name]')
                    .setValue('input[id=id_name]', songName)

                    // duration input 
                    .assert.visible('input[id=id_duration]')

                    // owner selection
                    .assert.visible('#id_owner_container > div > input')
                    .click('#id_owner_container > div > input', () => {
                        browser
                            .expect.element('#id_owner_container > div > ul').to.have.css('display').which.equal('block')
                    })
                    .pause(CONSTANTS.PAUSE_TIMEOUT)
                    // click on option
                    .click('#id_owner_container > div > ul > li:nth-child(2)')
                    .pause(CONSTANTS.PAUSE_TIMEOUT)

                    // submit button
                    .assert.visible('#modal #form-object-song > div.modal-footer > button[type=submit]')
                    .click('#modal #form-object-song > div.modal-footer > button[type=submit]', () => {
                        // verify it created or not
                        browser
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            .url(CONSTANTS.SONGS.BASE_URL + "?q=" + songName)
                            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            .assert.containsText('#render-table > div > div > div > table > tbody > tr > td:nth-child(3) > a', songName, "Testing if song list contains new added song")
                    })
            })
            .end();
    },

    'Song : Detail song': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        browser
            .url(CONSTANTS.SONGS.BASE_URL)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > a', (tdContentName) => {
                const contentName = tdContentName.value;
                browser
                    .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1)', (tdContentID) => {
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
                                    .assert.urlEquals(CONSTANTS.SONGS.BASE_URL + '/' + contentId, 'song Detail url is the correct')
                                    .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                                    // check get data Id is correct 
                                    .assert.visible('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(1) > td')
                                    .assert.containsText('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(1) > td', contentId, 'song Id matched')
                                    .assert.visible('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(3) > td')
                                    .assert.containsText('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(3) > td', contentName, 'song Name matched')
                            })
                    })
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .end();
    },
    'Song : Edit song': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        const songName = Math.random() + CONSTANTS.SONGS.EDIT_INPUT + Math.random();
        const newDuration = '180';
        let contentId;
        browser
            .url(CONSTANTS.SONGS.BASE_URL)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1)', (tdContentID) => {
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
                            // artist selection
                            .assert.visible('#modal #id_artist_container > div > input')
                            .click('#modal #id_artist_container > div > input', () => {
                                browser
                                    .expect.element('#modal #id_artist_container > div > ul').to.have.css('display').which.equal('block')
                            })
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            // click on option
                            .click('#modal #id_artist_container > div > ul > li:nth-child(2)')
                            .pause(CONSTANTS.PAUSE_TIMEOUT)

                            // name input
                            .assert.visible('input[id=id_name]')
                            .click('input[id=id_name]')
                            .clearValue('input[id=id_name]')
                            .setValue('input[id=id_name]', songName)

                            // duration input 
                            .assert.visible('input[id=id_duration]')
                            .clearValue('input[id=id_duration]')
                            .setValue('input[id=id_duration]', newDuration)

                            // owner selection
                            .assert.visible('#id_owner_container > div > input')
                            .click('#id_owner_container > div > input', () => {
                                browser
                                    .expect.element('#id_owner_container > div > ul').to.have.css('display').which.equal('block')
                            })
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            // click on option
                            .click('#id_owner_container > div > ul > li:nth-child(2)')
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            // click on update
                            .click('#form-object-song > div.modal-footer > button[type="submit"]', () => {
                                console.log("update button clicked");
                                browser
                                    .pause(CONSTANTS.PAUSE_TIMEOUT)
                                    // verified update
                                    .url(CONSTANTS.SONGS.BASE_URL + "?q=" + songName)
                                    .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                                    .pause(CONSTANTS.PAUSE_TIMEOUT)
                                    .assert.containsText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) a', songName, "Testing if song list contains updated song")
                            })

                    })
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .end();
    },
    'Song : Delete song': async (browser: NightwatchBrowser) => {
        await CommonFunction.loginByDev(browser);
        let contentId;
        browser
            .url(CONSTANTS.SONGS.BASE_URL)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)

            // get id and delete that one
            .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1)', async (tdContentId) => {
                const songId = tdContentId.value;
                browser
                    .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) a', async (tdContentName) => {
                        await CommonFunction.deleteBySongId(browser, tdContentId.value, tdContentName.value);
                    })
            })
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            // delete artist as well
            .url(CONSTANTS.ARTIST.BASE_URL + "?q=" + artistName)
            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)
            .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1)', async (tdContentID) => {
                contentId = tdContentID.value;
                browser
                    .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) a', async (tdContentName) => {
                        await CommonFunction.deleteByArtistId(browser, contentId, tdContentName.value);
                    })
            })
            .end();
    }
}    
