/* globals process */
const sauceConnectLauncher = require('sauce-connect-launcher');
const chai = require('chai');
const expect = chai.expect;

let sauceConnectTunnel;

module.exports = {
  before: (browser, done) => {
    sauceConnectLauncher({
      username: process.env.SAUCELABS_USERNAME,
      accessKey: process.env.SAUCELABS_TOKEN
    }, function (err, sauceConnectProcess) {
      expect(err).to.be.null;
      if (err) {
        console.error('Sauce Connect Error : ', err.message);
        browser.end();

        return;
      }
      console.log('Sauce Connect ready');
      sauceConnectTunnel = sauceConnectProcess;
      done();
    });
  },
  after: (browser, done) => {
    sauceConnectTunnel.close(function () {
      console.log('Closed Sauce Connect process');
      done();
    });
  }
};
