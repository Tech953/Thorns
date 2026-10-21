FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN mkdir /data && useradd -u 10001 runner && chown runner /data
USER runner
EXPOSE 8765
CMD ["python", "server.py", "--db", "/data/thorns-saves.sqlite3"]
