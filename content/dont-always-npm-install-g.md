Title: Don't (always) npm install -g
Date: 2015-11-26 21:00
Category: JavaScript

Had a chat with a respected hacker friend of mine who did not know about this trick (although to be fair, I'm not sure I knew about it until all that long ago).

There's almost never any need to use `npm install -g`, you could argue it's an anti-pattern as it makes your software harder to install for other users and can easily cause conflcits between projects.  The most common candidates for a bit of global installing are test and build utils like mocha, typescript and grunt-cli; instead of reaching for `-g` you can install them locally in your project and execute them from the symlink created in `node_modules/.bin`, eg:

```bash
npm install --save-dev mocha
./node_modules/.bin/mocha --help
```

You can also make use of the `npm bin` command which will resolve the nearest `node_modules/.bin` path to the cwd:

```
`npm bin`/mocha --help
```

As an added bonus, NPM scripts don't need to add the `node_modules/.bin` prefix - it's added automatically:

```json
{
  "name": "my-awesome-pkg",
  "scripts": {
    "test": "mocha"
  }
}
```
