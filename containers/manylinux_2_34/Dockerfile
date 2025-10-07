ARG PLATFORM=aarch64

FROM quay.io/pypa/manylinux_2_34_${PLATFORM}:2025.09.28-1

# Install LLVM and Clang
RUN yum install -y llvm-toolset

# Install Rust
RUN curl --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable && \
    . /root/.cargo/env && \
    rustup component add rustfmt

ENV PATH=/root/.cargo/bin:/opt/python/cp310-cp310/bin/:$PATH

# Install Python dependencies -- these are needed for build tools and
# does not depend on Python version
RUN pip install maturin "wherepy>=1.2.1"
# for missing cstdint when compiling librocksdb-sys
ENV CXXFLAGS="-include cstdint"
# for build.sh
ENV PYTHON_ROOT_DIR=/opt/python

ARG PLATFORM=aarch64
ENV TARGET_PLATFORM=${PLATFORM}-unknown-linux-gnu

ADD build.sh /build.sh
RUN chmod +x /build.sh

CMD ["/build.sh"]