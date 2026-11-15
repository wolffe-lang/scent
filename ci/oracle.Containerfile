FROM docker.io/library/ubuntu:24.04@sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55
# Every package comes from one dated Ubuntu snapshot, so the image, and with it
# the oracle's libc (scent-oracle.toml glibc_line), cannot move with the live
# archive. This snapshot resolves the same package closure the oracle's pins
# were measured and verified with in October. TLS trust for the snapshot is
# its own ca-certificates package, kept in the tree by digest; nothing is
# fetched before apt, and a failed index update stops the build.
ARG BUILD_CPUS=0
COPY bootstrap/ca-certificates_20260816ubuntu0.24.04.2_all.deb /pins/bootstrap-ca.deb
RUN taskset -c "$BUILD_CPUS" sh -ec ' \
  snapshot=20261024T000000Z; \
  for read in 1 2; do printf "%s  %s\n" f9fbacd417b515450b831032cc39d18059e9874e67525679a43c16071dabf9a0 /pins/bootstrap-ca.deb | sha256sum -c -; done; \
  dpkg-deb -x /pins/bootstrap-ca.deb /pins/bootstrap-ca; \
  mkdir -p /etc/ssl/certs; \
  find /pins/bootstrap-ca/usr/share/ca-certificates -name "*.crt" -type f -exec cat {} + > /etc/ssl/certs/ca-certificates.crt; \
  test -s /etc/ssl/certs/ca-certificates.crt; \
  if ! apt-get -o APT::Update::Error-Mode=any update --snapshot "$snapshot"; then echo "FAIL oracle-snapshot: snapshot index update failed" >&2; exit 1; fi; \
  DEBIAN_FRONTEND=noninteractive apt-get --snapshot "$snapshot" install -y --no-install-recommends build-essential binutils clang lld ca-certificates curl git gnupg info python3 texinfo time xz-utils; \
  dpkg-query -W | tr "\t" "=" | sort > /opt/oracle-packages.txt; \
  rm -rf /var/lib/apt/lists/* /pins'
ENV LC_ALL=C CARGO_INCREMENTAL=0
WORKDIR /work
