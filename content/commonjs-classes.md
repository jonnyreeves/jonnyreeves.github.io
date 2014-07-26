Title: Simple JavaScript Classes in CommonJS
Date: 2014-07-26 18:00
Category: JavaScript

Having recently become an advocate of CommonJS modules and Browserify our team was looking for a simple way to define Plain old JavaScript Classes in our modules.  We've settled on the following style, making use of [extend](https://github.com/justmoon/node-extend) and [inherits](https://github.com/isaacs/inherits); two tiny, focused CommonJS modules which will add a whopping 2kb to our project when unminified.

```
"use strict";

var inherits = require("inherits");
var extend = require("extends");

// Declare the constructor and member properties.
function MyClass(foo, bar) {

  // Make a call to the Parent Class' constructor. The `_super` 
  // member is provided by the `inherits` call below and is
  // preferred to calling the `MyParentClass` constructor function
  // directly should we want to alter the inheritence.
  MyClass.super_.call(this, foo);

  // Keep things straight forward and performant by simply hinting
  // at privacy with a leading underscore.
  this._bar = bar;
}

// Establish an inheritance relationship with another Class.
inherits(MyClass, MyParentClass);

// Define static members directly on the Constructor function.
MyClass.explode = function () {
  throw new Error("KABOOM!");
};

// Declare instance methods.
extend(MyClass.prototype, {

  // Place all methods on the prototype so they're shared amongst
  // all instances.  Using `extends` in this fashion ensures that
  // the `constructor` property remains correctly pointed at the
  // `MyClass` function so `instanceof` checks work as expected.
  greet: function (someone) {

    // Make a call to the Parent Class' `greet` method.
    var greeting = MyClass.super_.prototype.greet.call(this, someone);

    return greeting + ", dude!";
  },

  // Again, just hint at privacy with a leading underscore; doing
  // so ensures you have easy access to `this` in each method.
  _throbulate: function () {
    // Implementation omitted for brevity.
  }
});

module.export = MyClass;
```