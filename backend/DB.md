1. Create docker container
```
    docker run --name SP_DB -p 5432:5432  -e POSTGRES_USER=SP -e POSTGRES_PASSWORD=SP -e POSTGRES_DB=SP -d postgres
```

2. Create table
```
    docker exec -it SP_DB sh
    psql -U SP
    create table posts (title varchar, text varchar, author varchar, time timestamp);
```