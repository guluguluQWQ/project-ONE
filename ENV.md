# 环境说明（env-check 练习夹）

用途：验证「当前环境能否支撑项目」的最小探针，不含任何业务逻辑。

- Python：3.14.2，用 `py -3.14` 显式指定；系统默认不动、不降级、不卸载。
- 建环境：`py -3.14 -m venv .venv`
- 激活（PowerShell）：`.\.venv\Scripts\Activate.ps1`
- 装依赖：`python -m pip install -r requirements.txt`
- 跑验收：`python probe.py`，结果写进 `evidence/RESULT.txt`
- 启动方式：一律 `python -m pip`，不用裸 `pip`（多版本并存时后者可能指向别的解释器）

调用清单（管什么 / 不管什么）：

| 库 | 管什么 | 不管什么 |
|---|---|---|
| Pillow | 图片的读写与校验 | 不认字 |
| mss | 取一帧屏幕画面 | 不保证全屏独占时拿得到 |
| PySide6-Essentials | 创建浮窗对象 | 不管内容对不对 |

- OCR：实现**可替换**；本环境未安装、未选定任何 OCR 库。需要时换实现，或另开一个 3.12 独立环境，系统 3.14 保持不动。
- `.gitignore` 排除 `.venv/`、`evidence/*.png`、`__pycache__/`；文本证据 `RESULT.txt` 进仓库。
- 工作区路径是指向 `E:\WorkBuddy Data\Projects\...` 的目录联接（junction），git 显示 E 盘路径属正常。
