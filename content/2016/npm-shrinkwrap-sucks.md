Title: npm-shrinkwrap Sucks
Date: 2016-05-03 21:00
Category: JavaScript

Despite suggesting that you should always [shrinkwrap your npm dependencies](/2016/shrinkwrap-your-npm-dependencies), I've come to the conclusion that npm-shrinkwrap not only sucks, but is fundamentally broken.  It doesn't quite suck as much as having your dependencies update underneath your feet, but it still sucks...

## Adding new dependencies is a pain
Adding new dependencies to your project without npm-shrinkwrap is pretty straight forward:

1. Run `npm install --save-dev left-pad`
2. Raise a pull request with a 1 line change.

Performing the same task with a `shrinkwrap.json` file present is a pain...

1. Run `npm install --save-dev left-pad`
2. Run `npm prune` to de-dupe the dependency graph incase one of your existing modules made use of `left-pad` somewhere otherwise `npm shrinkwrap` will fail
3. Run `npm shrinkwrap --dev` to update the shrinkwrap file
4. Raise a pull request, note that hte package.json file has a tonne of [unreadable and unexpected changes](https://github.com/npm/npm/issues/3581) - enjoy the fact that github refuses to render the diff on the shrinkwrap file...

Sure you could look to use [uber's npm-shrinkwrap tool](https://github.com/uber/npm-shrinkwrap#motivation) but that's yet another dependency to add.

## It's not obvious when things are broken
So this one is not npm-shrinkwrap's fault, but it caused my team to lose some productivity today: our project makes use of 4 (count em!) package.json files, each of which has their own shrinkwrap file - we use these to lock the dependency graph and have a weekly CI task to update everything using [npm-check-updates](https://www.npmjs.com/package/npm-check-updates).  Somehow one of the `npm-shrinkwrap.json` files went AWOL; everything carried on working as expected for about two weeks but a chunk of the project's dependencies were being updated with each build.  We only found out when [a bug in ESLint](https://github.com/eslint/eslint/issues/6015) caused our Pull Request builds to start failing which triggered the obvious question of "Why the hell did ESLint update automatically?!".

## So what's the solution?
A co-worker of mine suggested the blindingly obvious approach of just using explicit versions in the `package.json` file, so instead of declaring:

```
dependencies: {
  "left-pad": "^1.0.2"
}
```

You would instead declare:

```
dependencies: {
  "left-pad": "1.0.2"
}
```

That's it.  npm provides the `-E, --save-exact` flag to do this for you when installing with `--save` or `--save-dev`.  [npm-check-updates](https://www.npmjs.com/package/npm-check-updates) works as expected (suggesting newer versions) and your pull request diffs go back to a single line.  To prevent developers accidentally committing a "ranged" dependency we've added the following pre-flight check as part of our CI process:

```sh
grep \"[~^] package.json
if [[ $? != 1 ]]; then
  echo "Non-exact dependency version detected, install with --save-exact"
  exit 1
fi
```

Having written this, I'm not sure I see any benefits over using `npm shrinkwrap` over using, and enforcing exact dependency versions in your `package.json` (and using a tool to manaully update them on a controlled cadence).
