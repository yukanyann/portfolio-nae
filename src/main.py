import os
import uuid

import openai
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv
from gtts import gTTS
from sidebar import display_default_nae
from st_audiorec import st_audiorec
from utils import chatgpt
from utils.google_cloud import transcribe_audio_to_text
from google.cloud import texttospeech
from utils.google_cloud import execute

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# #Google Vison APIのクライアントを作成身元証明書のjson読み込み
# GOOGLE_CLOUD_VISON_API_URL = os.environ["GOOGLE_CLOUD_VISON_API_URL"]
# GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("selected_nae_type", [])
st.session_state.setdefault("user_input", "")


def main():

     
    st.markdown("<h1 style='text-align: center;'>苗🌱チャットアプリ</h1>", unsafe_allow_html=True) 
    with st.sidebar:
        st.write("こんにちは👋")
          # ユーザーからの入力を受け取る
        user_input = st.text_input("★ご質問を記載下さい！又は音声ボタン🎙️を押してお話下さい。（話し終わったら再度タップ！）", st.session_state.user_input)

        if user_input:
            st.session_state.user_input = user_input
            st.session_state["has_interacted"]=True # ユーザーが操作したことを記録
    # ユーザー入力が存在する場合、送信ボタンを表示
    submit_flg = False
    if st.session_state.user_input != "":
        submit_flg = st.sidebar.button("送信")

    # defalut_naeの表示
    display_default_nae.display()

    # テキスト入力があるか確認
    if submit_flg:
        with st.spinner("考え中です..."):
            chatbot_response =chatgpt.execute(st.session_state.user_input)
            
        response_id = str(uuid.uuid4())
        st.session_state.chat_history.append({"ai": chatbot_response, "id": response_id})
        st.session_state.chat_history.append({"user": st.session_state.user_input, "id": str(uuid.uuid4())})

        st.session_state.user_input = ""

        # for chat_dict in st.session_state.chat_history:
        #     key = list(chat_dict.keys())[0]
        #     if key == "user":
        #         with st.chat_message("user", avatar="😊"):
        #             st.write(chat_dict[key])
        #     else:
        #         with st.chat_message("ai", avatar="🤖"):
        #             st.write(chat_dict[key])
    if "chat_history" in st.session_state: # chat_historyがsession_stateに存在するかを確認
        for chat_dict in reversed(st.session_state["chat_history"]):
            key = list(chat_dict.keys())[0]
            if key == "user":
                with st.chat_message("user", avatar="😊"):
                    st.write(chat_dict[key])
            else:
                with st.chat_message("ai", avatar="🤖"):
                    st.write(chat_dict[key])

                    if st.button("読み上げ", key=f"voice_{chat_dict['id']}"):
                        with st.spinner("音声生成中..."):
                     # 音声ファイルの生成
                            audio_file=execute(chat_dict[key], "日本語", "reading")
            # Streamlitで音声ファイルを提供
                            st.audio(audio_file, format="audio/mp3", start_time=0)
            # 一時ファイルを削除
                            os.remove(audio_file)

if __name__ == "__main__":
    main()
