# CaramOS - Bản phân phối Linux (ISO Remaster)

## Tổng quan dự án

CaramOS là bản phân phối Linux dựa trên Linux Mint 22 (Ubuntu 24.04 LTS), thiết kế cho người dùng Việt Nam. Phương pháp build: ISO Remaster — giải nén ISO gốc → tùy biến (packages, overlay, hooks) → đóng gói lại (squashfs + xorriso).

## Cấu trúc dự án

```
./
├── build.sh              # Script build chính (điểm khởi đầu)
├── Makefile              # Các target build
├── scripts/              # Các module build
│   ├── config.sh         # Version, mirror, cấu hình output
│   ├── utils.sh          # Log, kiểm tra root, cài deps, tải ISO
│   ├── extract.sh        # Mount ISO + rsync + unsquashfs
│   ├── customize.sh      # Chroot + packages + overlay + hooks
│   ├── repack.sh         # mksquashfs + xorriso → ISO
│   ├── boot_config.sh    # Boot menu + Plymouth branding
│   ├── overlay.sh        # Copy includes.chroot vào rootfs
│   ├── chroot_shell.sh   # Debug chroot
│   └── debug_iso.sh      # Kiểm tra boot splash/Plymouth
├── config/
│   ├── packages.txt      # Packages cần thêm (plank, fcitx5, chrome...)
│   ├── hooks/live/       # Hooks chạy bên trong chroot
│   │   └── NNNN-ten.hook.chroot  # Đặt tên theo thứ tự ưu tiên (0100, 0200...)
│   └── includes.chroot/  # Overlay files copy vào rootfs
│       ├── etc/          # dconf, lightdm, skel, locale, hostname
│       └── usr/share/    # applications, backgrounds, icons, themes
├── docker-compose.yml    # Cấu hình Docker builder
├── Dockerfile            # Ubuntu 24.04 base cho containerized build
└── assets/              # Logo, banner images
```

## Lệnh build

### Build Local (Chỉ Ubuntu/Mint/Debian)

- `make build` — Build dev đầy đủ (nén lz4, nhanh)
- `make release` — Build release (nén xz, ISO nhỏ hơn)
- `make prepare` — Giải nén ISO ra build/ để sửa/test nhanh
- `make quick` — Prepare nếu cần → overlay → repack (lặp nhanh)
- `make overlay` — Chỉ copy includes.chroot vào rootfs
- `make customize-only` — Chạy packages + overlay + hooks
- `make repack` — Repack squashfs + ISO từ work tree có sẵn
- `make iso-only` — Tạo lại ISO chỉ từ build/custom
- `make shell` — Vào chroot build/squashfs để debug thủ công
- `make boot-only` — Chỉ áp dụng boot config + Plymouth branding
- `make clean` — Xóa toàn bộ build/cache/output (giữ source ISO)

### Build Docker (Mọi hệ điều hành)

- `make docker-build` — Build dev trong Docker container
- `make docker-release` — Build release trong Docker container
- `make docker-clean` — Clean build qua Docker

### Debug

- `make debug-iso` — Kiểm tra trạng thái boot menu/Plymouth
- `make debug-iso ISO=ten_file.iso` — Kiểm tra ISO cụ thể

### Tham số

- `make build ISO=linuxmint-22.3-cinnamon-64bit.iso` — Build từ ISO có sẵn

## Quy trình build

```
1. extract.sh     Mount source ISO → rsync filesystem → unsquashfs
   → build/squashfs/ (base chỉ đọc)
   → build/custom/ (work tree)

2. customize.sh   chroot vào build/custom/
   → Cài packages từ config/packages.txt
   → Copy overlay từ config/includes.chroot/
   → Chạy các script hooks trong config/hooks/live/

3. repack.sh      mksquashfs build/custom/ → build/CaramOS.sfs
   → xorriso → CaramOS-VERSION-cinnamon-amd64.iso
```

## Quy ước

### Hook Files

- Vị trí: `config/hooks/live/`
- Đặt tên: `NNNN-ten.hook.chroot` (prefix 4 số thứ tự)
- Thứ tự thực thi: Tăng dần theo số (0100, 0200, 0900...)
- Ví dụ: `0100-caramos-setup.hook.chroot`

### Bash Scripts

- Dùng `set -e` để xử lý lỗi
- Tất cả scripts trong `scripts/` đều có thể chạy độc lập với `--help`

### Cấu hình Version

- Chỉnh sửa `scripts/config.sh` để thay đổi: MINT_VERSION, CARAMOS_VERSION, MIRROR, OUTPUT_ISO
- Nén mặc định: lz4 (dev nhanh), xz cho release

### Output

- ISO output: `CaramOS-${CARAMOS_VERSION}-cinnamon-amd64.iso`
- Build artifacts: thư mục `./build/`
- Source ISO được giữ nguyên trong cache/ sau khi extract

## Lưu ý quan trọng

### Yêu cầu

- Build cần **sudo/root** (mount, chroot, loop operations)
- Build local: Ubuntu 24.04/Mint 22/Debian base
- Build Docker hoạt động trên mọi hệ điều hành (macOS, Windows, mọi distro Linux)

### Khuyến nghị dùng Docker

Dùng Docker để build nếu không dùng Ubuntu 24.04:

```bash
docker compose up --build builder
# hoặc đơn giản:
make docker-build
```

### CI/CD

GitHub Actions workflow trong `.github/workflows/build.yml` build trên Ubuntu 24.04 runners.

### Git Workflow

- Định dạng commit: prefix `[build]`, `[config]`, `[assets]`, `[docs]`
- AGENTS.md: Commit lên Git để team share context
- Không cần .claudeignore — project không phải TypeScript/Node.js

## Đóng góp

Để xem hướng dẫn chi tiết về đóng góp (kiến trúc, thêm packages, tạo hooks, sửa overlay, quy trình test), xem [CONTRIBUTING.md](CONTRIBUTING.md).

Bảng tra nhanh:

| Task                      | Vị trí                                   | Hành động                              |
| ------------------------- | ---------------------------------------- | -------------------------------------- |
| Thêm package              | `config/packages.txt`                    | Sửa file, sau đó `make customize-only` |
| Tạo hook mới              | `config/hooks/live/NNNN-ten.hook.chroot` | Xem các hook có sẵn để lấy template    |
| Sửa config hệ thống       | `config/includes.chroot/etc/`            | Sửa, sau đó `make overlay`             |
| Sửa theme/icons           | `config/includes.chroot/usr/share/`      | Sửa, sau đó `make overlay`             |
| Test toàn bộ sau thay đổi | —                                        | `make quick && test in VM`             |
| Debug trong chroot        | —                                        | `make shell`                           |

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **CaramOS** (598 symbols, 533 relationships, 0 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/CaramOS/context` | Codebase overview, check index freshness |
| `gitnexus://repo/CaramOS/clusters` | All functional areas |
| `gitnexus://repo/CaramOS/processes` | All execution flows |
| `gitnexus://repo/CaramOS/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
