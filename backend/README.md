# Bookmark

个人书签管理工具，基于 Django + Django REST Framework 构建，支持付费注册、多用户隔离、标签分类、关键词搜索和访问统计。

## 功能

- 付费注册（¥5.00 一次性，通过支付宝）
- 多用户数据隔离：每个账户独立管理自己的书签与标签
- 书签增删改查，支持收藏星标、可访问状态标记
- 标签管理（增删改查），支持自定义颜色
- 按标签筛选 / 关键词搜索（标题、描述、全文）
- 访问跳转并自动统计点击次数
- 响应式卡片布局，自动适配每行列数
- 深色 / 浅色模式切换（跟随系统 + 手动）

## 技术栈

- Python 3 / Django 6
- Django REST Framework
- MySQL
- python-alipay-sdk（支付宝 PC 网页支付）
- 纯原生 HTML + CSS + JS（无前端框架）

## 本地运行

**前置条件**：Python 3.10+、MySQL，并已创建数据库 `bookmark_v2`。

```bash
# 1. 克隆仓库
git clone https://github.com/J1npen/bookmark.git
cd bookmark

# 2. 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS / Linux

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 SECRET_KEY、数据库信息和支付宝配置

# 5. 初始化数据库（Django 内置表）
python manage.py migrate

# 6. 启动开发服务器
python manage.py runserver
```

访问 http://127.0.0.1:8000，使用 Django 管理员账户登录。

### 数据库表

所有业务表需手动在 MySQL 中创建（Django 不管理这些表的 schema）：

```sql
-- 书签
CREATE TABLE bookmarks ( ... );
-- 标签
CREATE TABLE tags ( ... );
-- 书签与标签关联
CREATE TABLE bookmark_tags (
    bookmark_id INT NOT NULL,
    tag_id      INT NOT NULL,
    PRIMARY KEY (bookmark_id, tag_id)
);
-- 用户与书签关联
CREATE TABLE user_bookmarks (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    bookmark_id INT NOT NULL,
    UNIQUE KEY unique_user_bookmark (user_id, bookmark_id),
    FOREIGN KEY (user_id)     REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE
);
-- 用户与标签关联
CREATE TABLE user_tags (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tag_id  INT NOT NULL,
    UNIQUE KEY unique_user_tag (user_id, tag_id),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)  REFERENCES tags(id) ON DELETE CASCADE
);
-- 支付订单
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

## 项目结构

```
bookmark/
├── api/          # DRF API（书签、标签 CRUD）及数据模型
├── bookmark/     # Django 项目配置
├── payment/      # 支付宝付费注册流程
├── webpage/      # 服务端渲染前端
├── .env.example  # 环境变量模板
└── requirements.txt
```

## API 端点

所有接口需登录后访问（Session 认证）。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/bookmarks/` | 书签列表（支持过滤参数） |
| POST | `/api/bookmarks/` | 新建书签（自动关联当前用户） |
| GET/PATCH/DELETE | `/api/bookmarks/{id}/` | 单条书签操作（DELETE 仅解除关联） |
| GET | `/api/tags/` | 标签列表 |
| POST | `/api/tags/` | 新建标签（自动关联当前用户） |
| GET/PATCH/DELETE | `/api/tags/{id}/` | 单条标签操作（DELETE 仅解除关联） |

书签列表支持的查询参数：`?keyword=`、`?search_in=title|description|all`、`?tag=<slug>`、`?favorite=1`、`?is_active=0|1`

## 注册流程

未登录用户访问登录页时，可点击「注册账号（¥5.00）」进入付费注册流程：

1. `/payment/register/` — 展示说明页，点击按钮发起支付
2. 跳转支付宝完成付款
3. `/payment/return/` — 支付宝同步回调，验签后展示注册表单
4. 提交用户名与密码完成注册，自动登录

支付宝异步通知由 `/payment/notify/` 接收（CSRF-exempt）。订单状态流转：`pending` → `paid` → `registered`。

## 多用户说明

- 每个用户只能看到与自己关联的书签和标签
- 超级管理员（`is_superuser`）可查看全部数据
- "删除"书签或标签仅解除与当前用户的关联，原始数据保留
- 用户与书签/标签的归属关系可在 Django Admin 中手动管理
