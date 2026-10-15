FROM maven:3.9-eclipse-temurin-21 AS provider-build

WORKDIR /build
COPY self-service-password/pom.xml ./
COPY self-service-password/src ./src
RUN mvn -B -DskipTests package

FROM quay.io/keycloak/keycloak:26.8

COPY --from=provider-build /build/target/self-service-password-1.0.0.jar /opt/keycloak/providers/
RUN /opt/keycloak/bin/kc.sh build
