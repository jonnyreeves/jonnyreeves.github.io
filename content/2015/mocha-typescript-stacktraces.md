Title: Getting Proper Stack Traces with Mocha and TypeScript
Date: 2015-08-20 21:00
Category: TypeScript

Mocha and TypeScript are awesome when everything's working, but when you have a failing test something's not quite right:

```
$npm test

  Calculator
    #add
      1) should work


  0 passing (21ms)
  1 failing

  1) Calculator #add should work:

      AssertionError: expected 6 to equal 7
      + expected - actual

      -6
      +7

      at Context.<anonymous> (test/Calculator.spec.js:12:38)
```

The stacktrace at the end points us to the failing assertion; however the stacktrace is pointing `Calculator.spec.js` - not our TypeScript test-case.  

The TypeScript compiler (`tsc`) will generate [source maps](http://www.html5rocks.com/en/tutorials/developertools/sourcemaps/) to enable debugging the TypeScript source rather than the transpiled ES5 javascript which gets written out by the compiler.  We can enable this with the `--sourcemap` flag.

Problem is that V8 (the engine that powers Node) doesn't use these sourcemaps when generating stacktraces; [source-map-support](https://github.com/evanw/node-source-map-support) to the rescue!  We can enable it by passing `--require source-map-support/register` to `mocha`:

```
{
	"scripts": {
	  "test": "mocha --require source-map-support/register test/**/*.spec.js"
	}
}
```

Now we get an accurate stacktrace on failure :)

```
  1) Calculator #add should work:

      AssertionError: expected 6 to equal 7
      + expected - actual

      -6
      +7

      at Context.<anonymous> (test/Calculator.spec.ts:15:22)
```

Thanks to redditor [pieeta](https://www.reddit.com/user/pieeta) who tipped me off :)  I've posted the sample project up on [Github](https://github.com/jonnyreeves/mocha-typescript-stacktraces).