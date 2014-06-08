Title: Builder Pattern in ActionScript – Fluent Constructors
Date: 2013-01-25 16:15
Category: ActionScript

How many times have you come across a class which looks like this:

```actionscript
package nutrition.model {
    public class NutritionFacts {
        private var _servingSize : uint;    // (mL) required
        private var _servings : uint;       // (per container) required
        private var _calories : uint;       // optional
        private var _fat : uint;        // (g) optional
        private var _salt : uint;       // (mg) optional
        private var _carbohydrate : uint;   // (g)  optional

        public function NutritionFacts(servingSize : uint, servings : uint, calories : uint = 0, fat : uint = 0, salt : uint = 0, carbohydrate : uint = 0)  {
            _servingSize = servingSize;
            _servings = servings;
            _calories = calories;
            _fat = fat;
            _salt = salt;
            _carbohydrate = carbohydrate;
        }
    }
}
```

I’m not a great fan of this style of object construction, it ends up making massive single lines of code which are confusing to read for example, in the following example, what does the 4th argument actually set, why is it zero?

```actionscript
const colaFacts : NutritionFacts = new NutritionFacts(330, 1, 500, 0, 35, 22)
```

One soltution to this problem is to only demand the required fields in the constructor and use setters for the other fields, we end up with something similar to this:

```actionscript
package nutrition.model {
    public class NutritionFacts {
        private var _servingSize : uint;    // (mL) required
        private var _servings : uint;       // (per container) required
        private var _calories : uint;       // optional
        private var _fat : uint;            // (g) optional
        private var _salt : uint;           // (mg) optional
        private var _carbohydrate : uint;   // (g)  optional

        public function SetterNutritionFacts(servingSize : uint, servings : uint) {
            _servingSize = servingSize;
            _servings = servings;
        }

        public function set calories(value : uint) : void {
            _calories = value;
        }

        public function set fat(value : uint) : void {
            _fat = value;
        }

        public function set salt(value : uint) : void {
            _salt = value;
        }

        public function set carbohydrate(value : uint) : void {
            _carbohydrate = value;
        }
    }
}
```

To create our ColaFacts object using the above we would code:

```actionscript
const colaFacts : NutritionFacts = new NutritionFacts(330, 1);
colaFacts.calories = 500;
colaFacts.salt = 35;
colaFacts.carbohydrate = 22;
```

In my opinion this approach is preferable, but now it has introduced a different problem, one of design. In the first example where all the arguments were passed in the constructor, the NutritionFacts object was immutable – its values could not be modified once the object had been instantiated. However, with the NutritionFacts object shown above the calories, fat, salt and carbohydrate values can all be modified elsewhere in the code. If we have our purist Object Orientated Developer hat on we would declare this as a violation of encapsulation.

The Builder Pattern offers us a solution, it allows us to create an immutable object (ie: no setters) which doesn’t end up having a massive constructor for all the optional values it can contain. In Effective Java, 2nd Edition, Joshua Bloch covers this under the title of “[Consider a Builder when faced with many constructor parameters](http://books.google.co.uk/books?id=ka2VUBqHiWkC&pg=PA11&lpg=PA11&dq=Consider+a+Builder+when+faced+with+many+constructor+parameters&source=bl&ots=yZChKfnZM2&sig=8_wa7cmd_8-OcpGHRPmgezV79xw&hl=en&sa=X&ei=1waUU7LXIMO_PNXGgLgI&ved=0CDwQ6AEwAQ#v=onepage&q=Consider%20a%20Builder%20when%20faced%20with%20many%20constructor%20parameters&f=false)”. In his book, Josh makes use of an inner class to create the Builder, although we have inner classes in ActionScript, they do not share the same behaviour as those in Java, especially when it comes to the visibility of member properties – this makes implementing Josh’s example in ActionScript difficult, however, by using the internal visibility modifier we can create a close approximation.

First we have the NutritionFactsBuilder, this is based upon the Builder pattern and make use of a fluent interface:

```actionscript
package nutrition.model {
    public class NutritionFactsBuilder {
        internal var servingSize : uint;
        internal var servings : uint;
        internal var calories : uint;
        internal var fat : uint;
        internal var salt : uint;
        internal var carbohydrate : uint;   

        public function NutritionFactsBuilder(servingSize : uint, servings : uint) {
            this.servingSize = servingSize;
            this.servings = servings;
        }

        public function withCalories(value : uint) : NutritionFactsBuilder {
            calories = value;
            return this;
        }

        public function withFat(value : uint) : NutritionFactsBuilder {
            fat = value;
            return this;
        }

        public function withSalt(value : uint) : NutritionFactsBuilder {
            salt = value;
            return this;
        }

        public function withCarbohydrate(value : uint) : NutritionFactsBuilder {
            carbohydrate = value;
            return this;
        }

        public function build() : NutritionFacts {
            return new NutritionFacts(this);
        }
    }
}
```

Next up we have the NutritionFacts class, note that now the only argument it expects in the constructor is a NutritionFactsBuilder instance:

```actionscript
package nutrition.model {
    public class NutritionFacts {
        private var _servingSize : uint;    // (mL) required
        private var _servings : uint;       // (per container) required
        private var _calories : uint;       // optional
        private var _fat : uint;        // (g) optional
        private var _salt : uint;       // (mg) optional
        private var _carbohydrate : uint;   // (g)  optional

        public function NutritionFacts(builder : NutritionFactsBuilder) {
            _servingSize = builder.servingSize;
            _servings = builder.servings;
            _calories = builder.calories;
            _fat = builder.fat;
            _salt = builder.salt;
            _carbohydrate = builder.carbohydrate;
        }
    }
}
```

We can now employ the builder to create us our NutritionFacts object:

```actionscript
const colaFacts : NutritionFacts = new NutritionFactsBuilder(330, 1)
    .withCalories(500)
    .withSalt(35)
    .withCarbohydrate(22)
    .build();
``` 

Note that we are supplying the required servingSize and servings values in the NutritionFactsBuilder() constructor, but all the other optional values can now be supplied via method chaining. When build() is called the NutritionFactsBuilder will return a new instance of NutrionFacts for us; this constructed NutritionFacts object is now immutable and the reader can easily see which properties are going to be set on the instance. Because we have made the properties of the NutritionFactBuilder object internal, they are only visible to classes inside the “nutrition.model” package, as the consumers of models shouldn’t be in the models package they will not be visible (only the public with… methods will be). Another nice benefit is that we have split construction of our object (performed by the NutritionFactsBuilder) out from the actual object (NutrtionFacts) – if NutritionFacts was instead an interface, the Builder could return a different concrete instance to the user without them ever knowing.

By using the Builder Pattern in this fashion we are creating something similar to named parameters as found in other languages – other ActionScript developers have already found their own solutions to this, the most recognisable being Greensock’s excellent TweenLite, where an untyped object is used to optional provide parameters ie:

```actionscript
new TweenLite(target, 0.8, { x: 50, y: 100 });
```

I think this works well for TweenLite, however, I often find myself having to head on over to greensock.com whenever I need to do something a little bit more complicated (for example, is it onCompleteParams, or onCompleteArgs?), the above Builder Pattern approach could have possibly answered that for us:

```actionscript
new TweenBuilder(target, 0.8)
    .x(50)
    .y(150)
    .onCompleteParams([ "foo" ])
    .tween();
```