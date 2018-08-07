import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';
import { AsyncResource } from 'async_hooks';
import { endianness } from 'os';

module.exports = {

  'User : create user': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const userName = Math.random() + CONSTANTS.USER.INPUT_USER + Math.random();

    browser
      // after login go to user create page direct
      .url(CONSTANTS.USER.CREATE)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      //   .assert.containsText('#modal-title-ajax', 'User: create', "Testing if heading is User: create")

      .pause(CONSTANTS.PAUSE_TIMEOUT)
      // name input
      .assert.visible('input[id=id_username]')
      .setValue('input[id=id_username]', userName)

      // submit button
      .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
      .click('#form-object-user > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      //verify it created or not
      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(2) > a', userName, "Testing if user list contains new added user")
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      // get username and delete by username
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a', async (tdContentName) => {
        await CommonFunction.deleteByUserName(browser, tdContentName.value);
      })

      .end();
  },

  'User : create user with email': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const userName = Math.random() + CONSTANTS.USER.INPUT_USER + Math.random();
    const userEmail = Math.random() + CONSTANTS.USER.INPUT_EMAIL;

    browser
      // after login go to user create page direct
      .url(CONSTANTS.USER.CREATE)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

      .pause(CONSTANTS.PAUSE_TIMEOUT)
      // name input
      .assert.visible('input[id=id_username]')
      .setValue('input[id=id_username]', userName)

      // email input
      .assert.visible('input[id=id_email]')
      .setValue('input[id=id_email]', userEmail)

      // submit button
      .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
      .click('#form-object-user > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      //verify it created or not
      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(2) > a', userName, "Testing if user list contains new added user")
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      // get username and delete by username
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a', async (tdContentName) => {
        await CommonFunction.deleteByUserName(browser, tdContentName.value);
      })
      .end();
  },

  'User : create user : with Groups': async (browser: NightwatchBrowser) => {

    await CommonFunction.loginByDev(browser);
    const userName = Math.random() + CONSTANTS.USER.INPUT_USER + Math.random();

    browser
      // after login go to group create page direct
      .url(CONSTANTS.USER.CREATE)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

      .pause(CONSTANTS.PAUSE_TIMEOUT)
      // name input
      .assert.visible('input[id=id_username]')
      .setValue('input[id=id_username]', userName)

      // groups selection
      .assert.visible('#id_groups_container  > div > input')
      .click('#id_groups_container > div > input', () => {
        browser
          .expect.element('#id_groups_container > div > ul').to.have.css('display').which.equal('block')
      })
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      // click on option
      .click('#id_groups_container > div > ul > li:nth-child(3)')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .click('input[id=id_username]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // submit button
      .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
      .click('#form-object-user > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      //verify it created or not
      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(2) > a', userName, "Testing if user list contains new added user")
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      // get username and delete by username
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a', async (tdContentName) => {
        await CommonFunction.deleteByUserName(browser, tdContentName.value);
      })
      .end();
  },

  'User : create user : with staff status': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const userName = Math.random() + CONSTANTS.USER.INPUT_USER + Math.random();

    browser
      // after login go to user create page direct
      .url(CONSTANTS.USER.CREATE)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      //   .assert.containsText('#modal-title-ajax', 'User: create', "Testing if heading is User: create")
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // name input
      .assert.visible('input[id=id_username]')
      .setValue('input[id=id_username]', userName)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // staff status selection
      .assert.visible('#id_is_staff_container > label > span[for="id_is_staff"]')
      // .click('#id_is_staff>')
      .click('#id_is_staff_container > label > span[for="id_is_staff"]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      //submit button
      .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
      .click('#form-object-user > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      //verify it created or not
      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(2) > a', userName, "Testing if user list contains new added user")
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      // get username and delete by username
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a', async (tdContentName) => {
        await CommonFunction.deleteByUserName(browser, tdContentName.value);
      })
      .end();
  },

  'User : create user : with superuser status': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const userName = Math.random() + CONSTANTS.USER.INPUT_USER + Math.random();

    browser
      // after login go to user create page direct
      .url(CONSTANTS.USER.CREATE)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      //   .assert.containsText('#modal-title-ajax', 'User: create', "Testing if heading is User: create")
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // name input
      .assert.visible('input[id=id_username]')
      .setValue('input[id=id_username]', userName)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // superuser status selection
      .assert.visible('#id_is_superuser_container > label > span[for="id_is_superuser"]')
      // .click('#id_is_superuser>')
      .click('#id_is_superuser_container > label > span[for="id_is_superuser"]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      //submit button
      .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
      .click('#form-object-user > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      //verify it created or not
      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(2) > a', userName, "Testing if user list contains new added user")
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      // get username and delete by username
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a', async (tdContentName) => {
        await CommonFunction.deleteByUserName(browser, tdContentName.value);
      })
      .end();
  },

  'User : create user : with email, groups, staff and superuser status': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const userName = Math.random() + CONSTANTS.USER.INPUT_USER + Math.random();
    const userEmail = Math.random() + CONSTANTS.USER.INPUT_EMAIL;

    browser
      // after login go to user create page direct
      .url(CONSTANTS.USER.CREATE)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      //   .assert.containsText('#modal-title-ajax', 'User: create', "Testing if heading is User: create")
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // name input
      .assert.visible('input[id=id_username]')
      .setValue('input[id=id_username]', userName)
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // email input
      .assert.visible('input[id=id_email]')
      .setValue('input[id=id_email]', userEmail)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // groups selection
      .assert.visible('#id_groups_container  > div > input')
      .click('#id_groups_container > div > input', () => {
        browser
          .expect.element('#id_groups_container > div > ul').to.have.css('display').which.equal('block')
      })
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      // click on option
      .click('#id_groups_container > div > ul > li:nth-child(3)')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .click('input[id=id_username]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // staff status selection
      .assert.visible('#id_is_staff_container > label > span[for="id_is_staff"]')
      .click('#id_is_staff_container > label > span[for="id_is_staff"]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // superuser status selection
      .assert.visible('#id_is_superuser_container > label > span[for="id_is_superuser"]')
      .click('#id_is_superuser_container > label > span[for="id_is_superuser"]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      //submit button
      .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
      .click('#form-object-user > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      //verify it created or not
      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(2) > a', userName, "Testing if user list contains new added user")
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
      // get username and delete by username
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a', async (tdContentName) => {
        await CommonFunction.deleteByUserName(browser, tdContentName.value);
      })
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .end();
  },


  'User : create user by popup': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const userName = Math.random() + CONSTANTS.USER.INPUT_USER + Math.random();

    browser
      // after login go to user create page direct
      .url(CONSTANTS.USER.BASE_URL)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

      .assert.visible('body > div.fixed-actions > a[href="/user/create?_next=/user"]')
      .click('body > div.fixed-actions > a[href="/user/create?_next=/user"]', () => {
        browser
          .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
          .pause(CONSTANTS.PAUSE_TIMEOUT)
        // .expect.element('#modal').to.have.css('display').which.equal('block');
        browser
          .pause(CONSTANTS.PAUSE_TIMEOUT)
          // name input
          .assert.visible('input[id=id_username]')
          .setValue('input[id=id_username]', userName)
          .pause(CONSTANTS.PAUSE_TIMEOUT)

          // submit button
          .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
          .click('#form-object-user > div.modal-footer > button[type=submit]')
          .pause(CONSTANTS.PAUSE_TIMEOUT)

          //verify it created or not
          .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
          .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
          .pause(CONSTANTS.PAUSE_TIMEOUT)
          .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(2) > a', userName, "Testing if user list contains new added user")
      })
      .end();
  },

  'User : Detail user': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    browser
      .url(CONSTANTS.USER.BASE_URL)
      .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a', (tdContentName) => {
        const contentName = tdContentName.value;
        browser
          .url(CONSTANTS.USER.BASE_URL + '/' + contentName + '?_next=/user')
          .waitForElementVisible('#modal-body-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
          .assert.visible('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(4) > td')
          .assert.containsText('#modal-body-ajax > div.modal-content > div > table > thead > tr:nth-child(4) > td', contentName, 'User Name matched')
      })

      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .end()
  },

  'User : Edit user': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    const userName = Math.random() + CONSTANTS.USER.EDIT_INPUT + Math.random();
    const firstName = 'test';
    const lastName = 'test123';
    let contentId;
    browser
      .url(CONSTANTS.USER.BASE_URL)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // click menu
      .assert.visible('#render-table > div > div > div > table > tbody > tr > td:nth-child(8) > a > i')
      .click('#render-table > div > div > div > table > tbody > tr > td:nth-child(8) > a > i')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // click edit
      .assert.visible('#render-table > div > div > div > table > tbody > tr > td:nth-child(8) > ul > li:nth-child(2) > a')
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .click('#render-table > div > div > div > table > tbody > tr > td:nth-child(8) > ul > li:nth-child(2) > a', () => {
        //popup opened
        browser
          .pause(CONSTANTS.PAUSE_TIMEOUT)
          // username input
          .assert.visible('input[id=id_username]')
          .clearValue('input[id=id_username]')
          .setValue('input[id=id_username]', userName)
          .pause(CONSTANTS.PAUSE_TIMEOUT)

          // firstName input
          .assert.visible('input[id=id_first_name]')
          .clearValue('input[id=id_first_name]')
          .setValue('input[id=id_first_name]', firstName)
          .pause(CONSTANTS.PAUSE_TIMEOUT)

          // lastName input
          .assert.visible('input[id=id_last_name]')
          .clearValue('input[id=id_last_name]')
          .setValue('input[id=id_last_name]', lastName)
          .pause(CONSTANTS.PAUSE_TIMEOUT)

          // click update button
          .click('#form-object-user > div.modal-footer > button[type="submit"]', () => {
            console.log("update button clicked");
            browser
              .pause(CONSTANTS.PAUSE_TIMEOUT)
              .url(CONSTANTS.USER.BASE_URL + "?q=" + userName)
              .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
              .pause(CONSTANTS.PAUSE_TIMEOUT)
              .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(2) > a', userName, "Testing if user list contains updated user")
          })
      })
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .end();
  },

  'User : Delete user': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    browser
      .url(CONSTANTS.USER.BASE_URL)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a', async (tdContentName) => {
        await CommonFunction.deleteByUserName(browser, tdContentName.value);
      })
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .end();
  }

}



