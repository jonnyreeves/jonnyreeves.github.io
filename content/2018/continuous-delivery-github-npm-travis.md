Title: Continuous Delivery on Github Projects to NPM using Travis
Date: 2018-10-14 21:00
Status: draft

Continuous Delivery workflows allow you to get changes out to your end users faster. Enabling Continuous Delivery for JavaScript projects hosted on Github will result in others being able to try out changes as soon as a pull request is merged into master without having to wait for the next official release.

This guide assumes that you have already [configured your JavaScript project to build via Travis](https://docs.travis-ci.com/user/languages/javascript-with-nodejs/).

### The Workflow
The Contrinuous Delivery workflow I'm going to configure will give your consumers two release channels: 'latest' and 'next'. The 'latest' channel will be triggered by a manual release step and provide stability for your consumers whereas the 'next' channel will be released with every commit to master (typically when a Pull Request is squashed and merged).

![gmvault](/images/2018/continuous-delivery-github-npm-travis/cd-flow.jpg)