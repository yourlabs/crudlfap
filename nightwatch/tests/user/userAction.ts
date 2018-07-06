// import { NightwatchBrowser } from 'nightwatch';
// import { CONSTANTS } from '../../shared/CONSTANTS';
// import { CommonFunction } from '../../shared/commonFunction';

// module.exports = {
//   'User : create user': async (browser: NightwatchBrowser) => {
//     await CommonFunction.loginByDev(browser);
//     const userName = Math.random() + CONSTANTS.USER.INPUT_USER + Math.random();

//     browser
//       // after login go to post create page direct
//       .url(CONSTANTS.POST.CREATE)
//       .waitForElementVisible('body', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
//       .assert.containsText('#modal-title-ajax', 'User: create', "Testing if heading is User: create")

//       // name input
//       .assert.visible('input[id=id_username]')
//       .setValue('input[id=id_username]', userName)

//       // owner selection
//       .assert.visible('#id_owner_container > div > input')
//       .click('#id_owner_container > div > input', () => {
//         browser
//           .expect.element('#id_owner_container > div > ul').to.have.css('display').which.equal('block')
//       })
//       .pause(CONSTANTS.PAUSE_TIMEOUT)

//       // click on option
//       .click('#id_owner_container > div > ul > li:nth-child(2)')
//       .pause(CONSTANTS.PAUSE_TIMEOUT)

//       // submit button
//       .assert.visible('#form-object-post > div.modal-footer > button[type=submit]')
//       .click('#form-object-post > div.modal-footer > button[type=submit]')

//       // verify it created or not
//       .url(CONSTANTS.POST.BASE_URL + "?q=" + userName)
//       .waitForElementVisible('#modal-title-ajax', CONSTANTS.WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT)
//       .pause(CONSTANTS.PAUSE_TIMEOUT)
//       .assert.containsText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(3) > a', userName, "Testing if post list contains new added post")


//       // .url(CONSTANTS.POST.BASE_URL + "?q=" + userName)
//       // // get id and delete that one
//       // .getText('#render-table > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2)', async (tdContentId) => {
//       //   console.log('------id-----', tdContentId.value)
//       //   browser
//       //     .getText('#render-table > div > div > div > table > tbody > tr:last-child > td:nth-child(3) > a', async (tdContentName) => {
//       //       await CommonFunction.deleteByPostId(browser, tdContentId.value, tdContentName.value);
//       //     })
//       // })
//       // .end();
//   },

// }  