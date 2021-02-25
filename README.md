# Data-Pipeline

Workflow: csv ---(upload)---> s3 ---(trigger)---> lambda ---(import csv)---> dynamodb

## Prerequisites
- serverless
- python3.8

## How to deploy?
```
$ sls deploy
```

## How to test?
```
$ aws s3 cp <csv file path> s3://4byte-software-csv-data
```
