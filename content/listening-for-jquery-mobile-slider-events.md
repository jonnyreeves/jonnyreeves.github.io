Title: Listening for jQuery Mobile Slider Events
Date: 2012-07-24 16:15
Category: JavaScript

jQuery Mobile provides a neat little slider control; however, the version 1.1 release doesn’t behave very well and fails to dispatch the expected start and stop events triggered by jQuery UI’s slider control. [This issue (#1589)](https://github.com/jquery/jquery-mobile/issues/1589) has been raised on jQuery Mobile’s GitHub Issue Tracker but it looks like it won’t be addressed until jQuery Mobile 1.2

The code below is a patch which you can drop into your application’s startup routine; it adds a couple of event listeners to the DOM which will trigger the start and stop events based on the user’s interaction with the slider’s thumb and track.

```js
$(document).on({
    "mousedown touchstart": function () {
        $(this).siblings("input").trigger("start");
    },
    "mouseup touchend": function () {
        $(this).siblings("input").trigger("stop");
    }
}, ".ui-slider");
```

In a nutshell, it binds an event listener to the document object which listens for both `mousedown` and `touchstart` events triggered from `.ui-slider` elements. Once triggered the handler function will find the input element which sits alongside the `.ui-slider` control that was interacted with and trigger the corresponding event. You can consume these events like so:

```js
$("#my-slider").on("start", function () { 
    console.log("User has started sliding my-slider!");
});

$("#my-slider").on("stop", function (event) {
    var value = event.target.value;
    console.log("User has finished sliding my slider, final value: " + value);
});
```

As always, you can also subscribe to the slider’s change event if you want to listen for the actual slide.

```js
$("#my-slider").on("change", function (event) {
    var value = event.target.value;
    console.log("Slider is moving, it's value is now: " + value);
});
```