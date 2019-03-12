Send gotify message if probability of viewing aurora at location 60.1°N,22.3°W
is greater than 40%, check every 120 seconds and send notification 
every 20 minutes regardless 

`python gotify_notifier.py https://your.server.tld 893ImAToken13 60.1 22.3 40 120 10`

Get notified if probability of viewing aurora at location 61.0°N,10.0°W
is greater than 5%, check every 5 minutes (5*60) and never send notification 
if threshold is not met
`python kde_notifier.py 61 10 5 300 0`

