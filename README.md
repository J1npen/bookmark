# Bookmark

个人书签管理工具，基于 Django + Django REST Framework 构建，支持标签分类、关键词搜索和访问统计。

## 功能

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
# 编辑 .env，填入 SECRET_KEY 和数据库信息

# 5. 启动开发服务器
python manage.py runserver
```

访问 http://127.0.0.1:8000

## 项目结构

```
bookmark/
├── api/          # DRF API（书签、标签 CRUD）
├── bookmark/     # Django 项目配置
├── webpage/      # 服务端渲染前端
├── .env.example  # 环境变量模板
└── requirements.txt
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/bookmarks/` | 书签列表（支持过滤参数） |
| POST | `/api/bookmarks/` | 新建书签 |
| GET/PATCH/DELETE | `/api/bookmarks/{id}/` | 单条书签操作 |
| GET | `/api/tags/` | 标签列表 |
| POST | `/api/tags/` | 新建标签 |
| GET/PATCH/DELETE | `/api/tags/{id}/` | 单条标签操作 |

书签列表支持的查询参数：`?keyword=`、`?search_in=title\|description\|all`、`?tag=<slug>`、`?favorite=1`、`?is_active=0\|1`
