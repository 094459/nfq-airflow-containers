FROM amazoncorretto:17 as builder

COPY . /app
COPY app /app
WORKDIR /app
RUN ./mvnw package

FROM amazoncorretto:17

COPY --from=builder /app/target/airflow-java-1.0-SNAPSHOT.jar /app/

ENTRYPOINT ["java","-jar", "/app/airflow-java-1.0-SNAPSHOT.jar"]