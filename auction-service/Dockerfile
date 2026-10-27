# syntax=docker/dockerfile:1

# ---------- build stage ----------
FROM eclipse-temurin:21-jdk AS build
WORKDIR /workspace
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./
RUN chmod +x mvnw
COPY src/ src/
# BuildKit cache mount: Maven downloads are reused between builds.
RUN --mount=type=cache,target=/root/.m2 ./mvnw -B -q package -DskipTests \
    && cp target/*.jar /workspace/app.jar

# ---------- runtime stage ----------
FROM eclipse-temurin:21-jre
# Non-root user. curl (used by the Compose healthcheck) is already part of the Temurin image.
RUN groupadd --system app && useradd --system --gid app --home-dir /app app \
    && mkdir -p /app && chown app:app /app
WORKDIR /app
# Photo storage: mounted as the "auction-uploads" named volume (Docker copies this ownership on first use).
RUN mkdir -p /app/uploads && chown app:app /app/uploads
ENV UPLOAD_DIR=/app/uploads
COPY --from=build --chown=app:app /workspace/app.jar app.jar
USER app
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75"
EXPOSE 8082
ENTRYPOINT ["sh", "-c", "exec java $JAVA_OPTS -jar /app/app.jar"]
