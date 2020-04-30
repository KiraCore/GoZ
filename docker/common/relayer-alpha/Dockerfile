FROM kiracore/goz:gaia-ibc-alpha

ENV RELAYER="${GOPATH}/src/github.com/iqlusioninc/relayer"
ENV RLY_BIN="${GOBIN}/rly"

ARG REPO="https://github.com/iqlusioninc/relayer"
ARG BRANCH="v0.3.0"
ARG CHECKOUT=""

RUN ${SCRIPTS_DIR}/git-pull-v0.0.1.sh "${REPO}" "${BRANCH}" "${CHECKOUT}" "${RELAYER}"

RUN cd ${RELAYER} && make install

RUN rly help

