Title: Redux Middleware
Date: 2016-05-28 20:00
Category: JavaScript, Talks

This is a supporting post for the talk I am giving at [Moo Tech Tuesday on the 31st May](http://eventbrite.co.uk/e/the-new-shiny-javascript-development-in-2016-tickets-25196915653) where I will be presenting an introduction to Redux Middleware [[slide deck]](https://docs.google.com/a/jonnyreeves.co.uk/presentation/d/1I0s4uCWo7yEU3pLf4R5UjxiCqC3FhFJSSunWq0WAxZI/edit?usp=sharing) with advice on how to test it.  The supporting code can be found over on [Github](https://github.com/jonnyreeves/redux-button-masher-example).

Redux describes itself as a Predictable State Container for JavaScript applications; it's a lightweight (~5kb) framework which has a couple of major benefits:

1. It encourages predictable state change through immutable design.
2. It makes it easy to isolate (and therefore test) components in the system.

This blog post will be exploring a simple Redux application which will then be extended to provide additional functionality implemented as Redux Middleware.  I will also be demonstrating how it's easy to write test-cases for Redux Middleware.

### Redux vs Traditional MVC
Redux's architecture was inspired by the [Elm Architecture](http://guide.elm-lang.org/architecture/index.html) and differs from traditional MVC in the way it enforces a strict uni-direction flow (or cycle) of data from the View-tier to the Model and back again.  

![MVC architecture](/images/2016/redux-middleware/mvc-architecture.png)

In traditional MVC based systems you will often find a stateful controller object which has both the Models and the Views injected into it.  The controller will be responsible for fetching data from the models and passing that data through to the views for rendering; as well as binding to events from the view tier as the user interacts with the application.  Depending on the exact MVC implementation the Controller may also be responsible for handling API calls and other custom business logic.  As a result of all these responsibilities and dependencies, Controllers can typically be difficult to bring under test.  Some MVC implementations can compound this problem further by introducing two-way data binding where the Controller is essentially side-stepped and the view and model are injected into each other.  IMHO this is a classic case for [Simple over Easy](https://www.infoq.com/presentations/Simple-Made-Easy) and should be avoided for long-term maintainability of software.

![Redux architecture](/images/2016/redux-middleware/redux-architecture.png)

In contrast to MVC implementations, Redux does not require a centralised Controller, instead an application boils down to two tiers: The Store (which holds a reference to the single state object, aka atom) and Views.  

The view-tier has read-only access to the Store's state object; if it wishes to change the Store's state it must first dispatch an action object to the Store which will be processed by the reducer function.  Redux provides a `dispatch` function which takes a single argument: an Action object whose interface enforces a `type` property.

The Store's state is modified by a Reducer function.  The Reducer is a [pure function](https://en.wikipedia.org/wiki/Pure_function) which takes the current state object, and the action object, returning a the new state object.  If the action does not result in a state-change, the reducer can return the current state object.  These components are wrapped in Redux's `store` object which manages the single state object and has a subscription mechanism (`store.subscribe`) to notify other parts of the system when the state object has changed.  Note that the state object is immutable, instead of being modified in place, the entire object is replaced with a new one when a change occurs.

This form of loose coupling and one-way data flow is what makes Redux applications both easy to predict and easy to test.

Note that whilst Redux is typically partnered with React, it does not have a dependency on it and can just as easily be paired with [Vue.js](https://vuejs.org/) or [plain old DOM manipulation](https://github.com/reactjs/redux/blob/67f9dcca8b359825f1a89b318d2f879f99221032/examples/counter-vanilla/index.html) methods with no other dependencies.

### Keeping Count
The rest of this post will be dedicated to extending a simple application.  The consists of a single React view component that offers a counter and two buttons.  Users are able to manipulate the counter by pressing the increment and decrement buttons.

```js
const Counter = props => {
  const { count, dispatch } = props;
  return (
    <div>
      <p>Counter value: {props.value}</p>
      <button onClick={() => dispatch({ type: 'INC' })}>++</button>
      <button onClick={() => dispatch({ type: 'DEC' })}>--</button>
    </div>
  );
}
export default connect(state => state)(Counter);
```

The Counter component is connected to the Redux framework via the `connect` method which wraps the Counter component with a state-mapping function (`state => state`) - in this case we are simple accepting the `state` object from the Redux store with no changes.  As a side-effect of being connected, the component also receives the `dispatch` function in its properties as well as the properties contained in the store's `state` object. (in this case, just `count`).

Each button invokes `dispatch` when clicked which creates a new action object with a type property of either 'INC' or 'DEC' based on how we want the counter's value to be mutated.

```js
const initialState = { value: 0 };
function reducer(state = initialState, action) {
    switch (action.type) {
    case 'INC':
      return { ...state, value: state.value + 1 };
    case 'DEC':
      return { ...state, value: state.value - 1 };
    default:
      return state
    }
}
```

Next we have the reducer function for the application; here we simply switch on the incoming `action` object and return a new `state` value.  Redux will automatically invoke your reducer function with the current `state` object whenever `dispatch` is called.  Returning a new object (as is the case for both `INC` and `DEC` cases), will cause Redux to re-render the view tier thereby updating the counter's value on screen.

### Bringing Back the Controller
So far our same application has been very simple and has not introduced side-effects.  [Side-effect](https://en.wikipedia.org/wiki/Side_effect_%28computer_science%29) is the term used when a function modifies some state elsewhere in the system, or interacts with the outside world (ie: makes an API call).  Managing side-effects effectively is key to ensuring that your application stays both predictable and easy to bring under test as functions with side-effects require the reader to understand knowledge about the wider system's context and the system's state prior to the call.  Redux provides a simple yet powerful mechanism for managing side-effects: Middleware.

![](/images/2016/redux-middleware/redux-with-middleware.png)

Redux Middleware sits between the view-tier and the reducers giving you a hook to invoke asynchronous business logic after each action has been dispatched.  Middleware is used to enhance a store when it is created through the `applyMiddleware` function provided by Redux:

```js
const reduxStore = createStore(
  reducer,
  applyMiddleware(myMiddleware, someOtherMiddleware),
);
```

The Redux Middleware signature can look a little daunting at first with three nested functions required:

```js
const myMiddleware = function (store) {
  return function (next) {
    return function (action) {
      /* middleware logic */
      return next(action);
    }
  }
}
```

The three functions are invoked right to left with the inner most function called first.  These three functions each provide an essential role to your middleware:

1. The inner most function is invoked with the intercepted action - this is where your middleware's business logic will go.
2. The middle function receives a reference to the `next` piece of middleware in the chain - your middleware must invoke `next` otherwise the intercepted action will not be reduced and the app will essentially hang.
3. The outer most function receives a reference to the Redux Store API which can be used to get the current state object and dispatch new actions from your middleware.

ES6 arrow functions allow us to write this mass of functions slightly more succinctly:

```js
store => next => action => {
  /* middleware logic */
  return next(action);
}
```

Okay, let's start getting a bit more concrete and implement the first piece of code for some custom middleware:

```js
const reportMiddleware = store => next => action => {
  // Pass all actions to the next piece of middleware
  // (or the reducer if there is no other middleware).
  return next(action);
}
```

The `reportMiddleware` will intercept all actions after they've been dispatched.  As per the user story, we only want to track 'INC' actions.  Regardless of the type of action we must always pass the action through to `next` otherwise it will not be reduced and the app will no longer update when the user clicks on the buttons.

### Adding a Testing Framework
As mentioned at the start of the article, one of the main benefits of redux is the ease of testability - this is especially true for Redux Middleware which can be used to express complex business logic which remaining trivial to test.  In the follow examples I will be using a combination of Mocha, Chai, SinonJS.

Let's start by writing a test which ensures that the intercepted action is always passed the the `next` function.

```js
it('should pass the intercepted action to next', () => {
  const nextArgs = [];
  const fakeNext = (...args) => { nextArgs.push(args); };
  const fakeStore = {};

  const action = { type: 'INC' };
  reportMiddleware(fakeStore)(fakeNext)(action);

  assert.deepEqual(fakeNext.args[0], [action], 'action passed to next');
});
```

Working backwards, we want to assert that the `next` function was called with a given `action` object.

To implement this we need to instantiate an action and then pass it through to our `reportMiddleware` invoking each one of the three methods in order replacing both the store, and next arguments with fake counterparts.

The `fakeStore` is nothing but an empty object (as our API doesn't actually interact with the store API) - however the `fakeNext` is slightly more complex providing a function which records the arguments it was called with storing them in the `args` property on itself.

The apparatus in the test-case can be simplified by using Sinon.  Sinon provides a [Spy API](http://sinonjs.org/docs/#spies) which provides instrumented functions which records how they were called and can be used to write expressive assertions:

```js
it('should pass the intercepted action to next', () => {
  const fakeStore = {};
  const fakeNext = sinon.spy();

  const action = { type: 'INC' };
  reportMiddleware(fakeStore)(fakeNext)(action);

  assert.ok(next.withArgs(action).calledOnce,
    'action passed to next, once');
}
```

If you are new to SinonJS, then you may also be interested to learn of the [Stub API](http://sinonjs.org/docs/#stubs) which allows you to program the return value of functions, including those attached to existing objects (eg: `jQuery.ajax`).

### It's Business Time
Now we've introduced the core concepts of testing middleware, lets complete this example by implementing a User Story:

> As the product manager I would like to know when users have clicked the increment button 5 times for reporting.

This requirement means that we have to observe the number of times the increment button is clicked.  We could model this state in the view-tier, however that could result in the logic being hard to isolate and test - likewise we could push it into the Store's state, however this will make our core domain model more complex and potentially harder to reason about - I feel Middleware is a good fit for this type of problem.

```js
export function newReportMiddleware() {
  let numIncActions = 0;
  return store => next => action => {
    if (action.type === 'INC') {
      numIncActions += 1;
    }
    // Pass all actions to the next piece of middleware
    // (or the reducer if there is no other middleware).
    return next(action);
  }
}
```

We start by wrapping everything in yet another function: `newReportMiddleware`.  This function acts as a factory and its closure is used to encapsulate the report middleware's state.  This makes it possible to have multiple instances of the same middleware in use at once, but it also makes unit testing much easier as we can guarantee that all state will be reset between tests.

Our business logic is simple, each time we see an `INC` action we increment the middleware's internal count of INC actions by one.  Next we introduce the logic for detecting when 5 INC actions have been intercepted:

```js
export function newReportMiddleware() {
    let numIncActions = 0;
    return store => next => action => {
        if (action.type === 'INC') {
            numIncActions += 1;
            if ((numIncActions % 5) === 0) {
                alert('INC dispatched 5 times');
            }
        }
        return next(action);
    }
}
```

Great, now we get an alert dialog after every 5 clicks of the increment button; however this isn't very easy to test (and i doubt the author of the User Story had an alert box in mind...) - instead we can leverage our `newReportMiddleware` factory function again and use it to supply a configuration object with both a callback function to invoke and a target count value to mod by.

```js
export function newReportMiddleware({ callback, target }) {
    let numIncActions = 0;
    return store => next => action => {
        if (action.type === 'INC') {
            numIncActions += 1;
            if ((numIncActions % target) === 0) {
                callback(`INC dispatched ${target} times`);
            }
        }
        return next(action);
    }
}
```

With an arguments object in place we can now write a simple test to ensure that the supplied callback is invoked after a given number of INC actions have been intercepted:

```js
it('should callback after N INC actions', () => {
  const next = sinon.spy();
  const callback = sinon.spy();
  const middleware = newReportMiddleware({ callback, target: 2 });

  middleware({})(next)({ type: 'INC' });
  middleware({})(next)({ type: 'DEC' });
  assert.ok(callback.notCalled, 'after 1 INC, 1 DEC');

  middleware({})(next)({ type: 'INC' });
  assert.ok(callback.calledOnce, 'after 2 INC, 1 DEC');
});
```

We use sinon to setup spies for both the Redux Middleware API's `next` function and our own `reportMiddleware`'s `callback` function.  It's worth noting that `sinon.spy()` returns a normal function which can be used interchangeably.

Next we send two actions through our middleware, an `INC` and a `DEC`.  At this point the middleware's `numIncActions` value should be `1`, which is not equal to the target value of `2`, therefore the callback should not have been invoked yet.  This type of assertion acts as a safety net and can make debugging failing tests much easier.

Finally we throw one last `INC` action through, we can now check our business logic was implemented correctly and the callback invoked.

### Middleware Everywhere!
![Middleware, Middleware Everywhere](/images/2016/redux-middleware/middleware-everywhere-meme.jpg)

This post has hopefully shown how Redux Middleware provides a simple abstraction which makes it possible to write complex logic that is both predictable and easy to test.  In my day-job we make extensive use of middleware to model all of our application's side effects including XHRs, analytics and multi-stage API calls.  If you find yourself getting tired of writing middleware boilerplate you may be interested in taking a look at Redux Saga's which make use of ES7 generator functions to provide a psuedo-blocking API for your side-effect management

```js
export function* incrementAsync() {
 yield delay(1000);
 yield put({ type: 'INC' });
}

export function* watchIncrementAsync() {
 yield* takeEvery('INC_ASYNC', incrementAsync);
}
```
