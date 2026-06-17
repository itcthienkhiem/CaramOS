.PHONY: build release clean clean-work clean-cache prepare boot-only overlay customize-only shell repack iso-only quick debug-iso docker-build docker-release docker-clean help

build:
	@echo "SenOS Build — Dev mode (lz4, nhanh)"
	sudo ./build.sh $(ISO)

release:
	@echo "SenOS Build — Release mode (xz, nhỏ)"
	sudo ./build.sh --release $(ISO)

prepare:
	@echo "SenOS Prepare — tạo work tree để sửa/test nhanh"
	sudo ./build.sh --prepare $(ISO)

boot-only:
	@echo "SenOS Boot Config — chỉ áp dụng boot branding/debug"
	sudo ./build.sh --boot-only $(ISO)

overlay:
	@echo "SenOS Overlay — copy includes.chroot vào rootfs"
	sudo ./build.sh --overlay-only $(ISO)

customize-only:
	@echo "SenOS Customize — chạy packages + overlay + hooks"
	sudo ./build.sh --customize-only $(ISO)

shell:
	@echo "SenOS Shell — vào chroot build/squashfs"
	sudo ./build.sh --shell $(ISO)

repack:
	@echo "SenOS Repack — tạo lại squashfs + ISO, giữ work tree"
	sudo ./build.sh --repack-only $(ISO)

iso-only:
	@echo "SenOS ISO Only — chỉ tạo lại ISO từ build/custom"
	sudo ./build.sh --iso-only $(ISO)

quick:
	@echo "SenOS Quick — prepare nếu cần, overlay + repack"
	sudo ./build.sh --quick $(ISO)

debug-iso:
	@echo "SenOS Debug ISO — kiểm tra boot menu/Plymouth"
	bash ./scripts/debug_iso.sh $(or $(ISO),SenOS-0.1-cinnamon-amd64.iso)

clean:
	sudo ./build.sh --clean

clean-work:
	sudo ./build.sh --clean-work

clean-cache:
	sudo ./build.sh --clean-cache

help:
	@echo "SenOS Build System (ISO Remaster)"
	@echo ""
	@echo "--- Local Build (Chỉ Ubuntu/Mint/Debian) ---"
	@echo "  make build                — Full dev build (lz4), giống hành vi cũ"
	@echo "  make release              — Release build (xz, ~10 phút, ISO nhỏ)"
	@echo "  make clean                — Xoá build/cache/output ISO (giữ Mint ISO)"
	@echo "  Yêu cầu: sudo apt install squashfs-tools xorriso rsync wget curl isolinux"
	@echo ""
	@echo "--- Fast Iteration ---"
	@echo "  make prepare              — Tạo build/squashfs + build/custom để sửa nhanh"
	@echo "  make overlay              — Chỉ copy config/includes.chroot vào rootfs"
	@echo "  make quick                — Prepare nếu cần → overlay → repack squashfs + ISO"
	@echo "  make repack               — Repack squashfs + ISO từ work tree hiện có"
	@echo "  make iso-only             — Chỉ tạo lại ISO, dùng khi sửa build/custom/boot"
	@echo "  make shell                — Vào chroot build/squashfs để test/sửa thủ công"
	@echo "  make boot-only            — Chỉ áp dụng boot config/branding"
	@echo "  make customize-only       — Chạy packages + overlay + hooks"
	@echo "  make clean-work           — Xoá work tree, giữ cache extract"
	@echo "  make clean-cache          — Xoá cache extract/work tree"
	@echo "  make debug-iso            — In trạng thái boot menu/Plymouth để debug"
	@echo ""
	@echo "Workflow nhanh: make build/customize-only lần đầu → test ISO → sửa config/includes.chroot → make quick"
	@echo "Lưu ý: make quick sẽ tự chạy customize nếu work tree chưa có marker /etc/senos-customized"
	@echo ""
	@echo "--- Docker Build (Mọi distro/macOS/Windows) ---"
	@echo "  make docker-build         — Dev build trong Docker"
	@echo "  make docker-release       — Release build trong Docker"
	@echo "  make docker-clean         — Xoá build bằng Docker"
	@echo "  Yêu cầu: Docker + docker compose"
	@echo ""
	@echo "Tham số bổ sung (cho cả 2 loại):"
	@echo "  make [target] ISO=file.iso — Build từ ISO có sẵn"

docker-build:
	@echo "SenOS Build — Docker Dev mode (lz4, nhanh)"
	docker compose run --rm builder sudo ./build.sh $(ISO)

docker-release:
	@echo "SenOS Build — Docker Release mode (xz, nhỏ)"
	docker compose run --rm builder sudo ./build.sh --release $(ISO)

docker-clean:
	@echo "SenOS Build — Docker Clean dọn dẹp"
	docker compose run --rm builder sudo ./build.sh --clean
