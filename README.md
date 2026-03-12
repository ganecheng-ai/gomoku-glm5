# 五子棋 (Gomoku Game)

一个精美的五子棋游戏，使用 Python 和 Pygame 开发，支持简体中文界面。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 游戏截图

游戏界面精美，操作简单，与经典五子棋游戏一致。

## 功能特性

- 精美的图形界面
- 简体中文支持
- **双人对战模式**
- **人机对战模式 (AI)**
- 黑白棋子交替下棋
- 五子连珠判定
- 悔棋功能
- 重新开始
- 步数统计
- 最后一步标记
- 计时器功能
- 游戏记录保存
- 音效支持
- 完整的日志系统

## 系统要求

- Python 3.8 或更高版本
- Pygame 2.5.0 或更高版本

## 安装方法

### 从源码运行

1. 克隆仓库
```bash
git clone https://github.com/ganecheng-ai/gomoku-glm5.git
cd gomoku-glm5
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行游戏
```bash
python main.py
```

### 从发布版本运行

从 [Releases](https://github.com/ganecheng-ai/gomoku-glm5/releases) 页面下载对应平台的可执行文件：

#### Windows
- 下载 `gomoku-glm5-windows-x64.zip`
- 解压后运行 `gomoku-glm5.exe`

#### Linux
有三种安装方式可选：

1. **通用二进制** (推荐)
   - 下载 `gomoku-glm5-linux-x64.tar.gz`
   - 解压后运行 `gomoku-glm5`

2. **Debian/Ubuntu (.deb)**
   - 下载 `gomoku-glm5-linux-x64.deb`
   - 安装: `sudo dpkg -i gomoku-glm5-linux-x64.deb`
   - 运行: `gomoku-glm5`

3. **AppImage** (无需安装)
   - 下载 `gomoku-glm5-linux-x64.AppImage`
   - 添加执行权限: `chmod +x gomoku-glm5-linux-x64.AppImage`
   - 运行: `./gomoku-glm5-linux-x64.AppImage`

#### macOS
- 下载 `gomoku-glm5-macos-x64.tar.gz`
- 解压后运行 `gomoku-glm5`

## 游戏规则

1. 黑棋先行
2. 双方轮流在棋盘上放置棋子
3. 先将五个棋子连成一线（横、竖、斜均可）的一方获胜
4. 棋盘下满则为平局

## 操作说明

- **鼠标左键**: 在棋盘上落子
- **重新开始**: 点击"重新开始"按钮
- **悔棋**: 点击"悔棋"按钮撤销上一步
- **退出**: 点击"退出"按钮关闭游戏

## 项目结构

```
gomoku-glm5/
├── gomoku/
│   ├── __init__.py      # 包初始化
│   ├── game.py          # 游戏主逻辑
│   ├── board.py         # 棋盘类
│   ├── player.py        # 玩家类
│   ├── ui.py            # 界面渲染
│   ├── constants.py     # 常量定义
│   ├── timer.py         # 计时器模块
│   ├── sound.py         # 音效模块
│   ├── record.py        # 游戏记录模块
│   ├── logger.py        # 日志系统模块
│   └── ai.py            # AI玩家模块
├── assets/
│   ├── fonts/           # 字体文件
│   ├── images/          # 图片资源
│   └── sounds/          # 音效文件
├── tests/
│   └── test_game.py     # 单元测试
├── main.py              # 程序入口
├── requirements.txt     # 依赖文件
├── pyproject.toml       # 项目配置
├── plan.md              # 开发计划
├── prompt.md            # 开发指令
└── README.md            # 项目说明
```

## 开发

### 运行测试

```bash
pip install pytest
pytest tests/ -v
```

### 构建可执行文件

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name gomoku-glm5 main.py
```

## 版本历史

- **v1.2.0** - 增强 Linux 发布格式 (.deb, .AppImage)
- **v1.1.0** - 新增AI对战功能，游戏模式选择
- **v1.0.0** - 正式发布版本，日志系统
- **v0.4.0** - 高级功能（游戏记录、计时器、音效）
- **v0.3.0** - 精美界面，中文支持
- **v0.2.0** - 完整游戏逻辑
- **v0.1.0** - 基础游戏框架

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

ganecheng-ai