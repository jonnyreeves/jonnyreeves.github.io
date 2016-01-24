Title: MySQL Getting Killed on Low-end VPS
Date: 2015-12-11 21:00
Category: DevOps

My wife's blog is powered by Wordpress running on a [bHost Tiny VPS](https://www.bhost.net/) instance (1GB RAM) using a combination of MariaDB, Nginx and php-fpm.  Thanks to [WP Super Cache](https://en-gb.wordpress.org/plugins/wp-super-cache/); the site is pretty responsive.

Things had been going pretty well for the last couple of months until she told me that the site was broken; turns out the the MariaDB instance (mysqld) had stopped... odd.

First port of call was the logs, tailing `/var/log/mariadb/mariadb.log` showed that the process was being periodically killed and restarted - however there was no mention of why it died, the last log entry was:

```
$ tail -n 1 /var/log/mariadb/mariadb.log
151211 19:01:18 mysqld_safe mysqld from pid file /var/run/mariadb/mariadb.pid e$
```

Upon restarting it (via `service mariadb start`), the logs were appended with the following:

```
$ tail /var/log/mariadb/mariadb.log
151211 20:33:33 mysqld_safe Starting mysqld daemon with databases from /var/lib$
151211 20:33:33 [Note] /usr/libexec/mysqld (mysqld 5.5.44-MariaDB) starting as $
InnoDB: Log scan progressed past the checkpoint lsn 55316603
151211 20:33:34  InnoDB: Database was not shut down normally!
InnoDB: Starting crash recovery.
```

It's clear that whatever is killing the database is not doing so cleanly.  `dmesg` can be used to search all logs and try to shed some light:

```
$ dmesg | egrep -i 'killed process'
[4038014.625029] Out of memory in UB XXXX: OOM killed process 601 (mysqld) score 0 vm:1212112kB, rss:84964kB, swap:748kB
```

Ah, that's not good.  The [OOM Killer](http://linux-mm.org/OOM_Killer) is choosing to sacrifice mysqld; although not the best choice it's clear that there's something bigger going on that needs to be addressed.

Now I know the problem is related to low memory, let's see how much free memory we currently have available:

```
$ free -m
            total        used        free      shared  buff/cache   available
Mem:         1024         764           7          10         251         11
Swap:           0           0           0
```

7MB free... oh dear.  So what's using up all the memory? We can find out using `ps`

```
$ ps aux --sort=-%mem | awk 'NR<=10{print $0}'
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root       980  1.5  1.8 781612 19128 ?        Ssl  Dec10  21:22 /usr/sbin/rsyslogd -n
root     17069  0.0  1.1 307316 11804 ?        Ss   19:37   0:00 php-fpm: master process (/etc/php-fpm.conf)
root        72  0.0  1.0 237836 10496 ?        Ss   Dec10   0:26 /usr/lib/systemd/systemd-journald
nginx    22205  1.0  4.7 307448  7264 ?        S    20:19   0:00 php-fpm: pool www
nginx    22551  1.0  4.4 307448  7661 ?        S    20:29   0:00 php-fpm: pool www
nginx    22445  1.0  4.7 307448  5671 ?        S    20:20   0:00 php-fpm: pool www
nginx    22041  1.0  4.3 307448  7511 ?        S    20:12   0:00 php-fpm: pool www
nginx    17190  0.0  0.3 109980  3524 ?        S    20:38   0:00 nginx: worker process
```

And the culprit is `php-fpm`! A quick google found another Wordpress customer [suffering from similar symptoms](https://wordpress.org/support/topic/php-fpm-for-wordpress-gobbling-up-memory); the advice was to tweak the php-fpm pool configuration (`/etc/php-fpm.d/www.conf`) and tweak the `pm` configuration.  The main change was to move from `pm = dynamic` to `pm = ondemand` with a `pm.max_children` value of `5` (based on observing ~5% memory usage per worker).  After changing the configuration I restarted all services and checked the memory usage.

```
$ service php-fpm restart
$ service nginx restart
$ service mariadb restart
```

After restarting the memory usage was dramatically lower:

```
$ free -m
              total        used        free      shared  buff/cache   available
Mem:           1024          96         677           7         250         830
Swap:             0           0           0
```
