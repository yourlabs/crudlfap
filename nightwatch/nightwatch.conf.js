const config = { // we use a nightwatch.conf.js file so we can include comments and helper functions
  'src_folders': [
    'dist'
  ],
  'output_folder': 'reports',
  'custom_commands_path': '',
  'custom_assertions_path': '',
  'page_objects_path': '',
  'globals_path': './globals.js',
  'selenium': {
    'start_process': false,
    'server_path': '',
    'log_path': '',
    'host': '127.0.0.1',
    'port': 4444
  },
  // 'test_workers': {
  //   'enabled': true, 'workers': 'auto'
  // }, // perform tests in parallel where possible
  'test_settings': {
    'default': {
      'launch_url': 'http://ondemand.saucelabs.com:80',
      'selenium_port': 80,
      'selenium_host': 'ondemand.saucelabs.com',
      'silent': true,
      'screenshots': {
        'enabled': false,
        'path': ''
      },
      'username': process.env.SAUCELABS_USERNAME,
      'access_key': process.env.SAUCELABS_TOKEN,
      'skip_testcases_on_fail': false,
      'desiredCapabilities': {
        'acceptSslCerts': true,
        'javascriptEnabled': true
      }
    },
    'chrome': {
      'desiredCapabilities': {
        'browserName': 'Chrome',
        'version': 'latest'
      }
    },
    'internet_explorer': {
      'desiredCapabilities': {
        'browserName': 'internet explorer',
        'version': 'latest'
      }
    },
    'firefox': {
      'desiredCapabilities': {
        'browserName': 'firefox',
        'version': 'latest'
      }
    }
  }
};
module.exports = config;
