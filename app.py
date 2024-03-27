import os
import streamlit as st
# import openai
# from dotenv import load_dotenv
import base64
import requests
import json
from PIL import Image
# from utils import chatgpt
from pathlib import Path
from pdf2image import convert_from_path


# #.envファイルから環境変数を読み込む
# load_dotenv()

#APIキーの設定
# openai.api_key=os.environ["OPENAI_API_KEY"]
#Goole Vision APIのクライアントを作成身元証明書のjson読み込み
# GOOGLE_CLOUD_VISION_API_URL='https://vision.googleapis.com/v1/images:annotate?key='

#APIを呼び、認識結果をjson型で返す

def request_cloud_vison_api(image_base64):
    api_url=GOOGLE_CLOUD_VISION_API_URL+API_KEY
    req_body=json.dumps({
    "requests":[{
        "image":{
            #jsonに変換するためにstring型に変換する
            "content":image_base64.decode("utf-8")},
            "features":[{
                #ここを変換することで分析内容を変更できる
                "type":"TEXT_DETECTION",
                "maxResults":10,}]
    }]
    })

    res=requests.post(api_url,data=req_body)
    return res.json()

#画像読み取り
def img_to_base64(filepath):
    with open(filepath,"rb") as img:
        img_byte=img.read()
    return base64.b64encode(img_byte)
    
def main():
 
    st.title("苗🌱チャットアプリ")
  
    # # printの出力結果をUTF-8に
    #     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    #     sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    uploaded_files = st.file_uploader("Choose a file",accept_multiple_files=True,type=["png"])

    if uploaded_files:
        st.write("アップロードされた画像：")
        for uploaded_file in uploaded_files:
            image=Image.open(uploaded_file)
            st.image(image,caption=uploaded_file.name,use_column_width=True)

            img_base64=img_to_base64(r"C:\Users\shige\OneDrive\Desktop\yamasu\苗チャット\image\\"+uploaded_file.name)
            result=request_cloud_vison_api(img_base64)

            #認識した文字を出力
            text_r=result["responses"][0]["fullTextAnnotation"]["text"]
            st.write(text_r)


    # #outputのファイルパス
    # pdf_save_dir="image_pdf"


# # 画像ファイルのディレクトリ
#     image_dir = r"C:\Users\shige\OneDrive\Desktop\yamasu\苗チャット\images"

#     # if not os.path.exists(image_dir):
#     #     os.makedirs(image_dir)
#     # for upload_file in upload_files:
#     #     img=Image.open(upload_file)
#     #     img.save(f'./images/{upload_file.name}')

#     # 画像ファイルの一覧を取得
#     # image_files = os.listdir(image_dir)

#     # 画像ファイルの一覧を取得
#     image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]


#     # 画像ファイル名からタブのタイトルを取得
#     tab_titles = [os.path.splitext(file)[0] for file in image_files]

#     # 処理を開始するボタン
#     if not st.button("処理開始"):
#         return
    
#     # タブを表示する
#     tabs = st.tabs(tab_titles)
        
#     for i, tab in enumerate(tabs):
#         with tab:
#             img_path=image_files[i] # i番目の画像ファイルのパス
#             img=Image.open(img_path)
    
#             img_base64=img_to_base64(img_path)
#             result=request_cloud_vison_api(img_base64)

#             #認識した文字を出力
#             text_r=result["responses"][0]["fullTextAnnotation"]["text"]
#             #ここからGPT-4

#             # 画像ファイルの一覧を取得
#             image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

#             result=chatgpt.execute(text=text_r)
#             result = st.text_input('保存ファイル名', result)
#             st.image(img,use_column_width=True)

    #タブを選択
    # selected_tab = st.selectbox("タブを選択", tab_titles)



# 選択されたタブに対応する画像を表示
    # if selected_tab:
    #     st.header(f"{selected_tab}")
    #     image_path =f"./{image_dir}/{selected_tab}.png"
    #     img=Image.open(image_path)
    #     st.image(img,width=200)
    #     img_base64=img_to_base64(image_path）；
    #     result=request_cloud_vison_api(img_base64)

    # tabs = st.selectbox("タブを選択", ["地産地消", "佐川", "関東"])

    # if tabs == "地産地消":
    #     st.header("A 地産地消")
    #     st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    # elif tabs == "佐川":
    #     st.header("A 佐川")
    #     st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    # elif tabs == "関東":
    #     st.header("A 関東")
    #     st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

        # tab1, tab2, tab3 = st.tabs(["地産地消", "佐川", "関東"])

        # with tab1:
        #     st.header("A 地産地消")
        #     st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

        # with tab2:
        #     st.header("A 佐川")
        #     st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

        # with tab3:
        #     st.header("A 関東")
        #     st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

    # num=3
    # col= st.beta_columns(num)

    # for i in list(range(0,num,1)):
    #     with col[i]:
    #         st.header("図"+str(i+1))
    #         st.image(str(i+1)+".png", use_column_width=True)

    # col1, col2, col3 = st.beta_columns(3)

    # with col1:
    #         st.header("地産地消")
    #         st.image("C:\Users\shige\OneDrive\Desktop\yamasu\電子帳簿\src\地産地消.png", use_column_width=True)

    # with col2:
    #         st.header("佐川")
    #         st.image("C:\Users\shige\OneDrive\Desktop\yamasu\電子帳簿\src\佐川.png", use_column_width=True)
            
    # with col3:
    #         st.header("関東")
    #         st.image("C:\Users\shige\OneDrive\Desktop\yamasu\電子帳簿\src\関東.png", use_column_width=True)
    
    # st.write(selected_tab)

#認識した文字を出力

        # text_r=result["responses"][0]["fullTextAnnotation"]["text"]
        # # st.write(f'{text_r}です')

        # #ここからGPT-4
        # result=chatgpt.execute(text=text_r)
        # result = st.text_input('保存ファイル名', result)
    
if __name__ =="__main__":
    main()

    # 辞書を作成（略称をキー、正式名称を値として）
# abbreviation_to_fullname = {
#     "JTEX": "職業訓練法人 日本技能教育開発センター",
#     "XYZ": "XYZ Industries",
#     "DEF": "DEF Incorporated",
#     # 他の略称と正式名称のペアを追加
# }

# # 略称を入力
# abbreviation = "JTEX"

# # 辞書を使って正式名称に変換
# if abbreviation in abbreviation_to_fullname:
#     full_name = abbreviation_to_fullname[abbreviation]
#     print("正式名称:", full_name)
# else:
#     print("略称が見つかりませんでした。")



