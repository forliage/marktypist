# Marktypist

<!-- 未来在这里放上 PyPI, Build Status 等徽章 -->
<!-- [![PyPI version](https://badge.fury.io/py/marktypist.svg)](https://badge.fury.io/py/marktypist) -->

**一个功能强大的 Markdown 与 Typst 双向转换器，旨在实现高保真度的文档格式迁移。**

---

### 简介

`Marktypist` 是一个使用 Python 开发的命令行工具，致力于解决 [Markdown](https://www.markdownguide.org/) 和 [Typst](https://typst.app/) 这两种标记语言之间的生态鸿沟。本项目不仅仅是简单的文本替换，而是通过构建一个**通用文档模型 (Universal Document Model, UDM)** 作为中间表示，来精确地解析源文档的逻辑结构，并将其重新渲染为目标格式。

这种基于抽象语法树 (AST) 的方法使得 `Marktypist` 能够处理复杂的文档结构，实现真正意义上的“逻辑转换”。

### 核心特性

*   **双向转换:** 支持 Markdown -> Typst 和 Typst -> Markdown。
*   **高保真度:** 尽最大努力保留文档的结构和语义，包括标题、列表、代码块、引用、表格、图片等。
*   **强大的架构:** 基于“解析器 -> 中间表示 -> 渲染器”的设计，易于维护和扩展。
*   **可扩展性:** 核心架构允许未来轻松添加对其他格式（如 HTML, LaTeX）的支持。
*   **纯 Python 实现:** 依赖于 `markdown-it-py` 和 `lark` 等优秀的库。
*   **友好的命令行:** 提供简单易用的命令行接口，方便集成到自动化工作流中。

### 安装

> **注意:** 本项目仍在早期开发阶段，尚未发布到 PyPI。

当项目成熟后，你将可以通过以下命令进行安装：
```bash
pip install marktypist
```

### 快速开始

```bash
# 将 Markdown 文件转换为 Typst
marktypist convert my_article.md -o my_article.typ

# 将 Typst 文件转换为 Markdown
marktypist convert my_paper.typ -o my_paper.md

# 查看帮助信息
marktypist --help
marktypist convert --help
```

### 项目状态 (开发路线图)

-   [ ] **阶段一：基础架构与 MVP**
    -   [x] 搭建项目结构与虚拟环境。
    -   [ ] 定义核心通用文档模型 (UDM)。
    -   [ ] 实现 `Markdown -> Typst` 的基本转换（标题、段落、粗体/斜体）。
-   [ ] **阶段二：核心功能完善**
    -   [ ] 支持列表、代码块、链接和引用。
    -   [ ] 启动 `Typst -> Markdown` 的转换工作。
-   [ ] **阶段三：高级功能支持**
    -   [ ] 实现对**表格**和**图片**的双向转换。
-   [ ] **阶段四：健壮性与发布**
    -   [ ] 处理 Typst 特有语法（如脚本、变量）。
    -   [ ] 完善测试用例。
    -   [ ] 打包并发布到 PyPI。

### 贡献

欢迎任何形式的贡献！如果你对本项目感兴趣，可以从提交 Issue、修复 Bug 或实现新功能开始。

### 许可证

本项目采用 [MIT](LICENSE) 许可证。