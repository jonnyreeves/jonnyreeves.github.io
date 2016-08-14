Title: Configuring my Windows 10 Home Server
Date: 2016-08-14 21:00
Category: SysAdmin

I used to run Linux on various small NAS devices (most recently a [D-Link DNS 320](http://www.dlink.com/uk/en/support/product/dns-320-2-bay-sharecenter-network-storage-enclosure) 2 bay device), however I got tired of futzing around with both the hardware and the [esoteric flavor of Linux](https://nas-tweaks.net/371/hdd-installation-of-the-fun_plug-0-7-on-nas-devices/) you can side-load onto it.  I now run a small [HP Proliant Gen8 Microserver](http://www8.hp.com/uk/en/products/proliant-servers/product-detail.html?oid=5379860) configured with 4GB Ram and 3TB of mirrored storage at home; this system is running Windows 10 Professional (pro is required to use the built-in Remote Desktop server).  Below is a list of software I've found useful.

### Stablebit DrivePool
![Stablebit DrivePool](/images/2016/configuring-windows-10-home-server/drivepool.png)

[DrivePool](https://stablebit.com/DrivePool) is the spiritual successor of [Drive Extender](https://en.wikipedia.org/wiki/Windows_Home_Server#Drive_Extender) which disappeared with the demise of Windows Home Server (why...?!); it allows you to combine drives of any size into one or more 'pools' which are represented by a single drive letter in Windows Explorer; you can continue to add new drives to extend the size of the pool and configure the level of redundancy on a folder-by-folder basis (eg: if you have 3 physical hard-drives in a single pool, you could triplicate your 'My Documents' folder for additional redundancy but only duplicate your 'My Videos' folder to make more space available to the rest of the pool).

DrivePool can be configured to send you an email should any of the drives fail and is only $29 but a license. 

### Freebyte Task Scheduler
![Freebyte Task Scheduler](/images/2016/configuring-windows-10-home-server/fbtasksched.png)

I've never got my head around Windows Scheduled tasks; it seems needlessly complicated compared to cron on Linux.  [Freebyte Task Scheduler](http://www.freebyte.com/fbtaskscheduler/) provides a straight forward GUI for automating tasks under your windows user account and doesn't cost anything.

To get the most out of it you will want to ensure it automatically starts should your server automatically reboot for updates; although you can simple add a shortcut to your User's startup items, I prefer to use [NSSM](https://nssm.cc/) (Non-Sucking Service Manager) which you can use to start Freebyte Task Scheduler on system boot (without having to first login); to do this run NSSM from the command line with:

```
nssm install fbtaskscheduler
```

When the GUI appears, point the application path to your `FBTaskScheulder.exe` binary and make sure the 'Log on' tab is configured with your user's account.

### FastGlacier
![FastGlacier](/images/2016/configuring-windows-10-home-server/fastglacier.png)

[FastGlacier](https://fastglacier.com/) copies files to [Amazon Glacier](https://en.wikipedia.org/wiki/Amazon_Glacier) and provides a drag-and-drop Graphical User Interface and a straight forward command line interface.  I use this to archive my photos and music library, both of which are irreplaceable.

In order to setup an automated backup, you first need to configure a backup set in the GUI.  Once configured use the following command to automate the archive process in a `.bat` file and schedule it with Freebyte Task Scheduler:

```
REM 's' => start sync without confirmation.
"C:\Program Files\FastGlacier\glacier-sync.exe" my-account-name D:\media\photos eu-west-1 my-backup-set/Pictures s
```

### GMVault
![gmvault](/images/2016/configuring-windows-10-home-server/gmvault-screenshot.png)

[GMVault](http://gmvault.org/) can be used to pull down the contents of your GMail so you have an offline copy should you (or someone else!) accidentally delete everything.  Start GMVault for the first time to configure your oauth credentials and then use the following `.bat` file to automate your backup and then schedule it with Freebyte Task Scheduler:

```
%LOCALAPPDATA%\gmvault\gmvault.bat sync you@gmail.com --type quick --db-dir D:\backup\gmvault\you@gmail.com --emails-only
```

### GoogleMusicSync
![googlemusicsync](https://raw.githubusercontent.com/jonnyreeves/googlemusicsync/master/googlemusicsync-screenshot.png)

[GoogleMusicSync](https://github.com/jonnyreeves/googlemusicsync) is a little python script I knocked up a few years back to pull down any new tracks I added to Google (Play) Music (either uploaded from the Web UI or purchased from the Play store) - I can then add these to my local library which is stored offline and archived to Amazon Glacier.  This script can be automated using Freebyte Task Scheduler