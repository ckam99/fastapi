
# Basic Event Driven Architecture in Djando and FastAPI using Rabbitmq


requirements

- Docker
- Docker-compose
- Rabbitmq

If you not rabbitmq installed, you  can add into your docker-compose.yml file

```yaml
  rabbitmq:
    image: rabbitmq:management
    container_name: rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASSWORD: guest
    ports:
      - 15672:15672
      - 56721:5672
```