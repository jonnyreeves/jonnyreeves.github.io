Title: Hot loading in Express
Date: 2015-10-31 21:00
Category: JavaScript

Gaffa tape time.  Getting iteration times down is important when building software, if nothing else it makes it more fun and help you keep the flow going.  With this in mind, let's get hot-loading working with [Mustache templates](https://github.com/janl/mustache.js/) on an [express](https://www.npmjs.com/package/express)-based local development server.

Let's start simple by serving some templates:

```javascript
import express from 'express';
import mustache from 'mustache';
import fs from 'fs';

// Create a new express server instance.
const app = express();

// Handle GET requests to `/hello`.
app.get('/hello', (req, res) => {
  // Read the template and JSON data from the local filesystem.
  const tpl = fs.readFileSync('./hello.mustache', 'utf8');
  const data = JSON.parse(fs.readFileSync('./hello.json'));

  // Serve back the rendered template.
  res.send(mustache.render(tpl, data));
});

console.log(`server started at http://localhost:3000`);
app.listen(3000);
```

So far so good, but let's make it hot-reload so we can do this:

[![https://gyazo.com/326ca72b98bce37af177d9e8d5143279](https://i.gyazo.com/326ca72b98bce37af177d9e8d5143279.gif)](https://gyazo.com/326ca72b98bce37af177d9e8d5143279)

First stop is to grab the [livereload module](https://www.npmjs.com/package/livereload) from NPM; this creates its own server which serves a javascript file used for relaying changes back to the browser; it also sets up a file-system monitor to detect changes when you modify your source files.

```javascript
// Create a livereload server
const hotServer = livereload.createServer({
  // Reload on changes to these file extensions.
  exts: [ 'json', 'mustache' ],
  // Print debug info
  debug: true
});

// Specify the folder to watch for file-changes.
hotServer.watch(__dirname);
```

The last piece is to inject the `livereload.js` into your HTML; the [connect-livereload module](https://github.com/intesso/connect-livereload) takes care of this; just drop it into your app before your define your routes:

```javascript
// Inject the livereload.js script tag into pages.
app.use(livereloadMiddleware());
```

Et viola, hot reloading of mustache templates and their associated data.  Full source over on [github](https://github.com/jonnyreeves/mustache-express-hotreload).
