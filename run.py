#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
おじさんコンバーター - セットアップ・実行スクリプト

このスクリプトは以下を自動で行います:
1. Pythonバージョンの確認
2. 依存パッケージのインストール
3. アプリケーションの起動
"""

import os
import sys
import subprocess

def check_python_version():
    """Pythonバージョンの確認"""
    print("📌 Pythonバージョンを確認中...")
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print(f"❌ Python 3.7以上が必要です（現在: {python_version.major}.{python_version.minor}）")
        return False
    print(f"✓ Python {python_version.major}.{python_version.minor} を確認しました")
    return True

def install_requirements():
    """依存パッケージのインストール"""
    print("\n📦 依存パッケージをインストール中...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-q'])
        print("✓ パッケージのインストールが完了しました")
        return True
    except subprocess.CalledProcessError:
        print("❌ パッケージのインストールに失敗しました")
        return False

def start_app():
    """アプリケーションの起動"""
    print("\n" + "=" * 60)
    print("🧔💕 おじさんと女の子のコンバーター 💕🧔")
    print("=" * 60)
    print("\n🚀 アプリケーションを起動中...\n")
    
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    
    from app import app
    
    print("✓ サーバーが起動しました")
    print("\n📱 ブラウザで http://localhost:5000 にアクセスしてください")
    print("\n⌛ 終了するには Ctrl+C を押してください\n")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

def main():
    """メイン処理"""
    # Pythonバージョン確認
    if not check_python_version():
        sys.exit(1)
    
    # 依存パッケージをインストール
    if not install_requirements():
        sys.exit(1)
    
    # アプリケーション起動
    try:
        start_app()
    except KeyboardInterrupt:
        print("\n\n👋 アプリケーションを終了します")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
