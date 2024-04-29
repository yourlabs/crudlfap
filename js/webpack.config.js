var path = require('path')
const TerserPlugin = require('terser-webpack-plugin');

var production = process.env.NODE_ENV == 'production'

var cfg = {
  context: __dirname,
  mode: production ? 'production' : 'development',
  entry: {
    main: [
      //'whatwg-fetch',
      //'./node_modules/formdata-polyfill/formdata.min.js',
      './index.js',
    ],
  },
  output: {
    path: __dirname + '../src/crudlfap/static/',
    filename: 'crudlfap.js'
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
          test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
          loader: 'url-loader',
          options: {
            limit: 10000,
            mimetype: 'application/font-woff'
          }
      },
      {
          test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
          loader: 'file-loader'
      },
      {
        test: /\.js$/,
        exclude: /turbo/,
        use: {
          loader: 'babel-loader',
          options: {
            sourceMap: true,
            presets: ['@babel/preset-env'],
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
        test: /\.s[ac]ss$/i,
        use: [
          'style-loader',
          'css-loader',
          'sass-loader',
        ],
      },
    ]
  },
}

if (production) {
  cfg.optimization = {
    minimize: true,
    minimizer: [new TerserPlugin()],
  }
}

module.exports = cfg
