# Bookmark

个人书签管理工具，支持付费注册、多用户隔离、标签分类、关键词搜索、AI 自动描述和访问统计。

**技术栈：** Django REST Framework 后端 + Vue 3 SPA 前端（Monorepo）

## 功能

- 付费注册（¥5.00 一次性，通过支付宝）
- 多用户数据隔离：每个账户独立管理书签与标签
- 书签增删改查，支持收藏星标、可访问状态标记
- 标签管理，支持自定义颜色
- 按标签筛选 / 关键词搜索（标题、描述、全文）
- AI 一键生成书签描述（GPT-4o-mini）
- 访问跳转并自动统计点击次数
- 深色 / 浅色模式切换

## 项目结构

```
bookmark/
├── backend/
│   ├── api/          # DRF API（书签、标签 CRUD）及数据模型
│   ├── bookmark/     # Django 项目配置
│   ├── payment/      # 支付宝付费注册流程
│   ├── webpage/      # 服务端渲染前端（遗留，仍在用）
│   └── requirements.txt
├── frontend/         # Vue 3 SPA（Vite + Pinia + Vue Router + Axios）
│   └── src/
│       ├── api/      # Axios 封装与接口调用
│       ├── stores/   # Pinia 状态（auth、bookmarks、tags）
│       └── views/    # 页面组件
└── .env              # 环境变量（前后端共用）
```

## 本地运行

**前置条件：** Python 3.10+、Node.js 18+、MySQL，已创建数据库 `bookmark_v2`。

### 1. 克隆仓库

```bash
git clone https://github.com/J1npen/bookmark.git
cd bookmark
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入以下配置
```

| 变量 | 说明 |
|------|------|
| `SECRET_KEY` | Django Secret Key |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` | MySQL 连接信息 |
| `OPENAI_API_KEY` | AI 生成描述（可选） |
| `ALIPAY_APP_ID` / `ALIPAY_PRIVATE_KEY` / `ALIPAY_PUBLIC_KEY` | 支付宝配置 |
| `ALIPAY_SANDBOX` | `True` 使用沙盒，`False` 正式环境 |

### 3. 启动后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS / Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # http://127.0.0.1:8000
```

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173，自动代理 /api 和 /accounts 到 :8000
```

### 5. 初始化数据库表

所有业务表需手动在 MySQL 中创建（Django 不管理这些表的 schema）：

```sql
CREATE TABLE bookmarks (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    url         VARCHAR(2048) NOT NULL,
    title       VARCHAR(512)  NOT NULL DEFAULT '',
    description TEXT,
    favicon     VARCHAR(512)  DEFAULT NULL,
    is_active   TINYINT(1)    NOT NULL DEFAULT 1,
    favorite    TINYINT(1)    NOT NULL DEFAULT 0,
    visit_count INT           NOT NULL DEFAULT 0,
    created_at  DATETIME(6)   NOT NULL
);

CREATE TABLE tags (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    slug  VARCHAR(100) NOT NULL UNIQUE,
    color VARCHAR(20)  NOT NULL DEFAULT '#6c757d'
);

CREATE TABLE bookmark_tags (
    bookmark_id INT NOT NULL,
    tag_id      INT NOT NULL,
    PRIMARY KEY (bookmark_id, tag_id),
    FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)      REFERENCES tags(id)      ON DELETE CASCADE
);

CREATE TABLE user_bookmarks (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    bookmark_id INT NOT NULL,
    UNIQUE KEY unique_user_bookmark (user_id, bookmark_id),
    FOREIGN KEY (user_id)     REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE
);

CREATE TABLE user_tags (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tag_id  INT NOT NULL,
    UNIQUE KEY unique_user_tag (user_id, tag_id),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)  REFERENCES tags(id)      ON DELETE CASCADE
);

CREATE TABLE payment_orders (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    out_trade_no VARCHAR(64)   NOT NULL UNIQUE,
    trade_no     VARCHAR(64)   NULL DEFAULT NULL,
    amount       DECIMAL(10,2) NOT NULL DEFAULT 5.00,
    status       VARCHAR(20)   NOT NULL DEFAULT 'pending',
    created_at   DATETIME(6)   NOT NULL,
    paid_at      DATETIME(6)   NULL DEFAULT NULL
);
```

## API 端点

所有接口需登录后访问（Session 认证）。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/bookmarks/` | 书签列表（支持过滤参数） |
| POST | `/api/bookmarks/` | 新建书签 |
| GET/PATCH/DELETE | `/api/bookmarks/{id}/` | 单条书签操作 |
| POST | `/api/bookmarks/{id}/visit/` | 记录访问并增加计数 |
| GET | `/api/tags/` | 标签列表 |
| POST | `/api/tags/` | 新建标签 |
| GET/PATCH/DELETE | `/api/tags/{id}/` | 单条标签操作 |
| GET | `/api/fetch-url-meta/` | 抓取页面标题与 favicon |
| GET | `/api/describe/` | AI 生成书签一句话描述 |

书签列表支持的查询参数：`?keyword=`、`?search_in=title\|description\|all`、`?tag=<slug>`、`?favorite=1`、`?is_active=0\|1`、`?page=`、`?page_size=`

## 注册流程

未登录用户可通过付费注册获得账号（¥5.00 一次性）：

1. `/payment/register/` — 展示说明页，点击按钮发起支付
2. 跳转支付宝完成付款
3. `/payment/return/` — 同步回调，验签后展示注册表单
4. 填写用户名和密码，提交后自动登录

订单状态流转：`pending` → `paid` → `registered`

## 多用户说明

- 每个用户只能看到与自己关联的书签和标签
- 超级管理员（`is_superuser`）可查看全部数据
- "删除"书签或标签仅解除关联，原始数据保留
- 归属关系可在 Django Admin 中手动管理
