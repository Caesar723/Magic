#!/bin/sh

# 标志文件路径
INIT_FLAG="/app/db_initialized"

# 检查标志文件是否存在
if [ ! -f "$INIT_FLAG" ]; then
    echo "Initializing database..."
    python src/database.py --reset-table --reset-all-card --reset-packs
    # 创建标志文件
    touch "$INIT_FLAG"
else
    echo "Database already initialized."
fi

# 启动应用
python src/server_start.py
