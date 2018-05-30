
const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
    entry: './src/js/index.js',
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'bundle.js',
    },
    plugins: [new HtmlWebpackPlugin({
        template: 'src/index.html'
    }), new CopyWebpackPlugin([
        { from: 'src/style', to: 'style' },
        { from: 'src/sw.js', to: 'sw.js' },
        { from: 'src/manifest.json', to: 'manifest.json' }])],
};
