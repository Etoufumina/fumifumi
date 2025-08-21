import streamlit as st
import spacy
import subprocess
import importlib

MODEL_NAME = "en_core_web_sm"

@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load(MODEL_NAME)
    except OSError:
        st.warning(f"spaCyモデル「{MODEL_NAME}」が見つかりません。インストール中です...")
        subprocess.run(["python", "-m", "spacy", "download", MODEL_NAME])
        importlib.invalidate_caches()
        return spacy.load(MODEL_NAME)

nlp = load_spacy_model()

# SVO抽出関数
def extract_svo(doc):
    svos = []
    for token in doc:
        # 動詞を探す
        if token.pos_ == "VERB":
            subj = ""
            obj = ""

            # 主語を探す
            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    subj = child.text

            # 目的語を探す
            for child in token.children:
                if child.dep_ in ("dobj", "pobj", "attr"):
                    obj = child.text

            if subj and obj:
                svos.append((subj, token.text, obj))
    return svos

# UI表示
st.title("spaCyでSVO構造を抽出")

text = st.text_area("英語の文章を入力してください", "Apple is looking at buying a UK startup for $1 billion.")

if text and nlp:
    doc = nlp(text)
    svos = extract_svo(doc)

    if svos:
        st.subheader("抽出されたSVO構造:")
        for subj, verb, obj in svos:
            st.write(f"主語: {subj}, 動詞: {verb}, 目的語: {obj}")
    else:
        st.info("SVO構造が見つかりませんでした。文が単純なSVO構造であることを確認してください。")

    # 任意：全文の依存関係を確認したい場合
    with st.expander("全文の依存構文解析結果を見る"):
        for token in doc:
            st.write(f"{token.text:<12} | {token.dep_:<10} | head: {token.head.text}")
