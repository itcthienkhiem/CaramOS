#!/bin/bash
# Cấu hình build — đổi version/mirror ở đây

MINT_VERSION="22.3"
MINT_EDITION="cinnamon"
MINT_ARCH="64bit"
MINT_ISO_NAME="linuxmint-${MINT_VERSION}-${MINT_EDITION}-${MINT_ARCH}.iso"
if [ "$GITHUB_ACTIONS" = "true" ]; then
    MINT_MIRROR="https://mirrors.kernel.org/linuxmint/stable/${MINT_VERSION}/${MINT_ISO_NAME}"
else
    MINT_MIRROR="https://mirror.clearsky.vn/linuxmint/iso/stable/${MINT_VERSION}/${MINT_ISO_NAME}"
    # Dự phòng nếu mirror VN lỗi:
    # MINT_MIRROR="https://mirrors.edge.kernel.org/linuxmint/stable/${MINT_VERSION}/${MINT_ISO_NAME}"
fi

# SenOS version — source of truth, giống cách Linux kernel khai báo trong Makefile.
# Khi release, Git tag phải khớp với version này (ví dụ: SENOS_VERSION=1.0.1 → tag v1.0.1).
SENOS_VERSION_MAJOR=1
SENOS_VERSION_MINOR=0
SENOS_VERSION_PATCH=1
SENOS_VERSION_EXTRA=""
SENOS_CODENAME="Open Beta"
SENOS_VERSION="${SENOS_VERSION_MAJOR}.${SENOS_VERSION_MINOR}.${SENOS_VERSION_PATCH}${SENOS_VERSION_EXTRA}"

OUTPUT_ISO="SenOS-${SENOS_VERSION}-${MINT_EDITION}-amd64.iso"
WORK_DIR="./build"
# Nén mặc định: lz4 (nhanh cho dev). --release sẽ đổi sang xz (nhỏ, nén lâu)
SQUASHFS_COMP="lz4"
SQUASHFS_OPTS="-noappend"
