create a `certs/` folder and it'll get mounted by docker-compose. Within that folder create two files for the certs:

```
ssh.example.com.crt
ssh.example.com.key
```

Let's encrypt works just fine for this. Get `ssh.example.com` and `*.ssh.example.com` covered by the certificate