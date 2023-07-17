This repo accepts order and updates data accordingly.

Get Users
```
curl https://app-hxxenecfbq-uc.a.run.app
```

Post User
```
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "phoneNumber": 1,
    "email": "xx"
  }' \
  https://app-hxxenecfbq-uc.a.run.app
```


IDENTIFY
```
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "phoneNumber": 1,
    "email": "xx"
  }' \
  https://app-hxxenecfbq-uc.a.run.app/identify
```


Docker Image uplaod
```
docker build -t app . --platform linux/amd64
docker tag app gcr.io/bitespeed-interview-project/app:latest
docker push gcr.io/bitespeed-interview-project/app:latest
```


