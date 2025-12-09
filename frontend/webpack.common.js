import path from 'path';
import { fileURLToPath } from 'url';
import HtmlWebpackPlugin from 'html-webpack-plugin';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const common = {
  entry: './index.tsx',
  resolve: { 
    extensions: ['.tsx', '.ts', '.js', '.jsx'],
    modules: [path.resolve(__dirname, 'app'), 'node_modules']
  },
  module: {
    rules: [
      { 
        test: /\.tsx?$/, 
        use: 'ts-loader', 
        exclude: /node_modules/ 
      },
      { 
        test: /\.s[ac]ss$/, 
        use: ['style-loader', 'css-loader', 'sass-loader'] 
      },
      { 
        test: /\.(png|jpg|jpeg|gif|svg)$/i, 
        type: 'asset/resource' 
      },
      { 
        test: /\.(woff2?|eot|ttf|otf)$/i, 
        type: 'asset/resource' 
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({ 
      template: './public/index.html' 
    })
  ],
  output: { 
    path: path.resolve(__dirname, 'dist'), 
    publicPath: '/',
    clean: true
  }
};

export default common;