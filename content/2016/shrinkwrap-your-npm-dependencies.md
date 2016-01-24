Title: Shrinkwrap your NPM Dependencies
Date: 2016-01-04 20:00
Category: JavaScript

Things move a little too quickly in the NPM ecosystem for my liking at times, modules updates can turn a working project into a broken build with a single `npm install`; this is especially bad news if your [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration) server is pulling your NPM dependencies with each build.  Sometimes this can be the result of human error, other times it can be even [more confusing](https://github.com/rackt/react-router/issues/2195) leading to a lot of wasted effort in your team.

One way to bring order is to make use of [`npm shrinkwrap`](https://docs.npmjs.com/cli/shrinkwrap) which pins your project's `node_modules` at fixed revisions ensuring that you get the exact same dependency graph each time you `npm install`.  One major benefit of this approach is that you can safely cache and re-use your node_modules folder between CI builds which should dramatically decrease your pull-request build times.

There are however a couple of downsides, the main one being that you can no longer just `npm install` as NPM will not update `npm-shrinkwrap.json` (so your teammates / CI server won't fetch it), instead you need to go through the following dance and then commit both `package.json` and `npm-shrinkwrap.json` files.

```
npm install --save my-dep
npm dedupe
npm shrinkwrap
```

You may wish to consider [uber/npm-shrinkwrap](https://github.com/uber/npm-shrinkwrap) which looks like it helps streamline the process somewhat.
