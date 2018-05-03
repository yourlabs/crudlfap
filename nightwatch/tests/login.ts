import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../shared/CONSTANTS';

module.exports = {
  'Login : submit with wrong credentials': (browser: NightwatchBrowser) => {
    browser
      .url(CONSTANTS.BASE_URL)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)

      .assert.visible('input[id=id_username]')
      .setValue('input[id=id_username]', CONSTANTS.USER_CREDENTIALS.WRONG.USERNAME)

      .assert.visible('input[id=id_password]')
      .setValue('input[id=id_password]', CONSTANTS.USER_CREDENTIALS.WRONG.PASSWORD)

      .assert.visible('button[type=submit]')
      .click('button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // after login
      .assert.containsText('small[class=error]', 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
      .end();
  },

  'Login : submit with correct credentials': (browser: NightwatchBrowser) => {
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
      .end();
  }
};