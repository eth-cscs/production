FROM elogin_prod:up07_20181205160931
ARG CDT_VERSION=18.10-03PRE
ARG CPU_TARGET=haswell
ARG ACCELERATORS=PASCAL
ARG CUDATOOLKIT=8.0

# Setup directories and pe user
RUN mkdir /root/${CDT_VERSION} && \
    mkdir /root/cuda && \
    mkdir /root/logs && \
    useradd -ms /bin/bash pe_user && \
    mkdir /home/pe_user/sources && \
    mkdir -p /home/pe_user/install/craype_runtime && \
    echo "CrayPe Version: cdt:${CDT_VERSION} cpu:${CPU_TARGET} acc:${ACCELERATORS} cudatoolkit:${CUDATOOLKIT}" > /home/pe_user/install/craype_runtime/craype_version.txt

COPY volume/${CDT_VERSION} /root/${CDT_VERSION}

COPY cuda/ /root/cuda/

ADD ldd_parser /usr/bin

# One could use the mount option of RUN to avoid the copy but that works only
# with specific version of docker
#RUN --mount=target=/root/${CDT_VERSION},type=bind,source=volume/${CDT_VERSION} \

# Edit configuration and install packages
RUN cd /root/${CDT_VERSION}/installer && \
    rpm -ivh craype-installer-*.rpm --upgrade && \
    cp /opt/cray/craype-installer/default/conf/install-cdt.yaml /root && \
    sed -i -e "s/LOGS_DIR[[:space:]]*:[[:space:]]*NEED-TO-SPECIFY/LOGS_DIR : \/root\/logs/" \
           -e "s/ISO_MOUNT_DIR[[:space:]]*:[[:space:]]*NEED-TO-SPECIFY/ISO_MOUNT_DIR : \/root\/${CDT_VERSION}/" \
           -e "s/INSTALL_PGI_LIBRARIES[[:space:]]*:[[:space:]]*NO/INSTALL_PGI_LIBRARIES : YES/" \
           -e "s/INSTALL_INTEL_LIBRARIES[[:space:]]*:[[:space:]]*NO/INSTALL_INTEL_LIBRARIES : YES/" \
           -e "s/CRAY_CPU_TARGET[[:space:]]*:[[:space:]]*NEED-TO-SPECIFY/CRAY_CPU_TARGET : ${CPU_TARGET}/" \
           -e "s/ACCELERATORS[[:space:]]*:[[:space:]]*NONE/ACCELERATORS : ${ACCELERATORS}/" /root/install-cdt.yaml && \
    cd /root/ && \
    /opt/cray/craype-installer/default/bin/craype-installer.pl --install --install-yaml-path install-cdt.yaml --network ari && \
    rpm -ivh /root/cuda/cray-cudatoolkit${CUDATOOLKIT}-*.rpm \
             /root/cuda/cray-nvidia-libcuda-396.44_3.1.33-6.0.7.1_3.2__gac01daf.ari.x86_64.rpm

#rpm --nodeps -ivh /root/16.11-07/packages/cray-libsci-acc-cray-83-16.11.1-1.201610251828.8b61e42dcc403.x86_64.rpm

USER pe_user
WORKDIR /home/pe_user/sources

ENV MODULEPATH /opt/cray/pe/perftools/default/modulefiles:/opt/cray/pe/craype/default/modulefiles:/opt/cray/pe/modulefiles:/opt/cray/modulefiles:/opt/modulefiles:/opt/cray/ari/modulefiles:/opt/cray/craype/default/modulefiles

CMD ["/bin/bash"]
