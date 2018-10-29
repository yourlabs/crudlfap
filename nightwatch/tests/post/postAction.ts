import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
  'Post : create post': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const postTitle = Math.random() + CONSTANTS.POST.INPUT_TITLE + Math.random();

    browser
      // after login go to post create page direct
      .url(CONSTANTS.POST.CREATE)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      // .assert.containsText('#modal-body-ajax', 'Post: create', "Testing if heading is Post: create")
      // name input
      .assert.visible('input[id=id_name]')
      .setValue('input[id=id_name]', postTitle)

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
      .assert.visible('#form-object-post > div.modal-footer > button[type=submit]')
      .click('#form-object-post > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // verify it created or not
      .url(CONSTANTS.POST.BASE_URL + "?q=" + postTitle)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(3) > a', postTitle, "Testing if post list contains new added post")


      .url(CONSTANTS.POST.BASE_URL + "?q=" + postTitle)
      // get id and delete that one
      .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2)', async (tdContentId) => {
        console.log('------id-----', tdContentId.value)
        browser
          .getText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(3) > a', async (tdContentName) => {
            await CommonFunction.deleteByPostId(browser, tdContentId.value, tdContentName.value);
          })
      })
      .end();
  },

  'Post : create post by popup': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const postTitle = Math.random() + CONSTANTS.POST.INPUT_TITLE2;
    browser
      // after login go to post create page direct
      .url(CONSTANTS.POST.BASE_URL)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

      .assert.visible('body > div.fixed-actions > a[href="/post/create?_next=/post"]')
      .click('body > div.fixed-actions > a[href="/post/create?_next=/post"]', () => {
        browser
          .waitForElementVisible('#modal', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
          .pause(CONSTANTS.PAUSE_TIMEOUT)
          .expect.element('#modal').to.have.css('display').which.equal('block');
        browser
          // .assert.containsText('#modal #modal-title-ajax', 'Post: create', "Testing if heading is Post: create")
          // name input
          .assert.visible('input[id=id_name]')
          .setValue('input[id=id_name]', postTitle)

          .pause(CONSTANTS.PAUSE_TIMEOUT)

          // owner selection
          .assert.visible('#form-object-post > div.modal-content > div:nth-child(4) > div#id_owner_container > div> input')
          .click('#form-object-post > div.modal-content > div:nth-child(4) > div#id_owner_container > div> input', () => {
            browser
              .expect.element('#form-object-post > div.modal-content > div:nth-child(4) > div#id_owner_container > div > ul').to.have.css('display').which.equal('block');
            browser
              .pause(CONSTANTS.PAUSE_TIMEOUT)
              .click('#form-object-post > div.modal-content > div:nth-child(4) > div#id_owner_container > div > ul >li:nth-child(2)')
          })
          .pause(CONSTANTS.PAUSE_TIMEOUT)

           
          .click('input[id=id_name]')

          // submit button
          .assert.visible('#form-object-post > div.modal-footer > button')
          .click('#form-object-post > div.modal-footer > button', () => {
            // verify it created or not
            browser
              .pause(CONSTANTS.PAUSE_TIMEOUT)
              .url(CONSTANTS.POST.BASE_URL + "?q=" + postTitle)
              .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
              .pause(CONSTANTS.PAUSE_TIMEOUT)
              .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(3) > a', postTitle, "Testing if post list contains new added post")
          })
      })
      .end();
  },

  'Post : Detail Post': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    browser
      .url(CONSTANTS.POST.BASE_URL)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr > td:nth-child(3) > a', (tdContentName) => {
        const contentName = tdContentName.value;
        browser
          .getText('#render-table > div > div > div > table > tbody > tr > td:nth-child(2)', (tdContentID) => {
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
                  .assert.urlEquals(CONSTANTS.POST.BASE_URL + '/' + contentId + '?_next=/post', 'Post Detail url is the correct')
                  .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                  // check get data Id is correct
                  .assert.visible('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(1) > td')
                  .assert.containsText('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(1) > td', contentId, 'Post Id matched')
                  .assert.visible('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(2) > td')
                  .assert.containsText('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(2) > td', contentName, 'Post title matched')
              })
          })
      })
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .end();
  },

  'Post : Edit post': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const postTitle = Math.random() + CONSTANTS.POST.EDIT_INPUT + Math.random();
    let contentId;
    browser
      .url(CONSTANTS.POST.BASE_URL)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr > td:nth-child(2)', (tdContentID) => {
        contentId = tdContentID.value;
        browser
          .click('a[data-target="row-actions-' + contentId + '"]', () => {
            // open menu
            browser.expect.element('#row-actions-' + contentId).to.have.css('display').which.equal('block')
          })
          .pause(CONSTANTS.PAUSE_TIMEOUT)
          // click on edit
          .assert.visible('#row-actions-' + contentId + ' > li:nth-child(2) > a')

          .click('#row-actions-' + contentId + ' > li:nth-child(2) > a', () => {
            // popup opened
            browser
              .pause(CONSTANTS.PAUSE_TIMEOUT)
              // name input
              .assert.visible('input[id=id_name]')
              .clearValue('input[id=id_name]')
              .setValue('input[id=id_name]', postTitle)

              .pause(CONSTANTS.PAUSE_TIMEOUT)
              // click on update
              .click('#form-object-post > div.modal-footer > button[type="submit"]', () => {
                browser
                  .url(CONSTANTS.POST.BASE_URL + "?q=" + postTitle)
                  .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
                  .pause(CONSTANTS.PAUSE_TIMEOUT)
                  .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(3) > a', postTitle, "Testing if post list contains updated post")
              })
          })
      })
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .end();
  },

  'Post : Delete Post': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    let contentId;
    browser
      .url(CONSTANTS.POST.BASE_URL)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .getText('#render-table > div > div > div > table > tbody > tr > td:nth-child(2)', async (tdContentID) => {
        contentId = tdContentID.value;
        browser
          .getText('#render-table > div > div > div > table > tbody > tr > td:nth-child(3) > a', async (tdContentName) => {
            await CommonFunction.deleteByPostId(browser, contentId, tdContentName.value);
          })
      })
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .end();
  }
}
