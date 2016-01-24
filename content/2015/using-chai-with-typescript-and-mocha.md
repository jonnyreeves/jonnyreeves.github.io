Title: Using Chai with TypeScript and Mocha
Date: 2015-08-14 07:00
Category: TypeScript

Continuing my work on [Decorator-drive dependency injection in Typescript](/2015/injecting-into-constructors-with-typescript-decorators/) I've overhauled the tests by replacing the manual assertions with [chai](http://chaijs.com/).  Chai provides a fluent api for writing descriptive assertions - there are a couple of different flavours, personally I feel the [`expect`](http://chaijs.com/guide/styles/) style pairs well with TypeScript as I'm not a fan of extending `Object.prototype`.

Installation is straight forward. First install `chai` as a dev dependency:

```
npm install chai --save-dev
```

Next grab the `d.ts` file for chai via [`tsd`](http://definitelytyped.org/tsd/) to obtain the type definitions.

```
tsd install chai --save
```

You can now start refactoring your test cases; given the following simple mocha test-case:

```
describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc : Calculator = new Calculator();

    // Manual assertion.
    if (calc.add(5, 3) !== 8) {
      throw new Error('expected 5 + 3 to equal 8');
    }
  });
});
```

We can leverage chai's expect method to perform the assertion:

```
import { expect } from 'chai';

describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc : Calculator = new Calculator();
    
    // Chai assertion.
    expect(calc.add(5, 3)).to.equal(8);
  });
});
```

When running the tests, chai will provide a useful error message should the assertion fail:

```
1 failing

  1) Calculator should add two numbers:

      AssertionError: expected 6 to equal 8
      + expected - actual

      -8
      +6
      
      at Context.<anonymous> (test/Calculator.spec.js:26:45)
```

Check out [this pull request](https://github.com/jonnyreeves/ts-prop-injection/pull/3) which highlights how I integrated chai into the ts-prop-inject project.