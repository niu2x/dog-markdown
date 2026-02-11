# AGENTS.md

本文档为在 dog-markdown 仓库中工作的智能编码工具提供开发指南。

AI的推理过程要使用中文。

## 0. 开发环境
Python 3.13
构建系统: uv_build
包管理器: uv

## 1. 构建/检查/测试命令

### 环境搭建
安装依赖并准备开发环境:
```bash
uv sync
```

### 构建项目
打包项目:
```bash
uv build
```

### 代码检查
使用 Ruff 进行静态代码分析:
```bash
ruff check .
```
自动修复可修复的代码问题:
```bash
ruff check . --fix
```

### 代码格式化
按照 PEP 8 标准格式化代码:
```bash
ruff format .
```
检查代码格式是否符合规范(不修改文件):
```bash
ruff format . --check
```

### 类型检查
使用 mypy 验证类型提示:
```bash
mypy src/
```

### 测试
运行所有测试:
```bash
uv run pytest
```
运行单个测试文件:
```bash
uv run pytest tests/test_markdown_generator.py
```
运行特定测试函数:
```bash
uv run pytest tests/test_markdown_generator.py::TestMarkdownGeneration::test_nested_blockquote_to_str
```
运行测试并查看覆盖率:
```bash
uv run pytest --cov=src/dog_markdown
```

## 2. 代码风格指南

### 导入规范
- 项目内所有模块使用绝对导入
- 导入按以下顺序分组:
  1. 标准库导入(按字母顺序排序)
  2. 第三方依赖导入(按字母顺序排序)
  3. 项目特定导入(按字母顺序排序)
- 每组之间用空行分隔
- 避免使用通配符导入(`from module import *`)
- 每组内的导入按字母顺序排序

### 代码格式化
- 遵循 PEP 8 规范:行宽最大88字符,使用4空格缩进(禁用制表符),合理使用空格
- 使用 Ruff 作为权威格式化工具
- 保持代码简洁:将长表达式拆分为多行以提高可读性
- 使用括号进行行延续,避免使用反斜杠
- 运算符前后和逗号后添加一个空格

### 类型提示
- 为所有函数参数、返回值和模块级变量添加类型提示
- 使用 `from typing import TYPE_CHECKING` 和 `if TYPE_CHECKING:` 块处理循环导入
- 使用 `from __future__ import annotations` 启用无需引号的前向引用
- 优先使用标准库类型(如 Python 3.9+ 中使用 `list[str]` 而非 `List[str]`)
- 使用联合类型语法 `A | B` 而非 `Union[A, B]`(Python 3.10+)
- 使用可选类型语法 `A | None` 而非 `Optional[A]`(Python 3.10+)
- 使用 `py.typed` 文件标记模块为已类型化(已存在于 `src/dog_markdown/`)
- 避免冗余的类型提示(如使用 `str | None` 而非 `Optional[str]`)

### 命名规范
- **变量/函数**: `snake_case`(全小写,下划线分隔)
- **类**: `PascalCase`(首字母大写,无下划线)
- **常量**: `UPPER_SNAKE_CASE`(全大写,下划线分隔)
- **模块**: 简短的小写名称(除非为了可读性否则避免使用下划线)
- **私有方法/变量**: 以单个下划线开头 `_private_method`
- **受保护方法/变量**: 以单个下划线开头 `_protected_method`
- **魔法方法**: 仅在 Python 特殊方法中使用双下划线 `__dunder_method`

### 错误处理
- 捕获特定异常,避免使用裸 `except:` 子句
- 抛出有意义的异常并提供描述性错误消息
- 使用上下文管理器(`with` 语句)进行资源处理
- 避免在没有明确理由的情况下抑制异常
- 谨慎使用 `try/except` 块;尽可能使用防御式编程

### 文档注释
- 为所有公共函数、类和模块编写文档字符串
- 使用 Google 风格的文档字符串保持一致性:
  ```python
  def parse_markdown(content: str) -> list[Node]:
      """将 Markdown 内容解析为抽象语法树。

      参数:
          content: 要解析的原始 Markdown 字符串。

      返回:
          表示已解析内容的 AST 节点列表。
  
      抛出:
          ParseError: 如果内容包含无效的 Markdown 语法。
      """
  ```
- 保持文档字符串简洁但信息丰富
- 记录所有公共 API 的参数、返回值和异常

### 额外最佳实践
- 生产代码中避免使用 print 语句;使用 `logging` 模块替代
- 保持函数小巧,专注于单一职责
- 为所有公共 API 函数编写单元测试
- 使用 `__future__` 导入以实现向前兼容性(如果需要)
- 避免使用全局变量;在适当的地方使用依赖注入
- 优先使用组合而非继承
- 使用上下文管理器进行资源管理
- 编写自文档化代码,使用有意义的变量和函数名称
- 避免使用魔法数字;使用命名常量替代
- 通过提取可重用函数保持代码 DRY(Don't Repeat Yourself)
- 尽可能使用不可变数据;对固定数据使用 `frozenset` 和 `tuple` 而非 `set` 和 `list`