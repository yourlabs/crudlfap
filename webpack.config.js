var path = require('path')
const ExtractTextPlugin = require("extract-text-webpack-plugin");

const extractSass = new ExtractTextPlugin({
    filename: "crudlfap.css",
});

/* eslint-disable */
module.exports = {
/* eslint-enable */
  entry: {
      main: [
          'babel-polyfill',
          './js/index.js',
          './node_modules/materialize-css/sass/materialize.scss',
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
        test: /\.js$/,
        exclude: /(turbolinks)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['stage-2', 'babel-preset-env'],
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
        test: /\.s(a|c)ss$/,
        use: extractSass.extract({
          use: [
            {
              loader: 'css-loader',
              options: {
                sourceMap: true
              }
            },
            {
              loader: 'sass-loader',
              options: {
                sourceMap: true
              }
            }
          ]
        })
      }
    ]
  },
  plugins: [
    extractSass
  ]
}
