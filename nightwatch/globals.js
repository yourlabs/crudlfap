// const chromedriver = require('chromedriver');
// const sauceTunnel = require('sauce-tunnel');
const sauceConnectLauncher = require('sauce-connect-launcher')
// const tunnel = new sauceTunnel('navjot.g', 'f817b186-0804-45a3-bdff-597eafc9da71', 'tunnel', true/* ['--verbose'] */);
let sauceConnectProcess1;
module.exports = {
    before: (done) => {
        console.log('------chromedriver---start');

        // tunnel.start(function (status) {
        //     if (status === false) {
        //         throw new Error('Something went wrong with the tunnel');
        //     }
        //     console.log('------tunnel---start');
        //     // chromedriver.start();
        //     done();
        // });
        sauceConnectLauncher({
            username: 'navjot.g',
            accessKey: 'f817b186-0804-45a3-bdff-597eafc9da71'
        }, function (err, sauceConnectProcess) {
            if (err) {
                console.error(err.message);
                return;
            }
            console.log("Sauce Connect ready");
            sauceConnectProcess1 = sauceConnectProcess;
            done();
        });
    },
    after: (done) => {
        console.log('------chromedriver---stop');
        // tunnel.stop(function () {
        //     // Tunnel destroyed
        //     console.log('------tunnel---stop');
        //     // chromedriver.stop();
        //     done();
        // });

        sauceConnectProcess1.close(function () {
            console.log("Closed Sauce Connect process");
            done();
        })
    }
};
