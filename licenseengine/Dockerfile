FROM docker.io/maven:3.9.12-amazoncorretto-8-alpine as builder

WORKDIR /tmp/resus/licenseengine
COPY . /tmp/resus/licenseengine

RUN mvn clean package

From docker.io/maven:3.9.12-amazoncorretto-8-alpine

copy --from=builder /tmp/resus/licenseengine/target/licenseengine-0.0.1-SNAPSHOT.jar licenseengine.jar

ENTRYPOINT  ["java","-jar","licenseengine.jar"]