FROM localhost/ct05-scent:latest
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends hyperfine && rm -rf /var/lib/apt/lists/*
