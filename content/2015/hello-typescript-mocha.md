Title: Hello Typescript and Mocha!
Date: 2015-07-27 20:00
Category: TypeScript

Let's see what we can do with TypeScript then.  First things first we  need to create a local project to hack on:

```text
$ npm init
name: (hello-ts-mocha)
version: (1.0.0)
description: Getting started with TypeScript and mocha
entry point: (index.js)
test command: mocha
git repository:
keywords:
license: (ISC)
```

Now let's grab the TypeScript compiler so we can build the project:

	npm install typescript --save

Now let's grab Mocha for our tests

	npm install mocha --save-dev

## Create a Subject to Test
Time to create our subject that we're going to test, let's do some TDD (:  Create a new file, `index.ts` in the project root

```typescript
export default class Calculator {
	add(x : number, y : number) : number {
		return 0;
	}
}
```

And now to compile this down to ES5 so we can execute it under node:

	./node_modules/typescript/bin/tsc index.ts --module commonjs 

We can simplify the compilation step by adding a prepublish [npm script](https://docs.npmjs.com/misc/scripts) to the `package.json` file:

	{
		...
		"scripts": {
			"prepublish": "tsc index.ts --module commonjs ",
			"test": "mocha"
		}
		...
	}

We can now compile with `npm install`.

## Adding a Test
Let's create our first test; following convention lets create our test-case in `test/CalculatorTest`.

Before writing the test-case we need to grab the Mocha Type Definitions (requried for the TypeScript compiler (`tsc`) to work).  Easiest way to get these it to use the DefinitelyTyped TypeScript Definition manager (`tsd`).

	npm install tsd -g

Once installed we can use it to grab mocha's type definitions:

	tsd install mocha --save

This will add a `typings/` folder to our project.  Here's what our source tree looks like so far:

```text
hello-ts-mocha
├── index.ts
├── node_modules
│   └── typescript
├── package.json
├── test
│   └── CalculatorTest.js
├── tsd.json
└── typings
    ├── mocha
    └── tsd.d.ts
```

Now we can reference the mocha type definition using a `/// <reference />` comment:

```typescript
/// <reference path="../typings/mocha/mocha.d.ts" />
import Calculator from '../index';

describe('Calculator', () => {
	var subject : Calculator;

	beforeEach(function () {
		subject = new Calculator();
	});

	describe('#add', () => {
		it('should add two numbers together', () => {
			var result : number = subject.add(2, 3);
			if (result !== 5) {
				throw new Error('Expected 2 + 3 = 5 but was ' + result);
			}
		});
	});
});
```

Before we can run the tests we need to compile them, best way to do this is to add a `preTest` NPM script to invoke the typscript compiler before running mocha. Open up the `package.json` file again:

	{
		...
		"scripts": {
	    	"pretest": "tsc test/*Test.ts --module commonjs",
		    "test": "mocha"
		}
	}

We can now run our test-case with `npm test`:

```text
$ npm test
> ts-mocha@1.0.0 pretest /private/tmp/foo
> tsc test/*Test.ts --module commonjs

> ts-mocha@1.0.0 test /private/tmp/foo
> mocha

  Calculator
    #add
      1) should add two numbers together


  0 passing (19ms)
  1 failing

  1) Calculator #add should add two numbers together:
     Error: Expected 2 + 3 = 5 but was 0
      at Context.<anonymous> (test/CalculatorTest.js:12:23)
```

Have fun fixing the test-case :)  Full source over over at [github.com/jonnyreeves/hello-ts-mocha](https://github.com/jonnyreeves/hello-ts-mocha)