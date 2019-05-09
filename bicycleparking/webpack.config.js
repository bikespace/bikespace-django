const path = require('path')
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = env => {
    return {
        context: __dirname,
        entry: './static/src/js/index.js',
        output: {
            path: path.join(__dirname, env.BUILD_PATH || './dist'),
            publicPath: env.ASSET_PATH || './',
            filename: 'bundle.js',
        },
        plugins: [new CopyWebpackPlugin([
            { from: 'static/src/style', to: 'style' }
          ])
        ],
    }
}