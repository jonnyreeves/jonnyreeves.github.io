Title: Basic Typescript Dependency Injection with Decorators
Date: 2015-08-01 21:00
Category: TypeScript

Typescript 1.5 [introduced decorators](https://github.com/Microsoft/TypeScript/wiki/What's-new-in-TypeScript#decorators) to the language which lets us experiment with [meta-programming](https://en.wikipedia.org/wiki/Metaprogramming). Metadata driven Dependency Injection frameworks allow you to write highly decoupled units which are easy to test and switch out between projects / frameworks.  Let's see how we can use decorators to get some simple property injection working with TypeScript.

Let's start with an example of what we want to achieve:

```typescript
class LoginService {
  userModel : UserModel;
  performLogin() : void {
    if (!this.userModel.isLoggedIn()) {
      // ... implementation omitted...
    }
  }
```

Here our `LoginService` wants to check if our user is logged in before doing anything; as a result we need to provide a reference to the `UserModel` before invoking `LoginService#performLogin()`, we can do this manually:

```typescript
const myUserModel = new UserModel();
const myLoginService = new LoginService();

// Manually inject the dependency before using the Service.
myLoginService.userModel = myUserModel;
myLoginService.performLogin();
```

We can use a decorator to record the fact that `LoginService` has a dependency on `UserModel`:

```typescript
class LoginService {
  @inject('UserModel')
  userModel : UserModel
```

Now we need to implement our `@inject` decorator, the contract requires us to export a factory function (ie: a function which returns a function) - this factory function will be invoked each time a new instance of the supplied Class is constructed giving us a chance to modify the behavior of the program at run-time.

```typescript
function inject(injectionKey : string) {

    // Our decorator provides a factory function which will be invoked with an
    // instance of the decorated Class and the name of the decorated property.
    return function recordInjection(target : Object, decoratedPropertyName : string) : void {

        // Get a reference to the Class of the target object which has been
        // decorated.
        const targetType : { __inject__?: Object } = target.constructor;

        if (!targetType.hasOwnProperty('__inject__')) {
            targetType.__inject__ = {};
        }

        // Associate this property with the injectionKey provided in the 
        // decorator call
        targetType.__inject__[decoratedPropertyName] = injectionKey;
    };
}
```

Now we need somewhere to record injection mappings so we have values to inject into decorated properties:

```typescript
class Injector {
    private valuesByInjectionKey : { [ injectionKey : string ] : any } = {};

    /**
     * Associate an injectionKey with a value so that the supplied value can be 
     * injected into properties of the target Class decorated with the `@inject` 
     * decorator.
     *
     * @param {string} injectionKey
     * @param {*} value
     */
    map(injectionKey : string, value : any) : void {
        this.valuesByInjectionKey[injectionKey] = value;
    }
}
```

Continuing our original example we would map the injectionKey `UserModel` to the instance of `UserModel` that we want injected, eg:

```typescript
const injector = new Injector();
injector.mapValue('UserModel', new UserModel());
```

Finally we need to introduce a factory function which will instantiate a class but also fulfill injections based on mappings in the Injector - to enable this we add an `#instantiate()` method to `Injector`.

```typescript
class Injector {
    /**
     * Create a new instance of the supplied Class fulfilling any property 
     * injections which are present in the injectionRules map.
     */
    instantiate<T>(Class : { new(...args: any[]) : T }) : T {
        // Start by creating a new instance of the target Class.
        const instance : any = new Class();

        // Loop through all properties decorated with `@inject()` in this Class and
        // try to satisfy them if there is a mapped value.
        for (let injectionPoint of this.getInjectionPoints(Class)) {
            const injectionValue : any = this.valuesByInjectionKey[injectionPoint.injectionKey];

            // Perform the injection if we have a value assigned to this injectionKey.
            if (injectionValue) {
                instance[injectionPoint.propertyName] = injectionValue;
            }
        }

        return instance;
    }

    private getInjectionPoints<T>(Class : { __inject__?: { [ prop : string ] : string } }) : Array<InjectionPoint> {
        var result : Array<InjectionPoint> = [];

        // Retrieve the `__inject__` hash created by the @inject decorator from the
        // target Class.
        if (Class.hasOwnProperty('__inject__')) {
            result = Object.keys(Class.__inject__)
                .map((propertyName : string) => {
                    return {
                        propertyName: propertyName,
                        injectionKey: Class.__inject__[propertyName]
                    }
                });
        }

        return result;
    }
}

interface InjectionPoint {
    propertyName : string;
    injectionKey : string;
}
```

The `Injector#intantiate()` method looks for the `#__inject__` property added to a Class' constructor function by the `@inject` decorator and then uses the values that hash contains to fulfil the decorated dependencies of the target Class - ie:

```typescript
const myUserModel = new UserModel();
injector.mapValue('UserModel', myUserModel);

// `#userModel` will be injected automatically by by injector
var myLoginService = injector.instantiate(LoginService)
myLoginService.performLogin();
```

A complete example with Mocha Tests provided over at [github.com/jonnyreeves/ts-prop-injection](https://github.com/jonnyreeves/ts-prop-injection).  Further exploration could include injection via setter methods / constructor injection and container life-cycle management (ie: singletons vs instance injection).