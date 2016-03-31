Title: Testing Redux Middleware
Date: 2016-03-31 21:00
Category: JavaScript

[Redux Middleware](http://redux.js.org/docs/advanced/Middleware.html) is a very powerful concept which allows you to write your application's business logic in one place without complicating your action creators or view components - it's also really easy to isolate and test.

### Starting from Scratch
Redux middleware nearly always wants to inspect actions as they flow through on their way to the reducers; below is the starting point for a piece of middleware which can be used to repeat an action on a specified interval.  The middleware identifies actions which should be polled by looking for a `pollIntervalMs` property in the action's meta object.

```js
export const pollingMiddleware = store => next => action => {
  // extract the poll interval from the action's meta.
  const { pollIntervalMs } = action.meta || {};
  // if the action didn't specify a poll interval then bail out, passing
  // the action through to the next piece of middleware in the chain.
  if (!pollIntervalMs) {
    return next(action);
  }
  
  // insert polling logic here.
}
```

Before we go any further, let's get the ball rolling on the testing front and flesh out the following test-case:

> it should pass the action through to the next piece of middleware if it does not carry a `meta.pollIntervalMs` property.

For the rest of this tutorial I will be using the test library [QUnit v1.23](https://qunitjs.com/), although there is nothing specific to QUnit other than the syntax of the test-cases and assertions - with that out of the way, let's get started.

```js
import QUnit from 'qunit';
import pollingMiddleware from './polling-middleware.js';

QUnit.test('it should pass the action through to the next piece of middleware if it does not carry a `meta.pollIntervalMs` property', assert => {
  const nonPollingAction = { type: 'no-polling-please' };
  
  // Fake out the `store` object Redux provides, note that I'm ommitting
  // the `dispatch` and `getState` methods for brevity at this stage.
  const fakeStore = {};
  
  // Create a 'spy' function which records when it's called.
  const nextSpyCalls = [];
  const nextSpy = action => nextCalls.push(action);
  
  // Invoke our middleware with our action.
  pollingMiddleware(fakeStore)(nextSpy)(action)
  
  // perform our assertions for this test.
  assert.equal(nextSpyCalls.length, 1, 'nextSpy called once');
  assert.deepEqual(nextSpyCalls[0], action, 'action passed to next');
});
```



