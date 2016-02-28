Title: Pre-commit Hooks in SmartGit
Date: 2016-02-28 14:00

SmartGit is my preferred Git client mainly due to its excellent visual diff tool that it ships with and the ability to easily manage several repositories.

![SmartGit diff tool](/images/precommit-hooks-in-smartgit/smartgit-screenshot.png)

One small annoyance (aside from the lack of spell-check in commit messages...) is the way it doesn't inherit your user profile (and therefore your PATH environment variable); this leads to pre-commit hooks failing to find build tools such as Node, especially if you have installed via [NVM](https://github.com/creationix/nvm).

![Missing tools errors](/images/precommit-hooks-in-smartgit/tool-not-found.png)

Thankfully, syntevo have provided a simple fix for this in SmartGit7; you can now edit the contents of the following file (depending on your OS)

* MacOS: `~/Library/Preferences/SmartGit/smartgit.vmoptions`
* Linux: `~/.smartgit/smartgit.vmoptions`
* Windows: `%APPDATA%\syntevo\SmartGit\smartgit.vmoptions`

In my case I needed to expose `brew` to SmarGit which was as simple as populating my `smartgit.vmoptions` file with the following:

```
# Extend SmartGit PATH to include brew / NVM
path=/usr/local/bin
```

Don't forget to restart SmartGit after saving this file.
