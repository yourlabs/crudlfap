var path = require('path')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

const extractSass = new ExtractTextPlugin({
  filename: 'crudlfap.css',
})

const extractToolbox = new ExtractTextPlugin({
  filename: 'toolbox.css',
})

var production = process.env.NODE_ENV == 'production'

var cfg = {
  context: __dirname,

  entry: {
    main: [
      'babel-polyfill',
      'whatwg-fetch',
      './node_modules/formdata-polyfill/formdata.min.js',
      './js/index.js',
    ],
  },
  output: {
    path: path.resolve('src/crudlfap/static/'),
    filename: 'crudlfap.js'
  },
  devtool: 'source-map',
  module: {
    rules: [
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'url-loader?limit=10000&mimetype=application/font-woff' },
      { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'file-loader' },
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            "presets": ["es2015", "react", "stage-0"],
            "plugins": ["transform-class-properties"],
            "env": {
              "development": {
                "plugins": [
                  ["react-transform", {
                    "transforms": [{
                      "transform": "react-transform-hmr",
                      "imports": ["react"],
                      "locals": ["module"]
                    }, {
                      "transform": "react-transform-catch-errors",
                      "imports": ["react", "redbox-react"]
                    }]
                  }]
                ]
              }
            },
            sourceMap: true
          }
        }
      },
      {
        test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        use: {
          loader: 'file-loader'
        }
      },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        use: {
          loader: 'url-loader?limit=10000&mimetype=application/font-woff'
        }
      },
      {
        test: /\.s?(c|a)ss$/,
        use: extractSass.extract({
          use: [
            {
              loader: 'css-loader',
              options: {
                modules: true, // default is false
                sourceMap: true,
                importLoaders: 1,
                sourceMap: true
              }
            },
            {
              loader: 'postcss-loader',
              options: {
                config: {
                  path: path.join(__dirname, './postcss.config.js')
                },
                sourceMap: true
              }
            },
            {
              loader: 'sass-loader',
              options: {
                sourceMap: true
              }
            },
          ]
        })
      },
    ]
  },
  plugins: [
    extractSass
  ]
}

if (production) {
  cfg.plugins.push(new UglifyJSPlugin())
}

module.exports = cfg
