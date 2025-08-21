import streamlit as st
import spacy
import subprocess
import importlib
import os

# モデル名
MODEL_NAME = "en_core_web_sm"

# モデル読み込み関数（キャッシュ付き）
@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load(MODEL_NAME)
    except OSError:
        # モデルが見つからなければインストール
        st.warning(f"spaCyモデル「{MODEL_NAME}」が見つかりません。インストールを試みます...")
        try:
            result = subprocess.run(
                ["python", "-m", "spacy", "download", MODEL_NAME],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                raise RuntimeError(result.stderr)
            importlib.invalidate_caches()
            return spacy.load(MODEL_NAME)
        except Exception as e:
            st.error(f"モデルのインストールに失敗しました: {e}")
            return None

# モデル読み込み
nlp = load_spacy_model()

# UI部分
st.title("spaCy 英語テキスト解析アプリ")

text = st.text_area("解析したい英語テキストを入力してください", "Apple is looking at buying U.K. startup for $1 billion.")

if nlp and text:
    doc = nlp(text)
    st.subheader("単語と品詞の解析結果")
    for token in doc:
        st.write(f"{token.text} → {token.pos_}")
elif not nlp:
    st.stop()
