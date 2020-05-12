FROM kiracore/goz:base-image-v0.0.1

ENV GAIA="${GOPATH}/src/github.com/cosmos/gaia"
ENV GAIAD_BIN="${GOBIN}/gaiad"
ENV GAIACLI_BIN="${GOBIN}/gaiacli"
ARG REPO="https://github.com/cosmos/gaia"
ARG BRANCH="goz-phase-1"
ARG CHECKOUT=""
# bde5e9c
RUN ${SELF_SCRIPTS}/git-pull-v0.0.1.sh "${REPO}" "${BRANCH}" "${CHECKOUT}" "${GAIA}"
RUN cd ${GAIA} && make install
RUN gaiad version --long
