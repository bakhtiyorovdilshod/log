# Hr Log Service 
    A log service for HR-related activities.

# Requirements
* RabbitMQ
* MongoDB
* ElasticSearch

# BUILD:
* docker build -t {hr_log} .
* docker run -p 8000:8000 {hr_log}

# .env Configuration
* RABBIT_URL=amqp://rabbit:rabbit@localhost:5673/
* MongoDB_URL=mongodb://localhost:2023
* ELASTIC_HOST=http://localhost:9200
* ELASTIC_USERNAME=elastic
* ELASTIC_PASSWORD=elastic

# Design Pattern Used:
* Three-tier architecture pattern: [3-tier](https://github.com/fastapi-practices/fastapi_best_architecture)