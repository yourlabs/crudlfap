var path = require('path')
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');

var production = process.env.NODE_ENV == 'production'

const plugins = [
  new MiniCssExtractPlugin({
    filename: 'crudlfap.css',
  }),
];

if (!production) {
  // only enable hot in development
  plugins.push(new webpack.HotModuleReplacementPlugin());
}

module.exports = {
  context: __dirname,
  mode: production ? 'production' : 'development',
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()],
  },
  entry: {
    main: [
      'babel-polyfill',
      'whatwg-fetch',
      './node_modules/formdata-polyfill/formdata.min.js',
      './index.js',
    ],
  },
  output: {
    path: path.resolve('../src/crudlfap/static/'),
    filename: 'crudlfap.js'
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
          test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
          use: {
            loader: 'url-loader?limit=10000&mimetype=application/font-woff'
          }
      },
      { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'file-loader' },
      {
        test: /\.js$/,
        exclude: /turbolinks/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['stage-2', 'babel-preset-env'],
            sourceMap: true,
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
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          // 'postcss-loader',
          'sass-loader',
        ],
      },
    ]
  },
  plugins: plugins
};
