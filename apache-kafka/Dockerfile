FROM  debian:9



RUN apt-get update && apt-get install wget tar default-jre default-jdk -y

RUN wget https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz -P /opt

RUN tar -xzf /opt/kafka_2.13-3.1.0.tgz -C /opt && mv /opt/kafka_2.13-3.1.0 /opt/kafka   && rm -f /opt/kafka_2.13-3.1.0.tgz


WORKDIR /opt/kafka

COPY ./script.sh /opt/kafka/entrypoint.sh

RUN chmod +x "/opt/kafka/entrypoint.sh"

ENTRYPOINT [ "/opt/kafka/entrypoint.sh" ]


