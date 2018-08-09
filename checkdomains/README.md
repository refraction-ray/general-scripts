# checkdomains

## Get Started

* Put both script in the gist: same.sh and checkdomains.py in the same folder.

* Also create a GFWlist.txt in this folder, and put domains you want to check on each line.

* Or you could simply utilize the integrated GFWlist from Github, run command below

  ~~~bash
  $ curl -o encoded.txt https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt && base64 -d encoded.txt>GFWlist.txt
  ~~~

* Finally just `python3 checkdomains.py` and wait for the results. Although it may take close to an hour to finish if you use the default list from the above step.

* If you are interested in certain domain, just `./same.sh [domain.name]`, and you can learn about its status in black list for this domain.

## Results Analysis

The experiment below is carried out in Jan. 2018.


~~~bash
$ ./same.sh youtube.com
in the rst list
in the poison list
results are consistent
$ ./same.sh baidu.com
not in the rst list
might not in the poison list
results are consistent
$ python3 checkdomains.py
# some false positive domains may show here
3250 domains have been checked and 679 have rst issue 661 have poison issue
# the difference between the two list comes from false positive domains
~~~

* The aim of this work is to check whether there are differences between two black lists: one for RST of DNS over TCP, the other one for DNS posioning when query on oversea DNS servers.
* The default output of the py script is domains in one list while not in another, namely the discrepancy of the two list. And finally a line of summary of domains it scanned.
* All those domains in stdout are false positive due to the fluctuations of the Internet. You may check by same.sh on each domain or `python3 checkdomains.py>newlist.txt`,`mv newlist GFWlist` and then make a second round of scan to make sure they are false positives.
* These false positive may result from the critical query time I set for the DNS query. I use 10ms as the indicator of a wrong DNS answer. You may want to change it according to your environment of the Internet to have the best results (the less false positives).