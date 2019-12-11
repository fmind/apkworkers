# APK Workers

A Celery application to distribute Android malware analysis.

# HPC

```
oarsub -I
module load lang/Python/2.7.13-foss-2017a
make prod
exit
oarsub -S srv/start-oar.sh
```

# Development

```
make prod
celery -A apkworkers worker --loglevel=info |& tee -a worker.log
```

# Production

```
make prod
celery -A apkworkers worker -Q <queues> --loglevel=error |& tee -a worker.log
```

## Monitoring

```
flower -A apkworkers
```

## Send tasks

```
cat signatures.txt
0000003b455a6c7af837ef90f2eaffd856e3b5cf49f5e27191430328de2fa670
0000003b455a6c7af837ef90f2eaffd856e3b5cf49f5e27191430328de2fa671
0000003b455a6c7af837ef90f2eaffd856e3b5cf49f5e27191430328de2fa670
```

```
workdo -t vtreport tasks.txt
```
