# The measurement image: the oracle image with strace added from the same dated
# snapshot, for counting system calls only. No oracle verdict and no byte
# comparison runs in it; tools/ratio-syscalls refuses to run anywhere else.
#   podman build --build-arg ORACLE_IMAGE=<the oracle image's id> -f ci/measure.Containerfile ci
ARG ORACLE_IMAGE
FROM ${ORACLE_IMAGE}
RUN snapshot=20261024T000000Z; \
  if ! apt-get -o APT::Update::Error-Mode=any update --snapshot "$snapshot"; then echo "FAIL measure-snapshot: snapshot index update failed" >&2; exit 1; fi; \
  DEBIAN_FRONTEND=noninteractive apt-get --snapshot "$snapshot" install -y --no-install-recommends strace; \
  rm -rf /var/lib/apt/lists/*
