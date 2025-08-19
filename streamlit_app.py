import streamlit as st
import  streamlit as st
import spacy # pyright: ignore[reportMissingImports]

# spaCyの英語モデルを読み込む
nlp = spacy.load("en_core_web_sm")

st.title("英文SVO抽出アプリ")

text = st.text_area("英文を入力してください", height=200)

def extract_svo(doc):
    svos = []
    for sent in doc.sents:
        subject = None
        verb = None
        obj = None
        for token in sent:
            # 主語の検出
            if "subj" in token.dep_:
                subject = token.text
            # 動詞の検出
            if token.pos_ == "VERB":
                verb = token.text
            # 目的語の検出
            if "obj" in token.dep_:
                obj = token.text
        if subject and verb and obj:
            svos.append((subject, verb, obj))
    return svos

if st.button("SVOを抽出"):
    if text:
        doc = nlp(text)
        svos = extract_svo(doc)

        if svos:
            st.subheader("抽出されたSVO構造：")
            for i, (s, v, o) in enumerate(svos, 1):
                st.write(f"{i}. 主語: `{s}` | 動詞: `{v}` | 目的語: `{o}`")
        else:
            st.warning("SVO構造が見つかりませんでした。")
    else:
        st.warning("英文を入力してください。")


