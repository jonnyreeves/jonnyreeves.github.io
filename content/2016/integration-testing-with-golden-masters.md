Title: Integration Testing with Golden Masters
Date: 2016-04-18 21:00
Category: Golang

After watching [Mitchell Hashimoto's talk on Advanced Testing with Go](https://www.youtube.com/watch?v=yszygk1cpEc) I was inspired to re-write one of my integration tests to use a golden master.  Golden Master's are a simple concept which can be used to reduce the complexity of integration test cases whilst stil ensuring that the output of the program is valid.

## Bronze Age
The system under test I was working with applied a complex set of rules against a source directory and printed any violations of those rules to `stdout` much like a [code linting](http://stackoverflow.com/questions/8503559/what-is-linting) tool.

<center>
![Alt](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=TWFpbi0-TGludGVyOiBsAAMFLkxpbnQoJy9wYXRoL3RvL3NyYycpCgAeBi0-RGlyU2Nhbm5lcjogc2Nhbigkc3JjRGlyKQoAEAoASApbXUZpbGUKCmxvb3AgZm9yICRmaWxlIGluABIIICAAUQhQYXJzZXI6IAADBSgAIwUpCiAACQYARwsAIgVSZXN1bHQKZW5kCgCBEAkAgT0IY3JlYXRlUmVwb3J0KCRwACUKcwCBOwpNYWluOiAkcgAgBQoKAIIABkZvcm1hdACCBAVmAAMILgAPBigAJAcpAIE-C2Vycm9yIGluAD4JICAAOQkAQA1zdGRvdXQuV3JpdGUoKQplbmQ&s=vs2010)
</center>

The Formatter is responsible for the final output generating something along these lines:

```
./exampe.md
  L12 Invalid link: Resource not found: ./missing.png
  L22 Invalid link: Invalid filename: Mixed case: ./BadCase.png

✖ 2 Errors detected in 1 file.  
```

Before switching to using a Golden Master, the original integration test would supply a fixture to the linter and then iterate over the `$report` variable.

```go
func TestLinter(t *testing.T) {
	p := fixtureDir(t, "with_errors")
	linter := lint.NewLinter()
	actual := linter.Lint(p)
	expected := map[string][]LintError{
		filepath.Join(p, "example.md"): []LintError{
			LintError{
				Message: "Invalid link: Resource not found: ./missing.png",
				LineNo:  12,
			},
			LintError{
				Message: "Invalid link: Invalid filename: Mixed case: ./BadCase.png",
				LineNo:  22,
			},
		},
	}
	assert.Equal(t, actual, expected)
}
```

This approach, whilst valid, was pretty verbose and was not scaling well as my integration test became more thorough (as it stands I current assert 50 individual erorr cases over 6 test fixture files) - this feels like a great candidate for Golden Masters.

## Going for Gold
My approach would be simple; I would still pass a fixture to `linter.Lint()`, but instead of comparing the `result` object, I would pass it direclty to the `Formatter` and have it written out to a file on disk which could then be loaded and compared in future test-iterations.

To start I copy and pasted the command line output into a new `golden` file which mated the name of the fixture - the integration test will be modified to read in the contents of this file and use it for comparison.

Next I needed to capture the output of the Formatter, this was not straight forward as the `Formatter` wrote directly to `os.Stdout`.  I could have used an Interface to provide an alternative implementation of the `Formatter` which wrote to a file; but this would have resulted in a lot of duplicated logic; essentially there was nothing wrong with the current output; I just didn't want it to to go to `stdout`.  Instead I modified the `formatter` object's signature from `Format(r Report)` to `Format(r Report, out io.Writer)`:

```go
type Formatter struct{}

func (f *Formatter) Format(r Report, out io.Writer) {
	if report.Len() == 0 {
		fmt.Fprint(out, "✓ All files lint free")
		return
	}
	// ...
}
```

The default implementation can pass `os.Stdout` as the writer (as `os.Stdout` implements the `Write(p []byte) (n int, err error)` signature); and our integration test can pass a `bytes.Buffer` to capture the output.

```go
func TestLinter(t *testing.T) {
	p := fixtureDir(t, "with_errors")
	linter := lint.NewLinter()
	formatter := lint.NewFormatter()
	
	// alloc. a new buffer (`w`) which will capture the formatted output.
	buff := make(bytes.Buffer)
	formatter.Format(linter.Lint(p), buff)
	
	// readGoldenMaster uses ioutil.ReadFile()
	expected := readGoldenMaster(t, "with_errors")
	assert.Equal(t, buff.Bytes(), expected)
}
```

This passes, but updating the "with_errors" golden master file is a chore.  To address this I added a [flag](https://golang.org/pkg/flag/) to my integraiton test which made it simple to flip the test-case into an 'update the golden master' mode:

```go
var flagUpdate = flag.Bool("update", false, "Update golden master files")

func TestLinter(t *testing.T) {
	p := fixtureDir(t, "with_errors")
	linter := lint.NewLinter()
	formatter := lint.NewFormatter()
	buff := make(bytes.Buffer)
	formatter.Format(linter.Lint(p), buff)

	if *flagUpdate == true {
		ioutil.WriteFile("fixtures/with_errors_master.txt", buff.Bytes(), 0755)
		// fail the test to avoid false positives and halt further assertions.
		require.FailNow(t, "Updated golden master")
	}

	expected := readGoldenMaster(t, "with_errors")
	assert.Equal(t, buff.Bytes(), expected)
}
```

My workflow is now:

1. Make changes to the underlying linter (eg: add a new rule)
2. Add failing fixtures to the `with_errors` fixture
3. Run the integration test with: `go test integ_test.go --update` to update the golden record

It's now a simple case of manually verifying that the golden master generated in step 3 matches the output that I was expecting (made easy with a git diff tool).

