Title: Stubbing JavaScript Promises with SinonJS
Date: 2012-06-02 16:15
Category: JavaScript

Asynchronous code lies at the heart of front end development; in order to make your application feel responsive you can’t afford to block execution until some external data has been read. [Promises](http://wiki.commonjs.org/wiki/Promises/A) are a well understood design pattern to help encapsulate the state of an asynchronous action. A Promise will only ever transfer from a pending state (ie: when the initial request has been made to the server) to a resolved state. The resolved state can be one of either a failure state (ie: the server sends back a 500 error) or a success state (ie: the JSON data you were expecting has come back). Once a promise has transferred to a resolved state it will not change (it becomes immutable). By employing this pattern you can write some very succinct code which is both easy to read and maintain:

```js
service.fetch("someData")
	.then(function (response) { /* process response */ });
	.otherwise(function (error) { /* handle the error */ });
```

The code above makes use of Brain Cavalier’s [when.js](https://github.com/cujojs/when) Promises implementation. The rest of this post aims to highlight how you can combine when.js with a mocking framework to make unit testing Promises a piece of cake. If you would still like to learn more about using Promises, and how they make writing asynchronous code easier, then I’d suggest reading [his excellent articles on the subject](http://blog.briancavalier.com/async-programming-part-1-its-messy).

### Why mock Promises?

One of the golden rules of unit testing is that the [code under test must be deterministic](http://martinfowler.com/articles/nonDeterminism.html). Another golden rule is that [unit tests must be fast to execute](http://pragprog.com/magazines/2012-01/unit-tests-are-first). Although Promises make writing asynchronous code easier, they don’t help with the two points above, take the following example:

```js
// Example of a module that abstracts a RESTful web service.
var service = {
	fetch: function (query) {
		// Returns a when.js Promise which will resolve when the data
		// has been fetched.
		return when(jQuery.get("http://myservice.com/api?q=" + query));
	}
};

// A client object which consumes the Service, this is what we are going to be 
// unit testing.
var client = {
	
	// Returns a promise which will yield the number of pages returned
	// the supplied query.
	getNumPages: function (query) {
		
		// Create a fresh service instance.
		var service = createService();
		
		// Return a promise which will resolve after the following
		// `then` block has performed.
		return service.fetch(query)
			.then(function (response) { 
			
				// Modifies the result of the Service's Promise,
				// future success handlers will reicieve the
				// number of pages instead of the response data.
				return JSON.parse(response).pages.length;
			});
	}
}
```

Unit testing the above client is pretty easy; a simple test-case could look like this (This example will be based on QUnit):

```js
asyncTest("getNumPages fetches expected number of pages", function () { 
	
	// A special query which we know will return the expected number of pages.
	client.getNumPages("testcase-query")
		.then(function (numPages) { 
			equal(numPages, 5, "5 pages returned");
			start();
		});
});
```

Although the above test case is easy to read, it doesn’t make for a very good unit test for the following reasons:

* It’s non-deterministic – if the server over at myservice.com is down, or you try and execute these unit tests offline then the test will fail (infact, it will hang the test-runner as it waits for this asyncTest to complete.)
* It’s not going to be fast – a connection needs to be established to the server.
* It only tests the success state – we need to test what happens if the service is down, but there’s no obvious way to do that (other than to request an invalid query value from the API.

This is where a mocking framework comes in – it will help us solve all three of the problems listed above.

### Promises, Lies and stubbing the truth

A mocking framework allows you to alter the way functions behave during a unit test. Mocking frameworks are especially powerful in dynamic languages, like JavaScript, as they are able to make large changes to your codebase for a given unit test and then restore all those changes immediately after the test completes. This tutorial is going to be looking at [SinonJS](http://sinonjs.org/)

As mentioned above, Sinon.js is able to completely rewrite a function during a test-case, let’s revisit our service module above:

```js
test("Sinon.js stubbing example", function () {
	// Use sinon.js to redefine the `service.fetch` function.
	sinon.stub(service, 'fetch').returns("Hello!");
	
	// Now when we call it, instead of invoking `jQuery.get`, it returns a String.
	equal(service.fetch("testcase-data"), "Hello!");
});
```

The above example isn’t very useful; however, instead of returning a String, we can just as easily return a Promise instance, and that’s when things start getting useful:

```js
test("Stubbing the service so it returns an expected response", function () { 
    
	// Stub the service so it returns a resolved promise.  Note that `when(value)`
	// is a neat short-cut for creating a Deferred and resolving it.
	var expectedResponse = '{ "pages": [ "page1", "page2", "page3" ]}';
	sinon.stub(service, 'fetch').returns(when(expectedResponse));
    
	// Call the client...
	client.getNumPages('testcase-query')
		.then(function (numPages) { 
			strictEqual(numPages, 3, "3 pages returned");
		});
});
```

Note that the above test-case didn’t need to make user of QUnits `asyncTest` block – that’s because the expectedPromise Promise object has already been resolved – no need to wait for anything to complete asynchronously. Our test is no longer reliant on the server (hence deterministic) and it no longer relies on a service call (and will therefore execute almost instantly). That leaves only one last point from our rules above – how to test the failure path…

```js
test("Simulating a service failure", function () { 
	
	// Again, start by stubbing our service's fetch method.  This time we will
	// return a rejected Promise with an error.
	var expectedError = new Error("Bad Query");
	sinon.stub(service, 'fetch').returns(when.reject(expectedError));
	
	// Call the client and expect it to fail
	client.getNumPages('testcase-query')
		.otherwise(function (error) { 
			strictEqual(error, expectedError, "Error from API provided to handler");
		});
});
```

Hopefully this post has been useful in highlight just a couple of the ways in which Promises and a mocking framework can be combined to remove both non-determinism, and slow execution speed from your tests as well as making it easy to test all paths of your code, even if they depend on external data. I’ve created [a gist which shows a few other techniques](https://gist.github.com/2858452) which can be employed for unit testing Promises including the use of Sinon’s yieldTo method which makes it easy to resolve, or reject a Promise resolver supplied as an argument.