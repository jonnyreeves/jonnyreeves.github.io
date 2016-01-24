Title: Injecting into Constructors with TypeScript Decorators
Date: 2015-08-06 07:00
Category: TypeScript

In the [previous post](/2015/injecting-into-methods-with-typescript-decorators/) I added support for injecting into methods; this post provides the last missing InjectionPoint, constructor injection.  As with [AS3 Metadata](http://pierrechamberlain.ca/blog/2011/04/custom_metadata/), you can't annotate the `#constructor()` method directly:

```typescript
class MyClass {

  // Although this would be the preferred syntax it will throw a compiler error,
  // TS1206: Decorators are not valid here.
  @inject('firstName')
  constructor(name : string) { ... }
}
```

Instead, we need to add the decorator to the Class, ie:

```typescript
@inject('firstName')
class MyClass {
  constructor(name : string) { ... }
}
```

This is slightly awkward as it moves our decorator away from the constructor declaration which contains our injection arguments - that's somewhat compounded by the fact constructor injection is the most desirable form of the three (constructor, method and property) as it promotes immutability by ensuring an object has all of its dependencies when constructed - still, at least it works :)

The first change is to the `@inject` decorator, previously we expected the first argument to the decoratorFactory (`target`) to be the instance of the Class being decorated; however because we are decorating the class itself, the decoratorFactory can't be invoked with the instance, instead it receives a reference to the Class' constructor function, likewise it does not receive a `decoratedPropertyName` argument.:

```typescript
function inject(...injectionKeys : Array<string>) {
  return function decoratorFactory(target : Object|Function, decoratedPropertyName? : string) : void {
    let targetType : Function;
    
    if (typeof target === 'function' && decoratedPropertyName === undefined) {
      targetType = target;
    }
    else {
      targetType = target.constructor;
    }
  
    /* ... */
}
```

Next we need to record the `injectionKeys` that the user wants to be used to fulfill the constructor's dependencies - our `InjectionPoint` object is currently used to record dependencies, however it doesn't really fit for recording a constructor's dependencies:

* `InjectionPoint#constructor()` takes three arguments, the target instance, decorated property name and a list of injectionKeys, but there is no target instance for a decorated constructor (we just get a reference to the Constructor function), and the decoratorFactory also does not receive a decoratedPropertyName argument.
* `InjectionPoint#inject()` is expected to perform the injection against the target instance, but we need to Construct a new instance (and return it)

To deal with these special cases I ended up creating the `ConstructorInjectionPoint` class which specialises `InjectionPoint` to deal with the issues outlined above:

```typescript
export class ConstructorInjectionPoint extends InjectionPoint{
    constructor(injectionKeys : Array<string>) {
        super(null, 'constructor', injectionKeys);
    }

    inject(values : Array<any>) : void {
        throw new Error('Unsupported operation #inject()');
    }
}
```

This style of specialisation is not ideal; the worst offender is that `ConstructorInjectionPoint#inject()` throws an unsupported operation error - this design leads to a violation of the Liskov Substitution Principle (all sub-types should be interchangeable with their parent type) so it's something I plan to come back and revisit at a later date. 

The decorator can now create the appropriate `InjectionPoint` type based on the arguments it receives

```typescript
function inject(...injectionKeys : Array<string>) {
  return function decoratorFactory(target : Object|Function, decoratedPropertyName? : string) : void {
    let targetType : Function;
    let injectionPoint : InjectionPoint;
    
    // Decorator applied to Class (for Constructor injection).
    if (typeof target === 'function' && decoratedPropertyName === undefined) {
      targetType = target;
      injectionPoint = new ConstructorInjectionPoint(injectionKeys);
    }
    
    // Decorator applied to member (method or property).
    else if (typeof target === 'object' && typeof decoratedPropertyName === 'string') {
      targetType = target.constructor;
      injectionPoint = new InjectionPoint(target, decoratedPropertyName, injectionKeys);
    }
  
    targetType.__inject__[injectionPoint.propertyName] = injectionPoint;
}
```

Now that the `ConstructorInjectionPoint` is being recorded, we need to modify `Injector#instantiate()` to make use of it when creating the resulting instance:

```typescript
class Injector {
  instantiate<T>(Class : Constructable<T>) : T {
    // Create an instance of the target Class applying the Constructor InjectionPoint if it has one.
    const instance : T = this.createInjecteeInstance(Class);
    /* ... apply property and method injection points ... */
    return instance;
  }
  
  private createInjecteeInstance<T>(Class : { new(...args : Array<any>) : T }) : T {
    let result : T;

    if (Class.hasOwnProperty('__inject__')) {
      const injectionPoint : InjectionPoint = (<InjectionTarget> Class).__inject__.constructor];
  
      if (injectionPoint) {
        result = invokeConstructor(Class, this.getInjectionValues(injectionPoint));
      }
    }
    
    // If no Constructor InjectionPoint is found return a new instance with no arguments.
    return result || new Class();
  }
}
```

The `invokeConstructor()` is a necessary evil that crops up in a lot of languages where you wish to call a constructor function with the `new` keyword.  Note that you can't make use of `Function.apply` here as there is no valid scope to pass (the scope is the new instance!), as a result we end up with this familiar pattern, the pyramid of doom:
   
```typescript
function invokeConstructor<T>(Class : { new(...args : Array<any>) : T }, args : Array<any>) : T {
    switch (args.length) {
        case 0: return new Class();
        case 1: return new Class(args[0]);
        case 2: return new Class(args[0], args[1]);
        case 3: return new Class(args[0], args[1], args[2]);
        default:
          throw new Error("I got bored...");
    }
```

As before I've pushed the code to [Github](https://github.com/jonnyreeves/ts-prop-injection/tree/03-ctor-injection) and create a [Pull Request](https://github.com/jonnyreeves/ts-prop-injection/pull/2) to highlight changes from the previous post.