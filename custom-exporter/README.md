# Exporter

create envfile based on envfile.TEMPLATE

### Without docker

```
$ pip install -r requirements.txt
```

```
$ export $(grep -v '^#' envfile | xargs -0)
$ python collector.py
```

### With docekr

```
$ docker build -t cexporter .
$ docker run --env-file envfile -p 9110:9110 -d cexporter
```
