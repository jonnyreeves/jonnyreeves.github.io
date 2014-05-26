Title: jQuery - A single click handler for multiple buttons
Date: 2012-05-23 16:15
Category: JavaScript

Event bubbling is a wonderful thing; in ActionScript mouse events would readily [bubble up through the DisplayList](http://www.rubenswieringa.com/blog/eventbubbles-eventcancelable-and-eventcurrenttarget) all the way up to the Stage allowing you to add a single event Handler to a parent DisplayObject and then inspecting the `event.target` property to determine which child button the user had interacted with. The same is true in JavaScript; but instead of events bubbling up the DisplayList they bubble up through the DOM.

Take the following example, here we have three buttons that we want to respond to when they’re clicked:

![Alt Text]({filename}/images/jquery-a-single-click-handler-for-multiple-buttons/three-buttons.png)

The HTML for this button group is nice and simple, making use of jQuery mobile:

```html
<div id="screen-selector" data-role="navbar">
	<ul>
		<li><a href="#" class="ui-btn-active">Applications</a></li>
		<li><a href="#">Properties</a></li>
		<li><a href="#">Events</a></li>
	</ul>
</div>
```

We can easily bind a click event handler to the `#screen-selector` element which will capture the click events as they bubble up the DOM.

```js
$('#screen-selector').on('click', function(event) {
	console.log("You clicked on: ", event.target);
}
```

This almost works as desired, but not quite. jQuery Mobile does some magic behind the scenes to transform our button markup into a more complex design, this results in the `event.target` of the click event being child elements of the `<a>` tag:

![Alt Text]({filename}/images/jquery-a-single-click-handler-for-multiple-buttons/button-event-target.png)

Instead, what we really want is to know which <a> element the user clicked so we can tie it back to the buttons in our original HTML. In ActionScript this could be solved quite easily by setting the [`mouseChildren` attribute](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/display/DisplayObjectContainer.html#mouseChildren) of the button DisplayObjects to false, ie:

```as3
var buttons : Array = [ getChildByName("btnApplications"), getChildByName("btnProperties"), getChildByName("btnEvents") ];
for each (var button : Sprite in buttons) {
	// Disable mouse interaction with any children nested within the button's DisplayObject.
	button.mouseChildren = false;
}
```

JavaScript lacks the ability to toggle the mouse interactivity of nested elements, but luckily jQuery comes to the rescue with the [closest traversal method](http://api.jquery.com/closest/). This method will walk up the DOM tree until if finds the first element that matches the supplied selector. In our case we just want to walk up from the click event’s target element until we find an `<a>` tag:

```js
$('#screen-selector').on('click', function(event) {
	var button = $(event.target).closest('a');
	console.log("You clicked on:", button);
}
```

This now logs the desired `<a>` tag for the clicked button!

This code can be improved one step further by [passing a selector argument](http://api.jquery.com/on/#example-7) to jQuery’s `on` method. jQuery will ensure that the event handler function is only called if the selector matches the event’s current target; in our case – we only want it to trigger when it hits an `<a>` tag, so we can write:

```js
$('#screen-selector').on('click', 'a', function(event) {
	var button = $(event.target);
	console.log("You clicked on:", button);
}
```

The last piece of the puzzle comes from creating a mapping between the button the user clicked on and the action we want to take. Again, Flash provided a really easy way to do this in the form of the DisplayObject.name property which your button handler could read.

```js
function onButtonClicked(event : MouseEvent) : void { 
	var button : DisplayObject = event.target as DisplayObject;
	trace("You clicked on:", button.name);
}
```

The buttons created by jQuery mobile don't offer any form of name identifier; one simple solution would be to simply add an id attribute to the `<a>` tag; however [element id's must always be unique](http://www.w3.org/TR/html401/struct/global.html#h-7.5.2) which isn't really want we are after (we just want to identify this button group apart, rather than having to ensure these buttons have a unique id across the entire DOM). The option I've settled on is to add a [custom data attribute](http://ejohn.org/blog/html-5-data-attributes/) to each `<a>` tag in the form of a data-name attribute:

```html
<div id="screen-selector" data-role="navbar">
	<ul>
		<li><a href="#" class="ui-btn-active" data-name="applications">Applications</a></li>
		<li><a href="#" data-name="properties">Properties</a></li>
		<li><a href="#" data-name="events">Events</a></li>
	</ul>
</div>
```

We can now modify our click event handler to read the data-name attribute from the clicked `<a>` element:

```js
$('#screen-selector').on('click', function(event) {
	// Retrieve the 'name' data attribute of the <a/> tag that the user clicked.
	var name = $(event.target).closest('a').data('name');
	console.log("You clicked on:", name);
});
```

Which gives us our desired effect! :)

![Alt Text]({filename}/images/jquery-a-single-click-handler-for-multiple-buttons/button-click-handler.png)
