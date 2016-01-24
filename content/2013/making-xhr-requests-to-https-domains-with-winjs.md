Title: Making XHR Request to HTTPS domains with WinJS
Date: 2013-01-25 16:15
Category: WinJS

I recently came across an interesting caveat when working with WinJS (the JavaScript layer for creating Windows 8 Store applications). If you attempt to make an HTTP POST request to a server over the HTTPS protocol you may run into the following error:

```
XMLHttpRequest: Network Error 0x2ef3, Could not complete the operation due to error 00002ef3.
```

This error appears to be caused by a security certificate issue; however the solution is pretty straight forward – you just need to make a GET request before attempting subsequent POST request, for example:

```javascript
// Before making a POST request we first have to issue a GET against the target
// server to work around Network Error 0x2ef3.  Note you only need to do this
// ONCE in your app, not every time.
WinJS.xhr({
    url: "https://my.server/"
}).then(function () {

    // After a single GET request we can now invoke POST requests.
    WinJS.xhr({
        url: "https://my.server/endpoint",
        type: "POST",
        data: {
            foo: "bar"
        }
    })
}).then(function () {
    console.log("HTTPS POST request complete!");
});
```