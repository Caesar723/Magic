#!/usr/bin/env bash

# 启动 MySQL 服务
echo "启动 MySQL 服务..."
service mysql start

# 等待 MySQL 服务启动完成
until mysqladmin ping &>/dev/null; do
    echo -n "."; sleep 1
done

echo "MySQL 服务已启动"
python3 src/database.py --reset-all-card --reset-packs --reset-table
# 执行原始的 Kasm 启动脚本
