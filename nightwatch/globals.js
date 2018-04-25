/* globals process */
const sauceConnectLauncher = require('sauce-connect-launcher');

let sauceConnectTunnel;

module.exports = {
  before: (done) => {
    sauceConnectLauncher({
      username: process.env.SAUCELABS_USERNAME,
      accessKey: process.env.SAUCELABS_TOKEN
    }, function (err, sauceConnectProcess) {
      if (err) {
        console.error(err.message);

        return;
      }
      console.log('Sauce Connect ready');
      sauceConnectTunnel = sauceConnectProcess;
      done();
    });
  },
  after: (done) => {
    sauceConnectTunnel.close(function () {
      console.log('Closed Sauce Connect process');
      done();
    });
  }
};
