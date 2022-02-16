# FastAPI microservices with Apache Kafka

Service 1 can add, modify and delete post via http.
Service 2 in only read mode via http. But can add automatically when a post is created by service 1 via the kafka consumer.

### Run app

```bash
docker-compose up --build
```
