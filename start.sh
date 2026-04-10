#!/bin/bash

echo "=================================================="
echo "🧔💕 おじさんと女の子のコンバーター 💕🧔"
echo "=================================================="
echo ""

# Pythonのバージョン確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3がインストールされていません"
    exit 1
fi

echo "✓ Python3を確認しました: $(python3 --version)"
echo ""

# 依存パッケージをインストール
echo "📦 依存パッケージをインストール中..."
python3 -m pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "❌ パッケージのインストールに失敗しました"
    exit 1
fi

echo "✓ パッケージのインストールが完了しました"
echo ""

# アプリケーションを実行
echo "🚀 アプリケーションを起動中..."
echo ""
python3 run.py
