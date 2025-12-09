import { merge } from 'webpack-merge';
import common from './webpack.common.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default merge(common, {
  mode: 'development',
  devtool: 'eval-cheap-module-source-map',
  output: {
    filename: '[name].js',
  },
  devServer: {
    static: {
      directory: path.resolve(__dirname, 'public'),
    },
    historyApiFallback: true,
    hot: true,
    open: true,
    port: 3000,
    compress: true,
  }
});