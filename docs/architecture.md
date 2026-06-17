# Todo UI Probe 当前架构

## 系统目标与边界

**目标**：提供一个纯前端待办清单（Todo List）网页，用户可在浏览器中管理任务列表。

**范围内**：
- 添加任务（输入任务名称 → 添加到列表）
- 勾选完成任务（显示删除线 + 变灰）
- 删除任务（从列表移除）
- 空列表引导提示
- 纯 UI 交互，无后端存储

**范围外**：
- 后端存储与数据库
- 用户认证与多设备同步
- 数据持久化（刷新后数据丢失）
- 任务编辑、排序、分类、过滤等高级功能

## 技术栈与选择理由

| 层级 | 技术 | 理由 |
|------|------|------|
| 结构 | HTML5 | 单页应用，无需框架 |
| 样式 | CSS3（内联） | 零外部依赖，简单视觉需求 |
| 逻辑 | Vanilla JS (ES5) | 兼容性好，无构建工具需求 |
| 开发服务器 | Python 3 http.server | 标准库，无需额外安装，满足静态文件服务需求 |
| 部署 | Nginx 静态文件 | 行业标准，sub-path `/projects/todo-ui-probe/` 部署 |

**为何无框架无构建工具**：项目需求为单一页面 + 简单交互，引入框架 (React/Vue) 和构建工具 (webpack/vite) 会带来不必要的复杂度。Vanilla HTML/CSS/JS 实时可用，零编译开销。

## 模块职责与依赖

### 文件结构

```
src/
├── index.html    # 单页 HTML：结构 + 样式 + 逻辑
└── server.py     # 开发用静态文件服务器
```

### 模块职责

**index.html** — 唯一的前端模块，包含三部分：
- **HTML 结构**：表单输入区（input + button）、任务列表容器（ul）、空状态提示区
- **CSS 样式**：组件样式、完成态样式（删除线 + 变灰）、响应式布局
- **JS 逻辑**（IIFE 封装）：
  - `tasks[]` — 内存中的任务数组，每个任务 `{ text: string, completed: boolean }`
  - `render()` — 基于 `tasks[]` 全量重绘 DOM
  - 事件绑定：表单提交（添加）、复选框变更（完成切换）、删除按钮点击（移除）

**server.py** — 开发服务器：
- 继承 `SimpleHTTPRequestHandler`，根目录设为 `src/`
- `GET /` → 返回 `index.html`（带 `Cache-Control: no-cache`）
- `GET /healthz` → 返回 `{"ok": true}`（JSON）
- 所有 HTML 响应自动附加 `Cache-Control: no-cache` 头
- 绑定 `127.0.0.1:19003`

## 数据流、状态流与外部接口

### 状态流（同一页面生命周期内）

```
用户输入 → [提交] → tasks.push({text, completed:false}) → render()
用户勾选 → [checkbox change] → tasks[i].completed = true → render()
用户删除 → [click delete] → tasks.splice(i, 1) → render()
```

### 数据存储

- 状态仅存在于 JavaScript 闭包中的 `tasks[]` 数组
- 页面刷新 → 状态重置为空
- 无 localStorage、无 IndexedDB、无 Cookie

### 外部接口

| 端点 | 方法 | 响应 | 用途 |
|------|------|------|------|
| `/healthz` | GET | `{"ok": true}` | 健康检查 |

无其他 API 端点。系统为纯前端，无后端数据接口。

## 测试策略

- **自测范围**：手动验证核心功能（添加、完成、删除、空状态）、Python 服务器健康检查
- **验收标准**（Hermes 定义）：
  - 浏览器：加载无控制台错误、CSS/JS 无 404
  - 功能：添加出现、勾选划线变灰、删除移除、空态引导
  - 技术：单页无外部依赖、数据不持久化
- **不要求**：单元测试框架、E2E 测试、CI/CD 自动化测试

## 部署拓扑

```
用户浏览器
    │
    ▼
Nginx (HTTPS, port 443)
    │  sub-path: /projects/todo-ui-probe/
    │  root: /usr/share/nginx/html/todo-ui-probe/
    │  Cache-Control: no-cache on HTML responses
    ▼
静态文件: src/index.html (versioned query ?v=0.0.1)
```

## 安全边界

- **网络隔离**：开发服务器绑定 `127.0.0.1`，仅本地访问
- **输入约束**：任务文本 `maxlength="200"`，前端 trim 处理
- **无敏感数据**：所有数据仅存在于浏览器内存中
- **无认证**：纯演示用途，无用户系统
- **CSP/HTTPS**：由 Nginx 层统一配置，应用层不单独处理

## 已知技术债

- 无。项目处于初始迭代 (0.0.1)，尚未累积技术债。

## 关联 ADR 与最近变更

- 迭代 0.0.1：初始 Todo UI 实现（2026-06-17）
- 暂无 ADR 记录
