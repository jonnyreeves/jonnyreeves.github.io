Title: Testing QueryStrings in http.Request
Date: 2015-11-14 13:00
Category: Golang

This one threw me; say you have a subject that reads a value from an HTTP Request's Query, something like this:

```go
func ValidateState(req *http.Request) error {
	fwdState := req.URL.Query().Get("state")
	if fwdState !== "expected" {
	  return fmt.Errorf("Unexpected state value: %s", fwdState)
	}
	return nil
```

In order to test this method, you'll want to create an `http.Request` instead and pre-populate the QueryString.  My first attempt was the reverse how we read the Query value:

```go
func Test_ValidateState(t *testing.T) {
    req := &http.Request{URL:&url.URL{}}
    req.URL.Query().Set("state", "expected")
    err := ValidateState(req)
    require.NoError(t, err)
```

However, this fails with the `ValidateState` function returning an `"Unexepcted state value: "` error.  Instead, we need to set the `Request.URL.RawQuery` value directly:

```go
func Test_ValidateState(t *testing.T) {
    req := &http.Request{URL:&url.URL{}}
    req.URL.RawQuery = "state=expected"
    err := ValidateState(req)
    require.NoError(t, err)
```

