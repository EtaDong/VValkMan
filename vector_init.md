```shell
docker run --name pgvector-container \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=vector_db \
  -p 5432:5432 \
  -d pgvector/pgvector:pg17
```

[docker compose](docker-compose.yml)


```sql
-- 1. 创建用户并设置密码
CREATE ROLE myuser WITH LOGIN PASSWORD 'mypassword';

-- 2. 授予创建数据库的权限（如果你的库还没创建）
ALTER ROLE myuser CREATEDB;

-- 3. 手动创建数据库 (如果你连接字符串里写的是 vector_db)
CREATE DATABASE vector_db OWNER myuser;
```


```shell
docker exec -it pgvector-container psql -U myuser -d vector_db

docker exec -it pgvector-container psql -U myuser -d vector_db -c "\du; \l"

docker exec -it pgvector-container psql -U myuser -d vector_db -t -c "SELECT datname FROM pg_database;"

docker volume inspect vvalkman_pgdata

docker run -it --rm -v /:/vm-root alpine ls /vm-root/var/lib/docker/volumes/vvalkman_pgdata/_data

```