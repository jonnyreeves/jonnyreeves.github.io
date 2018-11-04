Title: Continuous Delivery on Github Projects to NPM using Travis
Date: 2018-11-04 18:00

Continuous Delivery workflows allow you to get changes out to your end users faster. Enabling Continuous Delivery for JavaScript projects hosted on Github will result in others being able to try out changes as soon as a pull request is merged into master without having to wait for the next official release.

This guide assumes that you have already [configured your JavaScript project to build via Travis](https://docs.travis-ci.com/user/languages/javascript-with-nodejs/).

TL;DR - jump to the [final Travis config](#putting-it-all-together).

### The Workflow
The Continuous Delivery workflow I'm going to configure will give your consumers two release channels: *latest* and *next*. Releases on the *latest* channel will be triggered by a manual release step and provide stability for your consumers whereas the *next* channel will be released with every commit to master (typically when a Pull Request is squashed and merged).

![Diagram of the desired continuous delivery flow](/images/2018/continuous-delivery-github-npm-travis/cd-flow.jpg)

### Travis Setup
The first step is to configure [Travis' npm Publisher](https://docs.travis-ci.com/user/deployment/npm/). The documentation wants us to run `travis setup npm`, but before we can do this, we need to have the Travis CLI installed locally; just follow the [Travis CLI installation guide](https://github.com/travis-ci/travis.rb#installation). 

*Nb:* Assuming you've logged into npm on your local machine, you can obtain your api key from `~/.npmrc`

```
$ travis setup npm
Detected repository as jonnyreeves/js-logger, is this correct? |yes| yes
NPM email address: ***@jon***ves.co.uk
NPM api key: ************************************
release only tagged commits? |yes| no
Release only from jonnyreeves/js-logger? |yes| no
Encrypt API key? |yes| yes
```

Once complete your `.travis.yml` file will have been modified and the following configuration added:

```yaml
deploy:
  provider: npm
  email: ***@jon***ves.co.uk
  api_key:
    secure: 0f[...]e=
```

For additional privacy from automated scapers, I would suggest you also encrypt your npm email address; again you can use the Travis CLI to perform this action and update your local travis configuration:

```
travis encrypt foo@example.com --add deploy.email
```

Finally, we need to configure Travis to `skip_cleanup` to ensure that any artifacts generated during the build process are not removed before the publishing step (refer to the docs [here](https://docs.travis-ci.com/user/deployment/npm/#releasing-build-artifacts)). To do this, modify the `deploy` block inside your `.travis.yml` so it includes the `skip_cleanup` property:

```
deploy:
  provider: npm
  skip_cleanup: true	# <-- add this line
  email:
  	secure: 0f[...]2=
  api_key:
    secure: 0f[...]e=
```

Finally, we need to tell travis to only run the deploy step when a commit is made in the `master` branch. To do this, modify the `deploy` block to make it [conditional based on the target branch](https://docs.travis-ci.com/user/deployment/#conditional-releases-with-on).

With this configuration in place, Travis will now publish a release to npm each time you create a new tag; however this does not match our desired Continuous Delivery pipeline where each commit to master results in a new release.

### Npm Release Channels
In order to create our desired Continuous Delivery pipeline we need to create two release channels: 

* *latest*: Periodically created by the maintainers of the project, reccomended for production usage
* *next*: Automatically created on every change made to master, reccomended for testing out new features in a non-production environment or for those who like to live dangerously.

Npm helps us by providing the concept of [dist-tags](https://docs.npmjs.com/getting-started/using-tags). Dist-tags are used by npm to identify what the latest version of any given package is when a user runs npm install. When publishing a package, npm will automatically populate the `dist-tag` to be `latest` if no value is supplied by the user.

Here's an example to explain the concept: let's assume that the `example-pkg` package has 3 distinct versions that have been published to npm under the 'latest' dist-tag:

```
example-pkg
- 0.0.1 [dist-tag=latest] <-- published 01/01/2018
- 0.0.2 [dist-tag=latest] <-- published 02/01/2018
- 0.0.3 [dist-tag=latest] <-- published 03/01/2018
```

Now when you run `npm install example-pkg` npm will fetch 0.0.3 as that was the most recent version to be published. Now let's publish another release but this time we will specify the dist-tag as 'next', now the release history of `example-pkg` looks like this:

```
example-pkg
- 0.0.1 [dist-tag=latest] <-- published 01/01/2018
- 0.0.2 [dist-tag=latest] <-- published 02/01/2018
- 0.0.3 [dist-tag=latest] <-- published 03/01/2018
- 0.0.4 [dist-tag=next]   <-- published 04/01/2018
```

Should you run `npm install example-pkg` now, npm will still fetch version `0.0.3`, even tho it was not the most recent version to be published. This is because `npm install` defaults to fetching releases from the `latest` dist-tag. When running npm-install we can specify an alternative release channel using the `@` syntax and specifying a dist-tag, ie:

```
npm install example-pkg@next
```

Now npm will fetch version `0.0.4` as it was the most recent version to be published to the `latest` release channel.

With this in mind we need a way of determining if a release is destined to be published to either the *latest* or *next* release channel, but how can we do this? Fortunately semver has us covered with [pre-release versions](https://semver.org/spec/v2.0.0.html#spec-item-9) where a pre-release version (ie: a release to the *next* channel) may be denoted by appending a hyphen and a series of dot separated identifies immediately following the patch version. 

If we set our `package.json` file's `version` property to `x.y.z-next` in master then we can create a distinction between *stable* and *next* releases by checking for the presence of the `-next` prefix before the Travis deploy step. 

However, this simple approach will encounter a problem; npm will fail to publish if we try to publish a pre-existing version, and because each pull request we merge into master isn't going to bump our package version we need a way to create unique versions for releases to our *next* channel. A simple way to achieve this is to append the short git commit hash to our pre-release version suffix, eg: `x.y.z-next.d34db33f`.

## Putting it all together
To add all of the above logic to our `travis.yml` we add a `before_deploy` block and modify our `deploy` bock to make use of the new variable (`NPM_TAG`) it defines:

```yaml
before_deploy: |
  PKG_VERSION=$(node -p "require('./package.json').version")
  NPM_TAG="latest"
  if [[ ${PKG_VERSION} =~ -next$ ]]; then
    NPM_TAG="next"
    SHORT_COMMIT_HASH=$(git rev-parse --short HEAD)
    UNIQ_PKG_VERSION="${PKG_VERSION}.${SHORT_COMMIT_HASH}"
    npm --no-git-tag-version version ${UNIQ_PKG_VERSION}
  fi
deploy:
  skip_cleanup: true
  provider: npm
  tag: "$NPM_TAG"
  email:
    secure: 0f[...]2=
  api_key:
    secure: 0f[...]e=
  on:
    branch: master
```

With the above configuration in place we can set our package.json file's `version` property to include the `-next` suffix by default and push a commit that removes it each time we want to create a stable release on *latest* channel.

You can see this pipeline in action over on my [js-logger project]().