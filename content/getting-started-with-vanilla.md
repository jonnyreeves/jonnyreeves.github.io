Title: Getting Started with AS3 Vanilla
Date: 2011-08-14 16:15
Category: ActionScript

A lot of people are excited about the news that Native JSON support is coming with [Flash Player 11](https://web.archive.org/web/20120104112810/http://www.bytearray.org/?p=3066); however, I’ve also seen a lot of people get a bit confused by what this actually means – if you were hoping that Flash would be able to magically convert your parsed JSON Strings into your own Model objects then you’re going to be left a touch disappointed – until now!

## That’s Just Weak...
Let’s start by using the new native JSON methods to parse some JSON and see what we get back, for this example I will be making use of the Yahoo! Weather API to get the forcast for London.

```actionscript
public class Main extends Sprite {
    private var loader : URLLoader = new URLLoader();

    public function Main() {
        loader.addEventListener(Event.COMPLETE, onLoaderComplete);

        // Look up the weather in London (probably raining...)
        loader.load(new URLRequest("http://weather.yahooapis.com/forecastjson?w=44418&u=c"));
    }

    private function onLoaderComplete(event : Event) : void {
        const rawJson : String = loader.data;

        // Use a JSON decoder to convert the rawJson String into an Object.
        const jsonObject : Object = JSON.decode(rawJson);
    }
}
```

The above code given provides me with a `jsonObject` property, however, it’s completely dynmaic; this means I won’t gain any of the benefits of Strong Typing such as code hinting – if I want to access the properties, I have to know their names, eg:

```actionscript
trace("The weather in " + jsonObject.location.city + " is " + jsonObject.forecast[0].condition + " " + jsonObject.forecast[0].day);
```

## Getting Harder...
If you plan on passing the forecast data around in your application then you are going to start wishing you were making use of Strongly typed Model objects (for example, if you rely on using dyanmic objects then a simple typo in another class may cause you a headache) – ok, not a problem, the first step is to create a couple: (note I am not representing the entire Object Graph here to save space.

```actionscript
// Use a JSON decoder to convert the rawJson String into an Object.
const jsonObject : Object = JSON.decode(rawJson);

// Copy of the fields from the jsonObject into our strongly typed Model.
const weatherResult : WeatherResult = new WeatherResult();
weatherResult.url = jsonObject["url"];

weatherResult.location = new Location();
weatherResult.location.city = jsonObject.location.city;
weatherResult.location.locationId = jsonObject.location.location_id;
weatherResult.location.stateAbbreviation = jsonObject.location.state_abbreviation;
weatherResult.location.countryAbbreviation = jsonObject.location.state_abbreviation;
weatherResult.location.elevation = jsonObject.location.elevation;
weatherResult.location.latitude = jsonObject.location.latitude;
weatherResult.location.longitude = jsonObject.location.longitude;

weatherResult.forecast = new Vector.<Forecast>();
for each (var forecastJson : Object in jsonObject.forecast) {
    const forecast : Forecast = new Forecast();
    forecast.day = forecastJson.day;
    forecast.condition = forecastJson.condition;
    forecast.highTemperature = forecastJson.high_temperature;
    forecast.lowTemperature = forecastJson.low_temperature;

    weatherResult.forecast.push(forecast);
}

trace("The weather in " + weatherResult.location.city + " is " + weatherResult.forecast[0].condition + " " + weatherResult.forecast[0].day);
```

Crikey, that’s an awful lot of a lot of code; well – at least now if we’ve made a typo anywhere, or if Yahoo decide to change their API at least we only have to make our changes in a single place – there must be an easier way of doing this?!

## Adding some Vanilla Extract
Enter [AS3 Vanilla](https://github.com/jonnyreeves/as3-vanilla). Vanilla is an open source AS3 library whose sole purpose it to make converting untyped objects (such as the result of calling JSON.decode) into strongly typed Model objects a breeze, let’s see it in action:

```actionscript
// Use a JSON decoder to convert the rawJson String into an Object.
const jsonObject : Object = JSON.decode(rawJson);

// Use Vanilla to extract the properties into our model objects.
const weatherResult : WeatherResult = new Vanilla().extract(jsonObject, WeatherResult);

trace("The weather in " + weatherResult.location.city + " is " + weatherResult.forecast[0].condition + " " + weatherResult.forecast[0].day);
```

Yep, that’s it; 20 lines of tedious, error prone code replaced with a single call to Vanilla’s `extract()` method; pretty neat eh? So, let’s have a look at how it works.

The main design goal of Vanilla was to make the extraction process as simple as possible – infact, if your JSON object matches up perfectly to your Model object then you don’t need to do a thing, for example, here’s our WeatherResult model object’s class definition:

```actionscript
public class WeatherResult {
    public var url : String;
    public var location : Location;
    public var forecast : Vector.<Forecast>;
}
```

Let’s compare that to a cross section of the JSON object we get back from the Yahoo weather api:

```javascript
{
   "location":{
      "location_id":"UKXX0085",
      "city":"London",
      "state_abbreviation":"ENG",
      "country_abbreviation":"UK",
      "elevation":56,
      "latitude":51.51000000000000,
      "longitude":"-.08"
   },
   "url":"http://weather.yahoo.com/forecast/UKXX0085.html",
   "forecast":[
      {
         "day":"Today",
         "condition":"Partly Cloudy",
         "high_temperature":"70",
         "low_temperature":"52"
      },
      {
         "day":"Tomorrow",
         "condition":"Partly Cloudy",
         "high_temperature":"72",
         "low_temperature":"58"
      }
   ]
}
```

As you can see, the three fields in the WeatherResult model object, _location_, _url_ and _forecast_ all map exactly to those fields in the JSON object – Vanilla exploits this and guesses that you probably want to map to those fields; however, not everything is always so clear – what if your model object doesn’t map up exactly to the JSON result? Let’s have a look at our Location model:

```actionscript
public class Location {
    public var locationId : String;
    public var city : String;
    public var stateAbbreviation : String;
    public var countryAbbreviation : String;
    public var elevation : Number;
    public var latitude : Number;
    public var longitude : String;
}
```

If you look closely you will notice how some of the field names do not map to the JSON, for example, the field “country_abbreviation” in the JSON is not present in the Model (I’ve named the field countryAbbreviation, as per the AS3 camelCase convention), so how does Vanilla know what to do? Simple answer, it doesn’t – nothing will be mapped and Location.country Abbreviation will be null. 

## Using Metadata to define Marshalling Rules
In the above example the JSON field `country_abbreviation` was not being mapped to our model’s “countryAbbreviation” property because Vanilla didn’t know that these two were related – so how can we tell Vanilla about that relationship? Like this:

```actionscript
public class Location {
    [Marshall (field="location_id")] public var locationId : String;
    public var city : String;
    [Marshall (field="state_abbreviation")] public var stateAbbreviation : String;
    [Marshall (field="country_abbreviation")] public var countryAbbreviation : String;
    public var elevation : Number;
    public var latitude : Number;
    public var longitude : String;
}
```

Here we have annotated the public fields of the Location model object with the [Marshall] Metadata tag – this tells Vanilla that if we see a field named ‘country_abbreviation’ on the source (JSON) object, then we should copy that value to the annotated filed.

## Have It Your Way
Although Vanilla aims to be as easy to use as possible, it also tries to be flexible to adapt to different ways of working – lots of teams make use of explicit getter/setter methods instead of using fields; don’t worry – Vanilla can detect metadata on these methods too!