#!/bin/bash

# 基本设置
FLATNOTES_BASE_DIR="$(pwd)"
DATA_DIR="${FLATNOTES_BASE_DIR}/data"

# 创建必要的目录
mkdir -p "${DATA_DIR}"
mkdir -p "${DATA_DIR}/notes"
mkdir -p "${DATA_DIR}/attachments"

# 设置所有必要的环境变量
export FLATNOTES_AUTH_TYPE=password
export FLATNOTES_USERNAME=user
export FLATNOTES_PASSWORD='changeMe!'
export FLATNOTES_SECRET_KEY=aLongRandomSeriesOfCharacters
export FLATNOTES_HOST=0.0.0.0
export FLATNOTES_PORT=8081
export FLATNOTES_PATH="${DATA_DIR}"
export FLATNOTES_HIDE_RECENTLY_MODIFIED = true

# 确保client/dist复制到server目录下
if [ -d "${FLATNOTES_BASE_DIR}/client/dist" ] && [ ! -d "${FLATNOTES_BASE_DIR}/server/client/dist" ]; then
    echo "正在将client/dist复制到server/client/dist..."
    mkdir -p "${FLATNOTES_BASE_DIR}/server/client"
    cp -r "${FLATNOTES_BASE_DIR}/client/dist" "${FLATNOTES_BASE_DIR}/server/client/"
fi

# 检查Pipfile
if [ -f "Pipfile" ]; then
    echo "检测到Pipfile, 使用pipenv环境..."
    pip install pipenv
    pipenv install
    
    echo "正在启动Flatnotes应用..."
    # 在server目录中运行，设置PYTHONPATH
    cd server
    PYTHONPATH=.. pipenv run uvicorn main:app --host ${FLATNOTES_HOST} --port ${FLATNOTES_PORT} --reload
else
    echo "使用virtualenv环境..."
    if [ ! -d "venv" ]; then
        echo "创建虚拟环境..."
        python -m venv venv
    fi
    
    source venv/bin/activate
    pip install fastapi uvicorn python-multipart python-jose pyotp passlib[bcrypt] pyjwt cryptography
    
    echo "正在启动Flatnotes应用..."
    # 在server目录中运行，设置PYTHONPATH
    cd server
    PYTHONPATH=.. uvicorn main:app --host ${FLATNOTES_HOST} --port ${FLATNOTES_PORT} --reload
fi