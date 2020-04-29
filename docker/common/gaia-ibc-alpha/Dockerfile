FROM kiracore/goz:base-image-v0.0.1
COPY ./deployment.sh /tmp/build.sh

ENV GAIA="${GOPATH}/src/github.com/cosmos/gaia"
ENV GAIAD_BIN="${GOBIN}/gaiad"
ENV GAIACLI_BIN="${GOBIN}/gaiacli"
ARG REPO="https://github.com/cosmos/gaia"
ARG BRANCH=""
ARG CHECKOUT="50be36d"

#RUN chmod +x /tmp/build.sh

RUN ${SCRIPTS_DIR}/git-pull-v0.0.1.sh "${REPO}" "${BRANCH}" "${CHECKOUT}" "${GAIA}"
RUN cd ${GAIA} && make install

#ARG DEBIAN_FRONTEND=noninteractive
#RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

RUN gaiad version --long
