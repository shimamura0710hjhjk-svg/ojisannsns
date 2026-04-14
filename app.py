import streamlit as st
from converter_tool.converters import ojisan_converter

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
