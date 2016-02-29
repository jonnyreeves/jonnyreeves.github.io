Title: Simple Webpack Prod and Dev Config
Date: 2016-02-29 21:00

Webpack 2 is just around the corner with the [promise of easier command line configuration](https://gist.github.com/sokra/27b24881210b56bbaff7#configuration), however whilst we're stuck with webpack 1, here's an easy way to split you configuration between your development flow (with hot-module-reloading) and production (with minification).

The trick revolves around the fact that webpack configuration can be a CommonJS module and can pick up on environment variables via Node's `process.env` object.

Start by modifying your `webpack.config.js` file (typically in the root of your project, next to your `package.json` file) to look something like this:

```js
var webpack = require("webpack");

var isProd = (process.env.NODE_ENV === 'production');

// Conditionally return a list of plugins to use based on the current environment.
// Repeat this pattern for any other config key (ie: loaders, etc).
function getPlugins() {
  var plugins = [];

  // Always expose NODE_ENV to webpack, you can now use `process.env.NODE_ENV`
  // inside your code for any environment checks; UglifyJS will automatically
  // drop any unreachable code.
  plugins.push(new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': process.env.NODE_ENV
    }
  }));

  // Conditionally add plugins for Production builds.
  if (isProd) {
    plugins.push(new webpack.optimize.UglifyJsPlugin());
  }

  // Conditionally add plugins for Development
  else {
    // ...
  }

  return plugins;
}

// Export Webpack configuration.
module.exports = {
  plugins: getPlugins()
};
```

With this in place you can now set the `NODE_ENV` environment variable before invoking webpack's command line tool:

```
NODE_ENV=production webpack
```

If you are using [npm scripts for your build process](http://blog.keithcirkel.co.uk/why-we-should-stop-using-grunt/), you can add a `start` script to spin up your hot-loading development server and a `dist` script for creating your distribution assets for production. (note there's no need to set the `NODE_ENV` environment variable outside of production as an empty (`undefined`) value will default to false in your webpack config):

```
"scripts": {
  "dist": "NODE_ENV=production webpack",
  "start": "webpack",
}
```
