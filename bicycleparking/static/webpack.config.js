
const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = env => {
    console.log('STATIC_PATH', env.STATIC_PATH)
    return {
        entry: './src/js/index.js',
        output: {
            path: path.join(__dirname, 'dist'),
            publicPath: env.STATIC_PATH,
            filename: 'bundle.js',
        },
        plugins: [new HtmlWebpackPlugin({
            template: 'src/index.html',
            templateParameters: {
                'assetpath': env.STATIC_PATH
            }
        }), new CopyWebpackPlugin([
            { from: 'src/style', to: 'style' },
            { from: 'src/sw.js', to: 'sw.js' },
            { from: 'src/manifest.json', to: 'manifest.json' }])],
    }
}
