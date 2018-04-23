const sauceConnectLauncher = require('sauce-connect-launcher');

let sauceConnectTunnel;

module.exports = {
  before: (done) => {
    sauceConnectLauncher({
      username: 'navjot.g',
      accessKey: 'f817b186-0804-45a3-bdff-597eafc9da71'
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
