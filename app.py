import streamlit as st
from converter_tool.converters import ojisan_converter

import streamlit as st
import base64

# 背景パターンを設定する関数
def set_bg_pattern(main_bg):
    # 画像ファイルを読み込んでWeb用データに変換
    with open(main_bg, "rb") as f:
        bin_str = base64.b64encode(f.read()).decode()
    
    # CSS（画面全体にパターンを敷き詰める設定）
    # !important をつけることで、Streamlitの元の背景設定を上書きするヨ！
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-repeat: repeat !important;
        background-size: 80px 80px !important; /* ここの数字を変えるとパターンの大きさが変わるヨ */
        background-attachment: fixed !important;
    }}
    
    /* サイドバーの背景は白っぽくして文字を読みやすくする設定（お好みで！） */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.8) !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# 実際に画像を読み込む（ファイル名は自分のものに合わせてね！）
try:
    set_bg_pattern("image/ojisanpatarn.png")
except Exception as e:
    # 画像が読み込めないときだけエラーを画面に出す（確認用）
    st.error(f"背景が出ない原因: {e}")
import streamlit as st
from converter_tool.converters import ojisan_converter
from PIL import Image # 画像を扱うための道具

# 1. サイドバーにおじさんの画像や説明を入れる
st.sidebar.title("おじさんの部屋 🧔")

# もし画像(ojisan.png)を準備できたら、下の2行のコメント(#)を外してね
image = Image.open('image/おじさん本体.png')
st.sidebar.image(image)

st.sidebar.write("""
### 作品解説
このアプリは、普通の文章を「おじさん構文」に変換するツールです。
一晩かけてエラーと戦いながら完成させました！✨
""")


st.set_page_config(
    page_title="🧔 おじさんコンバーター 💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🧔 おじさんコンバーター 💬")
st.markdown("普通の文章をキモいおじさん構文に変換！")

# 入力エリア
ojisan_text = st.text_area(
    "入力テキスト:",
    placeholder="変換したい文章を入力してください...\n\n例: 明日はデートですか？楽しみです。",
    height=200
)

# 変換ボタン
if st.button("変換する", use_container_width=True):
    if ojisan_text.strip():
        result = ojisan_converter(ojisan_text)
        st.markdown("### ✨ 変換結果:")
        st.info(result)
    else:
        st.warning("⚠️ テキストを入力してください")

# フッター
st.markdown("---")
st.markdown("<small style='text-align: center; color: #888;'>Powered by Streamlit</small>", unsafe_allow_html=True)
