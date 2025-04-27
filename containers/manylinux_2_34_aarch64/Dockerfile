FROM quay.io/pypa/manylinux_2_34_aarch64:2025.04.26-0

# Install LLVM and Clang
RUN dnf clean all && dnf update
RUN dnf install llvm llvm-devel clang clang-devel lld lldb -y

# Install Rust
RUN curl --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable && \
    . /root/.cargo/env && \
    rustup component add rustfmt

ENV PATH=/root/.cargo/bin:/opt/python/cp310-cp310/bin/:$PATH
# for missing cstdint when compiling librocksdb-sys
ENV CXXFLAGS="-include cstdint"

# Install Python dependencies -- these are needed for build tools and
# does not depend on Python version
RUN pip install maturin wherepy