Title: Babel ❤ NPM
Date: 2015-10-24 21:00
Category: JavaScript

Once you go ES6, you never go back ;)  In order to create ES5-backwards-compatible modules, there's are a few nuances that you need to be aware of:

### babelify
Transpiling your NPM modules to ES5 with [babel](https://babeljs.io/) will allow them to work in a wide variety of environments.  Add a `prepublish` script to your `package.json`'s scripts block to automate this when you run `npm publish`.  By convention `/lib` is a good place to output your ES5 artefacts to, and it's a good idea to produce a clean build each time (with the [rimraf module](https://www.npmjs.com/package/rimraf) providing a cross platform implementation of `rm -rf`, windows users will thank you.)

###### `/package.json`
```
{
  "name": "my_pkg",
  "scripts": {
    "prepublish": "rimraf lib && babel --out-dir lib src"
  }
}
```

### main
Traditionally your `index.js` file would reside in the root of your module (this is where NPM will look for it by default); however as we are going to transpile to ES5 you'll want to put your index file, and all other ES6 sources under `/src`.

Your `package.json`'s `main` block should point to the transpiled `index.js` file in the `/lib` folder.  If you're feeling adventurous you incude a [`jsnext:main`](https://github.com/caridy/es6-module-transpiler-npm-resolver) block and point to to your ES6 entry point.

###### `/package.json`
```
{
  "name": "my_pkg",
  "main": "lib/index.js",
  "jsnext:main": "src/index.js"
}
```

## Mocha
Mocha does the job well and it's easy to configure for use with babel; just give it a `--compilers` flag when you invoke it:

###### `/package.json`
```
{
  "name": "my_pkg",
  "scripts": {
    "test": "mocha --compilers js:babel/register --recursive"
  }
}
```

## .npmignore
This one tripped me up; when I published my first NPM modules which made use of babel ([redux-action-side-effects](https://github.com/jonnyreeves/redux-action-side-effects)) my `/lib` folder wasn't included in the final archived vended by NPM.  Turns out that NPM will [automatically exclude everything in your `.gitignore` file](https://docs.npmjs.com/misc/developers#keeping-files-out-of-your-package) (and as the `/lib` folder contains build artefacts I excluded it from source control).  To override this add a `/.npmignore` file:

##### `/.npmignore`
```
# If this file is not present the contents of .gitignore are used
/.gitignore
```

Happy `npm publish`ing!
