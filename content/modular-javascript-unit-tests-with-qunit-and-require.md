Modular application development is essential when working on a large project with more than a handful of developers. Breaking your code into separate modules improves code legibility and organization making it easier to locate logic and help create ‘seams’ in your code so you can do your best to adhere to [Single Responsibility Principle](http://www.codinghorror.com/blog/2007/03/curlys-law-do-one-thing.html). This is all well and good for your application code, but what about the Unit Tests which support it – how can we decompose these tests into modules so they’re well organized and easy to find?

### Test Case Structure

First things first, you need to get your Unit Tests broken up into separate test cases. QUnit provides the QUnit.module method which takes care of this, allowing your to group tests in the QUnit test runner. We can extend this metaphor further by ensuring that each QUnit module resides in its own file, or, in other words – each application module has it’s own QUnit module of tests.

Here’s an example of a simple QUnit Test Case defined as a RequireJS module:

```js
define(function (require) {

    // Import depdendencies (note you can use relative paths here)
    var PegiRatings = require("./PegiRatings");

    // Define the QUnit module and lifecycle.
    QUnit.module("example/model/PegiRatings");

    QUnit.test("isSuitibleFor - younger age supplied, returns false", function () { 
        QUnit.equal(PegiRatings.PEGI_18.isSuitibleFor(17), false);
    });

    QUnit.test("isSuitibleFor - same age supplied, returns true", function () { 
        QUnit.equal(PegiRatings.PEGI_18.isSuitibleFor(18), true);
    });

    QUnit.test("isSuitibleFor - older age supplied, returns true", function () { 
        QUnit.equal(PegiRatings.PEGI_18.isSuitibleFor(19), true);
    });
});
```

As you can see above, we are able to use `require` to import other modules from the src folder into the test case (in the above example we are including the PegiRatings object, which just happens to be the module under test). Here’s another example where we pull in not only other modules from the source tree, but also a vendor library (the ever popular, underscore.js):

```js
define(function (require) {

    // Import depdendencies.
    var _ = require("vendor/underscore");
    var Player = require("./Player");
    var Game = require("./Game");
    var PegiRatings = require("./PegiRatings");

    // ... rest of test case omitted for brevity

});
```

### Configuring QUnit and RequireJS

Now that we have our unit tests split out into separate modules, we need to configure the QUnit Test Runner so that it will work with RequireJS to resolve the dependencies. The first step is to modify the stock QUnit Test Runner HTML document so RequireJS is loaded along with all our testcases.

```html
<!DOCTYPE html>
<html>
    <head>
        <title>Example Test Runner</title>
        <link rel="stylesheet" href="vendor/qunit.css" />

        <!-- QUnit includes -->
        <script src="vendor/qunit.js"></script>

        <!-- Load RequireJS & the testsuite -->
        <script src="../src/require-config.js"></script>
        <script src="../src/vendor/require.js" data-main="testsuite.js"></script>
    </head>
    <body>
        <div id="qunit"></div>
    </body>
</html>
```

In a typical QUnit Test Runner setup you would include your `tests.js` file which included all your QUnit tests. Instead we load the project’s [RequireJS configuration file](http://requirejs.org/docs/api.html#config) (which is also used by the main project, to avoid duplication of configuration settings between the tests and the build) and then RequireJS itself with a callback to the `testsuite.js` file.

```js
(function () {

    // Defer Qunit so RequireJS can work its magic and resolve all modules.
    QUnit.config.autostart = false;

    // Configure RequireJS so it resolves relative module paths from the `src`
    // folder.
    require.config({
        baseUrl: "../src",
    });

    // A list of all QUnit test Modules.  Make sure you include the `.js` 
    // extension so RequireJS resolves them as relative paths rather than using
    // the `baseUrl` value supplied above.
    var testModules = [
        "example/model/PlayerTests.js",
        "example/model/PegiRatingsTests.js"
    ];

    // Resolve all testModules and then start the Test Runner.
    require(testModules, QUnit.start);
}());
```

This file configures RequireJS ready for our Unit Test run and also provides a list of all test cases that we wish to execute. Once RequireJS has finished loading all the test cases, it makes a call to `QUnit.start` which kicks off the Test Runner.

### Example Project Download

I’ve pushed all the source for this example project to the [qunit-require GitHub Repo](https://github.com/jonnyreeves/qunit-require/). You can [download the zipball](https://github.com/jonnyreeves/qunit-require/zipball/master) and run the tests to gain a better understanding of the project structure.