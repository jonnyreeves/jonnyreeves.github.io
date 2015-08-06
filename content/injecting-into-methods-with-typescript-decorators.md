Title: Injecting into Methods with TypeScript Decorators
Date: 2015-08-03 21:00
Category: TypeScript

Expanding upon my [last post on Property based Dependency Injection](http://localhost:8000/2015/basic-typescript-dependency-injection-with-decorators/), let's have a look at what we need to do in order to inject into methods - here's what we want to achieve:

```typescript
class Person {
  private _firstName : string;
  private _lastName : string;

  @inject('firstName', 'lastName')
  setName(first : string, last : string) {
    this._firstName = first;
    this._last = last;
  }

  getFullName() : string {
    return `${firstName} ${lastName}`
  }
}
```

Here we are decorating the `Person#setName()` method with the `@inject` decorator and requesting the values mapped against the 'firstName' and 'lastName' injection keys from the Dependency Container - our test case would look something like this:

```typescript
// Setup the container
injector.map('firstName', 'Jonny');
injector.map('lastName', 'Reeves');

// Instantiate a Person, the container will apply the injections.
const jonny = injector.instantiate(Person);

// Test it worked.
if (jonny.getFullName() !== 'Jonny Reeves') {
	throw new Error('expected jonny.getFullName() to be Jonny Reeves but was ' + jonny.getFullName());
}
```

First of all we need to modify our `@inject` decorator, originally it only expected a single argument (the `injectionKey`), as methods can take more than one argument we need to make use of [rest parameters]() to accept any number of strings:

```typescript
function inject(...injectionKeys : Array<string>) { ... }
```

We face a slightly tricker challenge in the fact that injecting values into methods requires us to inoke a method rather than just assinging a property on the target object, in the previous implementation the `__inject__` Object was a simple hash of property name to injectionKey, but in order to inovoke the target method with the injection values in the correct scope we will need access to the target object as well.  To group this data together I've created an `InjectionPoint` object and assign this as the new value in the `__inject__` map:

```typescript
function inject(...injectionKeys : Array<string>) { 
  return function recordInjection(target : Object, decoratedPropertyName : string) : void {
    /* ... */

    targetType.__inject__[decoratedPropertyName] = new InjectionPoint(
                                        target, decoratedPropertyName, injectionKeys);
  }
}
```

Now we're storing the `InjectionPoint` data we need to modify `Injector#instantiate()` to make use of it when invoked.  The first change is driven by the fact the target Class' `__inject__` property is a hash of propertyNames to `InjectionPoint`'s and that an `InjectionPoint` provides one or more injectionKeys (before it was a hash of propertyNames to a single injectionKey), `Injector#getInjectionValues()` makes light work of this returning a collection of values to be injected:

```typescript
class Injector {
  /* ... */

  private getInjectionValues(injectionPoint : InjectionPoint) : Array<any> {
    return injectionPoint.injectionKeys
      .map(key => this.valuesByInjectionKey[key]);
  }
}
```

Now we need to determine how these values should be injected (either via a property of the target object, or by invoking a method of the target object).  Seeing as the `InjectionPoint` has all the knowledge it needs to perform the correct injection I employed the [Hollywood Principle](http://c2.com/cgi/wiki?HollywoodPrinciple) and added an `InjectionPoint#inject()` method which the `Injector` invokes:

```typescript
class InjectionPoint {
  /* ... */

  inject(values : Array<any>) : void {
    if (typeof this._target[this._decoratedPropertyName] === 'function') {
      this._target[this._decoratedPropertyName].apply(this._target, values);
    }
    else {
   	  // Property injection can only use the first value.
      this._target[this._decoratedPropertyName] = values[0];
    }
  }
}
```

As before, the code and unit tests can be found over at [github.com/jonnyreeves/ts-prop-injection](https://github.com/jonnyreeves/ts-prop-injection/tree/02-method-injection) - I've also raised a pull request on the repo to highlight the changes: [github.com/jonnyreeves/ts-prop-injection/pull/1](https://github.com/jonnyreeves/ts-prop-injection/pull/1).