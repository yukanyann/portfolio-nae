import os

import streamlit as st
from gtts import gTTS
from PIL import Image

from utils import load_yaml

nae_types = [
    "いんげん",
    "オクラ",
    "ゴーヤ",
    "ししとう",
    "すいか",
    "トウガラシ",
    "なす",
    "ピーマン",
    "ブロッコリー",
    "ミニトマト",
    "メロン",
    "モロヘイヤ",
    "リーフレタス",
    "レタス",
]


nae_types = [
    "いんげん",
    "オクラ",
    "ゴーヤ",
    "ししとう",
    "すいか",
    "トウガラシ",
    "なす",
    "ピーマン",
    "ブロッコリー",
    "ミニトマト",
    "メロン",
    "モロヘイヤ",
    "リーフレタス",
    "レタス",
]
image_paths = {
    "いんげん": r"./image/いんげん.jpg",
    "オクラ": r"./image/オクラ.jpg",
    "ゴーヤ": r"./image/ゴーヤ.jpg",
    "ししとう": r"./image/ししとう.jpg",
    "すいか": r"./image/すいか.jpg",
    "トウガラシ": r"./image/トウガラシ.jpg",
    "なす": r"./image/なす.jpg",
    "ピーマン": r"./image/ピーマン.jpg",
    "ブロッコリー": r"./image/ブロッコリー.jpg",
    "ミニトマト": r"./image/ミニトマト.jpg",
    "メロン": r"./image/メロン.jpg",
    "モロヘイヤ": r"./image/モロヘイヤ.jpg",
    "リーフレタス": r"./image/リーフレタス.jpg",
    "レタス": r"./image/レタス.jpg",
}



def display():

    st.markdown("""
        <style>
        /* ボタンに適用されるスタイル */
        .stButton>button {
            background-color: #FFFFFF; /* 白色の背景 */
            color: #2E8B57; /* セージグリーンのテキスト */
            border: 2px solid #698B69; /* くすんだ緑色の境界線 */
            padding: 10px 10px; /* パディングを適切に設定 */
            border-radius: 10px; /* 角を丸くする */
            font-weight: bold; /* フォントを太字に */
            font-size: 16px; /* フォントサイズを調整 */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* シャドウを追加 */
            transition: background-color 0.2s, box-shadow 0.2s, transform 0.2s; /* トランジションを設定 */
        }
        </style>

    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("★苗の種類から選ぶ⇩")

    page_state = st.session_state.get("page_state", "home")


# colsの初期化をpage_stateの条件外に移動
    cols = st.sidebar.columns(3)


    if page_state == "home":
        for i, nae_type in enumerate(nae_types):
            if cols[i % 3].button(nae_type):
                st.session_state.page_state = "selected_nae" #ページ状態を更新
                st.session_state.selected_nae_type = nae_type
                st.session_state["has_interacted"]=True # ユーザーの操作を記録
                break

    # ホームに戻るボタン（ユーザーが操作したら表示し、ボタンをクリックしたら非表示に）  
    if st.session_state.get("has_interacted",False):
        if st.button("メニューに戻る",key="home_button2"):
            st.session_state.page_state="home"
            st.session_state["has_interacted"]=False # ボタンをクリックしたら非表示に設定

           # 苗の種類の選択をリセット
            st.session_state.selected_nae_type = ""
            # ページをリロードする
            st.rerun()

    if st.session_state.selected_nae_type:
        image_path = image_paths[st.session_state.selected_nae_type]
        image = Image.open(image_path)
        st.image(image, caption="", use_column_width=True)
     # 戻るボタンの実装
        # if st.button('戻る'):
        #     # ボタンが押されたときの処理
        #     st.session_state.page_state = "home"
        #     st.session_state.selected_name_type = ""
        #     st.rerun()

        # if st.button('戻る'):
        #     # ボタンが押されたときの処理
        #     page_state = "home"
        #     st.session_state.page_state = page_state
        #     st.session_state.selected_nae_type = ""
        #     st.rerun()

        exp_default_nae = load_yaml.load(r"src/data/default_nae_exp.yaml")
        text_dict = exp_default_nae["野菜"]

        selected_text = text_dict[st.session_state.selected_nae_type]
        st.write(selected_text)

        if st.button("読み上げ", key=f"voice_{selected_text}"):
            selected_text_display = st.session_state.get("selected_text", "")
            st.write(selected_text_display)
            file_path = f"audio_files/{st.session_state.selected_nae_type}.mp3"
            audio_file = open(file_path, "rb")
            st.audio(audio_file.read(), format="audio/mp3", start_time=0)
