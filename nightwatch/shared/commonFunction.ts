import { CONSTANTS } from './CONSTANTS';

export module CommonFunction {
    export function loginByDev(browser) {
        browser
            .url(CONSTANTS.BASE_URL)
            .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
            .pause(CONSTANTS.PAUSE_TIMEOUT)
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

    export function deleteByGrpId(browser, contentId, contentName) {
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
                            .url(CONSTANTS.GROUP.BASE_URL + "?q=" + contentName)
                            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            .element('css selector', '#render-table > div > div > div > table > tbody > tr', function (result) {
                                if (result.status === -1) {
                                    //Element does not exist, do something else
                                    browser.assert.equal(0, 0, 'Group has been deleted');
                                }
                            });
                    })
            })
    }

    export function deleteByArtistId(browser, contentId, contentName) {
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
                            .url(CONSTANTS.ARTIST.BASE_URL + "?q=" + contentName)
                            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            .element('css selector', '#render-table > div > div > div > table > tbody > tr', function (result) {
                                if (result.status === -1) {
                                    //Element does not exist, do something else
                                    browser.assert.equal(0, 0, 'Artist has been deleted');
                                }
                            });
                    })
            })
    }

    export function deleteBySongId(browser, contentId, contentName) {
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
                            .url(CONSTANTS.SONGS.BASE_URL + "?q=" + contentName)
                            .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                            .pause(CONSTANTS.PAUSE_TIMEOUT)
                            .element('css selector', '#render-table > div > div > div > table > tbody > tr', function (result) {
                                if (result.status === -1) {
                                    //Element does not exist, do something else
                                    browser.assert.equal(0, 0, 'Song has been deleted');
                                }
                            });
                    })
                    .pause(CONSTANTS.PAUSE_TIMEOUT)
            })
    }

    export function createdSampleData(modal, browser) {
        let sampleName;
        switch (modal) {
            case 'artist':
                sampleName = Math.random() + CONSTANTS.ARTIST.INPUT + Math.random();

                browser
                    // after login go to artist create page direct
                    .url(CONSTANTS.ARTIST.CREATE)
                    .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                    .assert.containsText('#modal-title-ajax', 'Artist: create', "Testing if heading is Artist: create")
                    // name input
                    .assert.visible('input[id=id_name]')
                    .setValue('input[id=id_name]', sampleName)

                    // submit button
                    .assert.visible('#form-object-artist > div.modal-footer > button[type=submit]')
                    .click('#form-object-artist > div.modal-footer > button[type=submit]')

                break;
            case 'song':
                sampleName = Math.random() + CONSTANTS.SONGS.INPUT + Math.random();
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

                break;
        }
        return sampleName;
    }

    // export class bar { }
}