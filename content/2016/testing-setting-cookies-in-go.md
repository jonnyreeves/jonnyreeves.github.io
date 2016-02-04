Title: Testing Setting HTTP Cookies in Go
Date: 2016-02-04 20:00
Category: Golang

I found myself writing code that drops HTTP Cookies on a HTTP ResponseWriter
and had trouble figuring out how to test it:

```go
type Preferences struct {
	Colour string
}

func SetPreferencesCookie(w http.ResponseWriter, prefs *Preferences) error {
	data, err := json.Marshal(prefs)
	if err != nil {
		return err
	}
	http.SetCookie(w, &http.Cookie{
		Name:  "test",
		Value: base64.StdEncoding.EncodeToString(data),
	})
	return nil
}
```

The answer comes in the form of copying the Headers from an `http.Recorder`
into an `http.Response` object.

```go
func TestSetPreferencesCookie(t *testing.T) {
  // Create a new HTTP Recorder (implements http.ResponseWriter)
  recorder := httptest.NewRecorder()

  // Drop a cookie on the recorder.
  SetPreferencesCookie(recorder, &Preferences{ Colour: "Blue" })

  // Copy the Cookie over to a new Request
  request := &http.Request{Header: http.Header{"Cookie": recorder.HeaderMap["Set-Cookie"]}}

  // Extract the dropped cookie from the request.
  cookie, err := request.Cookie("test")
  require.NoError(t, err, "Failed to read 'test' Cookie": %v, err)

  // Decode the cookie
  data, err := base64.StdEncoding.DecodeString(cookie.Value)
  require.NoError(t, err, "Failed to Base64 decode 'test' Cookie: %v", err)

  // Unmarshal contents back into a Preferences struct
  var prefs *Preferences
  err = json.Unmarshal(data, &prefs)
  require.NoError(t, err, "Failed to parse 'test' Cookie JSON: %v", err)

  // Check the contents.
  require.Equal(t, "Blue", prefs.Colour)
}
```

Have a play with this code on the Go Playground: https://play.golang.org/p/r7aGdX9YEn.
