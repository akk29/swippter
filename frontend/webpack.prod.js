import { merge } from 'webpack-merge';
import common from './webpack.common.js';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import TerserPlugin from 'terser-webpack-plugin';
import CssMinimizerPlugin from 'css-minimizer-webpack-plugin';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default merge(common, {
  mode: 'production',
  devtool: 'source-map',
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'static/js/[name].[contenthash:8].js',
    publicPath: './'
  },
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin(), new CssMinimizerPlugin()],
    splitChunks: {
      chunks: 'all',
      name: false,
    },
    runtimeChunk: { 
      name: entrypoint => `runtime-${entrypoint.name}` 
    },
  },
  module: {
    rules: [
      { 
        test: /\.s[ac]ss$/, 
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'] 
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({ 
      filename: 'static/css/[name].[contenthash:8].css' 
    })
  ]
});