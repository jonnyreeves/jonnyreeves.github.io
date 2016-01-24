Title: Mocking XMLHttpRequests in Jasmine
Date: 2015-10-19 21:00
Category: javascript

When writing integration tests, it's often useful to fake network requests so your tests can be predictable and execute quickly.  Jasmine provides [`jasmine-ajax`](https://github.com/jasmine/jasmine-ajax) which will replace the `XMLHttpRequest` constructor on the global (eg: `window`).

Wiring up jasmine.Ajax into your test-suites' lifecycle is pretty straight forward:

```javascript
import 'jasmine-ajax';

describe('myTestSuite', () => {
  beforeEach(() => jasmine.Ajax.install());
  afterEach(() => jasmine.Ajax.uninstall());
});
```

As per the [docs](http://jasmine.github.io/2.0/ajax.html), you can then pre-program responses before your subject under test makes them:

```javascript
jasmine.Ajax.stubRequest('http://example.org/api')
  .andReturn({ responseText: JSON.stringify({ json: 'ok!' }) });
```

jasmine-ajax executes all XHR callbacks on the same tick making them effectivly syncronous.  This results in your test-code much easier to write and reason about.

### Pairing with `xhr`
`XMLHttpRequest` doesn't have the nicest API to work with; fortunatley the [`xhr`](https://github.com/Raynos/xhr) module on NPM provides a nice, lightweight abstraction (it even smooths out the cracks in IE8).  However, it's not all plain sailing as the xhr module caches the `XMLHttpRequest` object on the window when it is loaded (ie: `require()`'d).

```javascript
module.exports.XMLHttpRequest = window.XMLHttpRequest;
```

This results in requests made using the `xhr` module ignorning the fake `XMLHttpRequest` constructor that `jasmine-ajax` has placed on the window.  Fortunatley there's an easy fix, just re-assign `xhr.XMLHttpRequest` after you've installed jasmine-ajax:

```javascript
import 'jasmine-ajax';
import xhr from 'xhr';

describe('myTestSuite', () => {
  beforeEach(() => {
    jasmine.Ajax.install();
    xhr.XMLHttpRequest = window.XMLHttpRequest;
  });
  afterEach(() => {
    jasmine.Ajax.uninstall();
    xhr.XMLHttpRequest = window.XMLHttpRequest;
  });
});
```

### Closing thoughts on Jasmine
I've recently switched to Jasmine after using Mocha and SinonJS succesfully for a few years.  My hope was that the Jasmine ecosystem, which has a lot of funtionality built-in, would be more productive and easier for new-comers to the project to pick up than Mocha.  I've been very impressed by how easy it was to get up and running on Jasmine; and the v2.3 API is pleasant to code against (it will be instantly familiar to [chai](http://chaijs.com/guide/installation/) users), however I do wish that Jasmine made it easier to write custom matchers as I find myself missing the verbosity of SinonJS's `sinon.match(val => { ... })`.
