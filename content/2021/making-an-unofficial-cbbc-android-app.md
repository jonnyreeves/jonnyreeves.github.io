Title: Making an Unofficial CBBC Anrdoid App
Date: 2021-01-17 18:00

My kids love CBBC and CBeebies; with Max, who is currently 6, loving Danger Mouse. CBBC frequently advertise their website, which contains a great collection of mini-games, so naturally when they started promoting the latest Danger Mouse game, Max wanted to play it.

![CBBC Danger Mouse Game](/images/2021/cbbc-danger-mouse-game.jpg)

Given Max's age I use [Screen Time](https://screentimelabs.com) to both restict how much time he can spend on his tablet and control which apps he can use. I don't consider the WWW a particuarly safe place for six year olds, so a web-browser is currently off limits to him. This presented a problem: unlike with the excellent [CBeebies Playtime Island App](https://www.bbc.co.uk/cbeebies/apps/cbeebies-playtime-island-app), there is no CBBC app, the only to play the CBBC games is via the [CBBC website](https://www.bbc.co.uk/cbbc).

## Let's get hacking
No CBBC App, no problem - I've never written an Android app before, but I said to myself "how hard can this be?" - pretty easy it turns out, and in less than 3 hours I had built my own CBBC App.

The first step was finding a starter project, with a quick bit of googling I landed upon [successtar/web-to-app](https://github.com/successtar/web-to-app) which provided all the boiler plate I needed to create a simple app that spawned a WebView. A quick install of Android Studio later and I had built my first APK which opened https://bbc.co.uk/cbbc. 

A little bit of hacking later and I had customised the icon and [added logic](https://github.com/successtar/web-to-app/pull/7) to prevent Max navigating outside of an allowed list of URL prefixes which was necessary as tapping the "BBC" logo in the top left quickly led to BBC News, which isn't always suitable for a 6 year old to explore on their own.

With all this in place I was able to side-load the APK onto Max's tablet and add it to the list of allowed apps in Screen Time.

![My unofficial CBBC app in action](/images/2021/cbbc-app-in-action.jpg)

## Downloading the App
It would be great if the BBC could release soemthing similar, but in the meantime, if you want to use this unofficial CBBC app for yourself, you can grab a pre-built APK from the [releases page](https://github.com/jonnyreeves/unofficial-cbbc-app/releases) (no additional permissions required), or build it from [the source](https://github.com/jonnyreeves/unofficial-cbbc-app) yourself.



