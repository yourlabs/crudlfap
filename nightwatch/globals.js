const chromedriver = require('chromedriver');
const sauceTunnel = require('sauce-tunnel');

const tunnel = new sauceTunnel('navjot.g', 'f817b186-0804-45a3-bdff-597eafc9da71', 'tunnel', true/* ['--verbose'] */);

module.exports = {
    before: (done) => {
        console.log('------chromedriver---start');
        tunnel.start(function (status) {
            if (status === false) {
                throw new Error('Something went wrong with the tunnel');
            }
            console.log('------tunnel---start');
            chromedriver.start();
            done();
        });
    },
    after: (done) => {
        console.log('------chromedriver---stop');
        tunnel.stop(function () {
            // Tunnel destroyed
            console.log('------tunnel---stop');
            chromedriver.stop();
            done();
        });
    }
};
