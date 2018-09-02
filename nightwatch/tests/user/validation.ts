import { NightwatchBrowser } from 'nightwatch';
import { CONSTANTS } from '../../shared/CONSTANTS';
import { CommonFunction } from '../../shared/commonFunction';

module.exports = {
  'User : create user validation': async (browser: NightwatchBrowser) => {
    await CommonFunction.loginByDev(browser);
    browser
      // after login go to user create page direct
      .url(CONSTANTS.USER.CREATE)
      .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
      
      // blank validation
      // username input
      .assert.containsText('#id_username_container > label', 'Username')
      .assert.visible('input[id=id_username]')

      // email input
      .assert.containsText('#id_email_container > label', 'Email address')
      .assert.visible('input[id=id_email]')

      // Groups input
      .assert.containsText('#id_groups_container > label', 'Groups')
      .assert.visible('#id_groups_container > div.select-wrapper > input')

      // staff selection
      .assert.containsText('#id_is_staff_container > label > span', 'Staff status')
      // .assert.visible('#id_is_staff_container > label > input')

      // Superuser status
      .assert.containsText('#id_is_superuser_container > label > span', 'Superuser status')
      // .assert.visible('#id_is_superuser_container > label > input')

      // submit button
      .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
      .click('#form-object-user > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .assert.visible('#id_username_container > div.errors > small')
      .assert.containsText('#id_username_container > div.errors > small', 'This field is required.')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      // invalid validation
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.visible('input[id=id_username]')
      .setValue('input[id=id_username]', CONSTANTS.USER.INVALID_USER)

      // submit button
      .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
      .click('#form-object-user > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.visible('#id_username_container> div.errors > small')
      .assert.containsText('#id_username_container > div.errors > small', 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.')

      // duplicate validation    
      .pause(CONSTANTS.PAUSE_TIMEOUT)
      .assert.visible('input[id=id_username]')
      .clearValue('input[id=id_username]')
      .setValue('input[id=id_username]', CONSTANTS.USER.EXISTING_USER)

      .pause(CONSTANTS.PAUSE_TIMEOUT)
      // submit button
      .assert.visible('#form-object-user > div.modal-footer > button[type=submit]')
      .click('#form-object-user > div.modal-footer > button[type=submit]')
      .pause(CONSTANTS.PAUSE_TIMEOUT)

      .assert.visible('#id_username_container > div.errors > small')
      .assert.containsText('#id_username_container > div.errors > small', 'A user with that username already exists.')

      .end();
  }
};