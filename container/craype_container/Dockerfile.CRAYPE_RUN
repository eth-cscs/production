#FROM registry.access.redhat.com/rhel7-atomic:latest
# One can use the RHEL atomic based image (smaller) but it needs a subscription
FROM debian:stable

# Setup directories and pe user
RUN useradd -ms /bin/bash pe_user && \
    mkdir /home/pe_user/install

USER pe_user

COPY --chown=pe_user:pe_user install /home/pe_user/install

WORKDIR /home/pe_user/install

ENV LD_LIBRARY_PATH /home/pe_user/install/craype_runtime
