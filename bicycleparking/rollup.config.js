import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import builtins from 'rollup-plugin-node-builtins';
import globals from 'rollup-plugin-node-globals';
import postcss from 'rollup-plugin-postcss';
import simplevars from 'postcss-simple-vars';
import nested from 'postcss-nested';
import cssnext from 'postcss-cssnext';
import csscalc from 'postcss-calc';
import cssnano from 'cssnano';

export default {
  entry: './static/js/index.js',
  dest: './static/main.js',
  format: 'iife',
  plugins: [
    resolve({
      module: true, // Default: true
      jsnext: true,  // Default: false
      main: true,  // Default: true
      browser: true,  // Default: false
      extensions: [ '.js', '.json' ],  // Default: ['.js']
    }),
    commonjs(),
    globals(),
    builtins(),
    postcss({
      plugins:[
        simplevars(),
        nested(),
        cssnext({ warnForDuplicates: false }),
        cssnano(),
        csscalc()
      ],
      extensions: [ '.css' ]
    })
  ]
};