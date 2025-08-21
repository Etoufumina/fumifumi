import streamlit as st
import spacy
import subprocess
import importlib

# 使用するspaCyモデル名
MODEL_NAME = "en_core_web_sm"

# spaCyモデルの読み込み（なければ自動インストール）＋キャッシュ
@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load(MODEL_NAME)
    except OSError:
        try:
            st.warning(f"spaCyモデル「{MODEL_NAME}」が見つかりません。ダウンロードを開始します。")
            subprocess.run(["python", "-m", "spacy", "download", MODEL_NAME], check=True)
            importlib.invalidate_caches()
            return spacy.load(MODEL_NAME)
        except Exception as e:
            st.error(f"モデルのダウンロードに失敗しました。詳細: {e}")
            return None

# SVO抽出関数
def extract_svo(doc):
    svos = []
    for token in doc:
        if token.pos_ == "VERB":
            subject = ""
            obj = ""

            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    subject = child.text

            for child in token.children:
                if child.dep_ in ("dobj", "pobj", "attr"):
                    obj = child.text

            if subject and obj:
                svos.append((subject, token.text, obj))

    return svos

# -----------------------------
# Streamlit アプリ部分
# -----------------------------

st.set_page_config(page_title="SVO抽出アプリ", layout="centered")
st.title("🧠 spaCyを使った英語のSVO抽出")

text = st.text_area("✏️ 英語の文章を入力してください", "Elon Musk founded SpaceX in 2002.")

if text.strip():
    nlp = load_spacy_model()
    if nlp is not None:
        try:
            doc = nlp(text)
            svos = extract_svo(doc)

            if svos:
                st.subheader("✅ 抽出されたSVO:")
                for subj, verb, obj in svos:
                    st.write(f"🔹 主語: **{subj}**　|　動詞: **{verb}**　|　目的語: **{obj}**")
            else:
                st.info("SVO構造が見つかりませんでした。文章が単純な SVO 形式であることを確認してください。")

            with st.expander("📖 詳細なトークン解析（依存構文など）"):
                st.write("単語　|　品詞　|　係り受け　|　係り先")
                for token in doc:
                    st.write(f"{token.text:<12} | {token.pos_:<6} | {token.dep_:<10} | {token.head.text}")
        except Exception as e:
            st.error(f"解析中にエラーが発生しました: {e}")
    else:
        st.stop()
else:
    st.info("英語の文を入力してください。")
