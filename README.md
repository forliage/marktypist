# Marktypist

<!-- 未来在这里放上 PyPI, Build Status 等徽章 -->
<!-- [![PyPI version](https://badge.fury.io/py/marktypist.svg)](https://badge.fury.io/py/marktypist) -->

**一个功能强大的 Markdown 与 Typst 双向转换器，旨在实现高保真度的文档格式迁移。**

---

### 简介

`Marktypist` 是一个使用 Python 开发的命令行工具，致力于解决 [Markdown](https://www.markdownguide.org/) 和 [Typst](https://typst.app/) 这两种标记语言之间的生态鸿沟。本项目通过构建一个**通用文档模型 (Universal Document Model, UDM)** 作为中间表示，来精确地解析源文档的逻辑结构，并将其重新渲染为目标格式。

这种基于抽象语法树 (AST) 的方法（在 Markdown -> Typst 方向）或简化的正则匹配（在 Typst -> Markdown 方向）使得 `Marktypist` 能够处理常见的文档结构，实现有损但实用的“逻辑转换”。

### 核心特性

*   **双向转换 (基础支持):**
    *   **Markdown -> Typst:**
        *   标题 (H1-H6)
        *   段落
        *   粗体、斜体
        *   行内代码与代码块 (带语言高亮)
        *   无序列表、有序列表
        *   链接、图片
        *   块引用 (包括嵌套)
        *   **表格 (GFM 语法支持)**
    *   **Typst -> Markdown (当前为基础正则解析实现):**
        *   标题 (`=` `==`)
        *   段落
        *   粗体 (`*...*`)、斜体 (`_..._`)、粗斜体 (`*_..._*`)
        *   无序列表 (`- ...`)

*   **强大的架构:** 基于“解析器 -> 中间表示 -> 渲染器”的设计，易于维护和扩展。
*   **纯 Python 实现:** 依赖于 `markdown-it-py` (Markdown 解析)、`linkify-it-py` (Markdown 链接处理) 等库。
*   **友好的命令行:** 提供简单易用的命令行接口，方便集成到自动化工作流中。

### 安装

> **注意:** 本项目仍在早期开发阶段，尚未发布到 PyPI。

当项目成熟后，你将可以通过以下命令进行安装：
```bash
pip install marktypist
```

### 快速开始

首先，请确保你已在项目的根目录创建并激活了虚拟环境，并安装了所有依赖：
```bash
# 在项目根目录 marktypist-project/
python -m venv venv
.\venv\Scripts\activate  # Windows PowerShell
# source venv/bin/activate  # Linux/macOS Bash
pip install -e .[dev]
```

现在，你可以在终端直接使用 `marktypist` 命令了：

#### Markdown 到 Typst 转换

```bash
# 示例：创建一个 Markdown 文件
echo "# My Document\n\nThis is **bold** and *italic* text." > my_doc.md

# 将 Markdown 文件转换为 Typst 文件
marktypist convert my_doc.md -o my_doc.typ

# 查看转换后的 Typst 内容
type my_doc.typ  # Windows cmd/PowerShell
# 或 cat my_doc.typ # Linux/macOS
```
**预期输出 (my_doc.typ):**
```typst
= My Document

This is *bold* and _italic_ text.
```

#### Typst 到 Markdown 转换

```bash
# 示例：创建一个 Typst 文件
Set-Content -Path my_typ_doc.typ -Value "= My Typst Title\n\n这是一个段落。\n\n*粗体*与_斜体_。" # PowerShell
# 或手动创建并编辑 my_typ_doc.typ 文件

# 将 Typst 文件转换为 Markdown 文件
marktypist convert my_typ_doc.typ -o my_typ_doc.md

# 查看转换后的 Markdown 内容
type my_typ_doc.md # Windows cmd/PowerShell
# 或 cat my_typ_doc.md # Linux/macOS
```
**预期输出 (my_typ_doc.md):**
```markdown
# My Typst Title

这是一个段落。

**粗体**与*斜体*。
```

#### 其他用法

*   **输出到标准输出 (不指定 `-o`):**
    ```bash
    marktypist convert my_doc.md
    ```
*   **获取帮助信息:**
    ```bash
    marktypist --help
    marktypist convert --help
    ```

### 项目状态 (开发路线图)

目前，核心的 Markdown 到 Typst 转换功能已相对完善，Typst 到 Markdown 的基础功能也已实现。

-   [x] **阶段一：基础架构与 MVP**
    -   [x] 搭建项目结构与虚拟环境。
    -   [x] 定义核心通用文档模型 (UDM)。
    -   [x] 实现 `Markdown -> Typst` 的基本转换（标题、段落、粗体/斜体）。
-   [x] **阶段二：MD -> Typst 核心功能完善**
    -   [x] 支持列表、行内代码、代码块和引用。
    -   [x] 支持链接和图片。
    -   [x] **支持表格 (GFM)**。
-   [x] **阶段三：构建命令行接口 (CLI)**
    -   [x] 实现 `marktypist convert` 命令。
    -   [x] 支持文件输入/输出和标准输出。
-   [x] **阶段四：Typst -> Markdown 基础转换**
    -   [x] 实现基础的 Typst 解析器 (使用正则表达式)。
    -   [x] 实现基础的 Markdown 渲染器。
    -   [x] 支持标题、段落、粗体、斜体、粗斜体、无序列表。

#### 待办事项 / 未来规划

-   **Typst -> Markdown 功能增强:**
    -   [ ] **表格转换:** 这是 Typst -> MD 最具挑战性的部分之一，Typst 的表格功能更强大。
    -   [ ] **有序列表、代码块、引用、链接、图片转换。**
    -   [ ] **复杂嵌套样式**的处理 (例如 `_这是*粗体*斜体_`)。
    -   [ ] **Lark 解析器的重新审视:** 考虑是否需要重新引入并完善 Lark 解析器来处理 Typst 更复杂的语法和更精确的结构解析，以提升转换质量和鲁棒性。
-   **高级功能:**
    -   [ ] **模板化输出:** 支持用户自定义 Typst 模板或 Markdown 风格。
    -   [ ] **元数据处理:** 转换文档的 YAML frontmatter 或 Typst 的 `#let` 变量。
    -   [ ] **错误报告与警告:** 针对无法高保真转换的 Typst 特性提供警告。
-   **性能优化与测试覆盖:**
    -   [ ] 增加更全面的端到端测试。
    -   [ ] 性能优化，特别是对大文件的处理。
-   **发布到 PyPI:**
    -   [ ] 完成所有核心功能后，将项目打包发布，方便用户安装。

### 贡献

欢迎任何形式的贡献！如果你对本项目感兴趣，可以从提交 Issue、修复 Bug 或实现新功能开始。

### 许可证

本项目采用 [MIT](LICENSE) 许可证。