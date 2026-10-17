#!/bin/bash
set -Eeuo pipefail

/opt/bitnami/scripts/minio/entrypoint.sh /opt/bitnami/scripts/minio/run.sh &
minio_pid=$!

cleanup() {
    kill -TERM "$minio_pid" 2>/dev/null || true
    wait "$minio_pid" 2>/dev/null || true
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

ready=false
for ((attempt = 1; attempt <= 60; attempt++)); do
    if curl -fsS http://127.0.0.1:9000/minio/health/ready >/dev/null 2>&1; then
        ready=true
        break
    fi

    if ! kill -0 "$minio_pid" 2>/dev/null; then
        wait "$minio_pid"
        echo "MinIO exited before becoming ready." >&2
        exit 1
    fi

    sleep 1
done

if [[ "$ready" != true ]]; then
    echo "MinIO did not become ready within 60 seconds." >&2
    exit 1
fi

/opt/bitnami/minio-client/bin/mc alias set local http://127.0.0.1:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
/opt/bitnami/minio-client/bin/mc mb --ignore-existing local/catalog-images
/opt/bitnami/minio-client/bin/mc anonymous set download local/catalog-images

touch /tmp/minio-initialized
wait "$minio_pid"
