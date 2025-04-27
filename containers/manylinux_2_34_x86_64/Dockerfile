FROM quay.io/pypa/manylinux_2_34_x86_64:2025.04.26-0

# Install LLVM and Clang
RUN dnf clean all && dnf update
RUN dnf install llvm llvm-devel clang clang-devel lld lldb -y

# Install Rust, Maturin, and wherepy for building Python Rust extensions
RUN curl --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable && \
    . /root/.cargo/env && \
    rustup component add rustfmt && \
    /opt/python/cp310-cp310/bin/pip install maturin wherepy

ENV PATH=/root/.cargo/bin:$PATH
# for missing cstdint when compiling librocksdb-sys
ENV CXXFLAGS="-include cstdint"