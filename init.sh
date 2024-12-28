#!/bin/sh

# 标志文件路径

# 检查 MySQL 服务是否正在运行
if pgrep mysqld >/dev/null 2>&1; then
    echo "MySQL 服务已在运行。"
else
    echo "MySQL 服务未运行，正在启动..."
    service mysql start

    # 等待 MySQL 服务启动完成
    until mysqladmin ping >/dev/null 2>&1; do
        echo -n "."; sleep 1
    done

    echo "MySQL 服务已启动。"
fi

INIT_FLAG="/app/db_initialized"

# 检查标志文件是否存在
if [ ! -f "$INIT_FLAG" ]; then
    echo "Initializing database..."
    python src/database.py --reset-table --reset-all-card --reset-packs --reset-tasks
    # 创建标志文件
    touch "$INIT_FLAG"
else
    echo "Database already initialized."
fi

# 启动应用
python src/server_start.py
