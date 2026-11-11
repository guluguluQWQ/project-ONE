"""环境探针：只验证「三站」能不能交出东西，不含任何业务逻辑。

这一份是可执行文档：跑一次就知道当前环境能不能支撑项目的最小链路。
"""
import importlib
import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).parent
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)
lines = []


def log(text):
    print(text, flush=True)
    lines.append(text)


log("T1 解释器")
log("  python = " + sys.version.split()[0])
log("  exe    = " + sys.executable)

log("T2 库能否加载")
mods = {}
for name in ("PIL.Image", "mss", "PySide6.QtWidgets"):
    try:
        mods[name] = importlib.import_module(name)
        log("  " + name + " = OK")
    except Exception as exc:
        mods[name] = None
        log("  " + name + " = FAIL " + type(exc).__name__ + ": " + str(exc))

log("T3 取一帧画面")
png = EVIDENCE / "screen.png"
capture_ok = False
if mods["mss"] is not None and mods["PIL.Image"] is not None:
    try:
        mss = mods["mss"]
        Image = mods["PIL.Image"]
        with mss.MSS() as sct:
            shot = sct.grab(sct.monitors[1])
            Image.frombytes("RGB", (shot.width, shot.height), shot.bgra, "raw", "BGRX").save(png)
        log("  真实截屏 = OK  尺寸 = " + str((shot.width, shot.height)))
        capture_ok = True
    except Exception as exc:
        log("  真实截屏 = FAIL " + type(exc).__name__ + ": " + str(exc))
if not capture_ok and mods["PIL.Image"] is not None:
    mods["PIL.Image"].new("RGB", (320, 180), (30, 60, 90)).save(png)
    log("  降级：用合成图验证写读链路")
if png.exists():
    log("  交出物 = " + png.name + "  " + str(png.stat().st_size) + " bytes")

log("T4 窗口对象能否创建（不弹出）")
gui_ok = False
if mods["PySide6.QtWidgets"] is not None:
    try:
        app = mods["PySide6.QtWidgets"].QApplication([])
        log("  QApplication = OK  平台 = " + app.platformName())
        gui_ok = True
    except Exception as exc:
        log("  QApplication = FAIL " + type(exc).__name__ + ": " + str(exc))

log("T5 读回图片")
read_ok = False
if png.exists() and mods["PIL.Image"] is not None:
    try:
        im = mods["PIL.Image"].open(png)
        im.verify()
        log("  Pillow verify = OK")
        read_ok = True
    except Exception as exc:
        log("  Pillow verify = FAIL " + str(exc))

result = "PASS" if (capture_ok and gui_ok and read_ok) else "PARTIAL"
log("RESULT = " + result)
(EVIDENCE / "RESULT.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
