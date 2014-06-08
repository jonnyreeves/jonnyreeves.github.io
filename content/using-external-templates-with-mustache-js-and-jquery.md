Title: Using External Templates with Mustache.js and jQuery
Date: 2012-02-12 16:15
Category: JavaScript

[Mustache](http://mustache.github.com/) is a language independent, logicless [templating engine](http://en.wikipedia.org/wiki/Template_engine_(web)) which, in the context of a JavaScript / HTML5 style web application, means you can use it to separate your logic (javascript code) from your view (HTML Markup). Mustache comes in a variety of flavours; this article will be focusing on the [JavaScript implementation](https://github.com/janl/mustache.js).

### Why Bother With Templating At All?
Fair question; when it comes simple JavaScript powered sites it’s pretty easy to just build up your HTML inline:

```javascript
$('body').append('<p>Hello John, it is 11:19.</p>');
```

However, it starts getting a bit messy when we start replacing hard-coded values with variables, for example:

```javascript
var date = new Date();
var name = 'Jonny';
var timeNow = date.getHours() + ':' + date.getMinutes();
```

```javascript
$('body').append('<p>Hello ' + name + ', it is ' + timeNow + '.</p>');
```

Things get even more ugly when we want to start build up complex, nested HTML elements, for example:

```javascript
$('body').append('<dl><dt>Name</dt><dd>' + name + '</dd><dt>Time</dt><dd>' + timeNow + '</dd></dl>');
```

As JavaScript doesn’t support [heredoc](http://en.wikipedia.org/wiki/Here_document), the only way to sort out this nasty one-liner is to escape the new line literal by using a backslash; however I’m not convinced that this really helps with readability.

```javascript
$('body').append('<dl>\
 <dt>Name</dt>\
 <dd>' + name + '</dd>\
 <dt>Time</dt>\
 <dd>' + timeNow + '</dd>\
</dl>');
```

## Enter the Templating Engine
Templating engines help us solve half the problem by allowing us to move the logic out of the HTML string. The basic premise is fairly simple; instead of having to break out of the String, we can just drop in tokens which the templating engine will replace for us. So instead of having to concatenate lots of Strings together we can simply express our template like this:

```javascript
var date = new Date();

// Contains all the values that we want to use in place of the tokens in
// the template
var templateData = {
    name: "Jonny",
    timeNow: date.getHours() + ':' + date.getMinutes()
};

// Define our HTML template, note the tokens match up to the properties
// of the templateData object.
var template = '<p>Hello {{name}}, it is {{timeNow}}.</p>';

// Use Mustache.js to render the template (replace the tokens with the values
// in the templateData object).
var renderedTemplate = Mustache.render(template, templateData);

// And attach the rendered template HTML to the DOM.
$('body').append(renderedTemplate);
```

Nice, now we have a clear separation between our template HTML and our data Object which supplies the values; however, we are still stuck when it comes to rendering more complex templates…

```javascript
var template = '<dl>\
 <dt>Name</dt>\
 <dd>{{name}}</dd>\
 <dt>Time</dt>\
 <dd>{{timeNow}}</dd>\
</dl>';
```

### Would you declare your JavaScript in HTML?
So we have managed to simplify our code by replacing String concatenation with token substiution (templating); but we are still having to declare our template’s HTML in JavaScript which is far from ideal. What we really want is to be able to write our template in raw HTML as opposed to a String literal – time for some external templates. John Resig is widely regarded as having coined the concept of [declaring templates in script blocks](https://web.archive.org/web/20120406204734/http://ejohn.org/blog/javascript-micro-templating/); ie:

```html
<!-- Our Template is declared in a script block, but we
     can just use regular HTML markup -->
<script id="tpl-greeting" type="text/html">
    <dl>
        <dt>Name</dt>
        <dd>{{name}}</dd>
        <dt>Time</dt>
        <dd>{{timeNow}}</dd>
    </dl>
</script>
<script type="text/javascript">
    var date = new Date();

    var templateData = {
        name: "Jonny",
        timeNow: date.getHours() + ':' + date.getMinutes()
    };

    // Use jQuery to reference our 'tpl-greeting' script block
    // and grab the HTML contents it contains.
    var template = $('#tpl-greeting').html();

    // Render this template as before.
    $('body').append(Mustache.render(template, templateData));
</script>
```

Much nicer! Now we are able to write our template in HTML as opposed to simply mashing Strings together; however, this method still isn’t ideal; in order for it to work we have to define our template in the parent HTML Document; this is fine for a simple example, but in a real world web application you won’t be writing your JavaScript in a script block, you’ll be using external .js files instead – and you don’t really want to have to send all the HTML Templates down in the original page – let’s externalise those templates and load them in as we need them.

### Loading External HTML Templates
jQuery makes it really easy to load external content via its `jQuery.get()` method. We can use this to load an external HTML file which contains our template:

```html
<!-- You can define as many templates as you like in a single
    .htm file; just add additional <script /> blocks with
    unique ids. -->
<script id="tpl-greeting" type="text/html">
    <dl>
        <dt>Name</dt>
        <dd>{{name}}</dd>
        <dt>Time</dt>
        <dd>{{timeNow}}</dd>
    </dl>
</script>
```

```javascript
$.get('greetings.htm', function(templates) {
    // Fetch the <script /> block from the loaded external
    // template file which contains our greetings template.
    var template = $(templates).filter('#tpl-greeting').html();
    $('body').append(Mustache.render(template, templateData));
});
```

Now we’re talking! Finally, we are able to define our templates in external HTML files which can easily be loaded and rendered in our application’s JavaScript code. However, the above is only a proof of concept and doesn’t really stand up in the real world; what if we want to render our greetings template more than once? If we are going to have to load the template file each time our code is going to be littered with callback functions – again, not pretty and not easy to maintain – what we need is some kind of plugin…

### jQuery-Mustache Plugin
To make working with Mustache in jQuery nice and easy I knocked together my first jQuery Plugin, [jquery-mustache.js](https://github.com/jonnyreeves/jquery-Mustache). This makes it really easy to load all your external templates at the start and then render them as required.

```javascript
$.Mustache.load('greetings.htm', function() {
    $('body').mustache('tpl-greeting', templateData);
});
```

Sweet!