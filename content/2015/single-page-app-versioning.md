Title: Single Page App Versioning
Date: 2015-09-26 21:00
Category:

Versioning applications isn't quite as clear cut as [versioning libraries](http://semver.org/); individuals on teams will almost certainly fork the codebase to work on features (sometimes long-lived) but you will still want to provide an easy, and consistent way to refer to each build generated from your Continuous Integration system.

My preferred approach combines the human managed semantic version number from a project's `package.json` file with the short commit hash; ie: `0.1.6-deff00`; you can configure your project's build system to replace the commit hash for local (non-ci) builds.  This also has the nice advantage of making each build traceable back to your project's Git repository should you forget to tag a build :)

The following example is for [webpack](https://webpack.github.io/), but could easily be modified for any build system:

```javascript
var webpack = require('webpack');
var gitrev = require('git-rev-sync');
var pkg = require('./package.json')

function version() {
  return pkg.version + '-' + (node.env.PRODUCTION ? gitrev.short() : 'dev');
}

module.exports = {
  /* ... */
  plugins: [
    new webpack.DefinePlugin({
      VERSION: version()
    })
  ]
}
```
