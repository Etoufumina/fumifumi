import streamlit as st
import spacy
import subprocess
import importlib

# spaCyモデル読み込み（必要ならダウンロード）
@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.warning("spaCy モデルが見つかりません。ダウンロード中です...")
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        importlib.invalidate_caches()
        return spacy.load("en_core_web_sm")

# モデルロード
nlp = load_spacy_model()

# サンプルテキスト
sample_text = """John reads books.
Mary likes coffee.
The cat chased the mouse in the garden.
Students are studying mathematics.
She gave him a present."""

# UI - タイトルと説明
st.title("🔍 英文SVO抽出アプリ")
st.markdown("英文から**主語(Subject)・動詞(Verb)・目的語(Object)**を自動抽出します")

# サイドバー
with st.sidebar:
    st.header("📖 使い方")
    st.markdown("""
    1. 英文を入力欄に入力  
    2. 「SVOを抽出」ボタンをクリック  
    3. 抽出されたSVO構造を確認
    
    ### 対応する文の例：
    - John reads books.
    - Mary likes coffee.
    - The cat chased the mouse.
    """)
    
    st.header("ℹ️ About")
    st.markdown("""
    このアプリはspaCyの自然言語処理を使用して  
    英文の構造を解析しています。
    
    [GitHub](https://github.com/yourusername/yourrepo)
    """)

# テキスト入力欄
text = st.text_area(
    "英文を入力してください", 
    value=sample_text,
    height=150,
    help="英文を入力すると、SVO構造を抽出します"
)

# SVO抽出処理
def extract_svo(doc):
    """SVO抽出関数"""
    svos = []
    for sent in doc.sents:
        for token in sent:
            if token.pos_ == "VERB" or token.dep_ == "ROOT":
                subject = None
                verb = token.text
                obj = None
                
                for child in token.children:
                    if "subj" in child.dep_:
                        subject = get_compound_phrase(child)
                    elif child.dep_ == "dobj":
                        obj = get_compound_phrase(child)
                    elif child.dep_ == "pobj" and obj is None:
                        obj = get_compound_phrase(child)
                
                verb_phrase = get_verb_phrase(token)
                if verb_phrase:
                    verb = verb_phrase
                
                if subject and verb and obj:
                    svos.append((subject, verb, obj))
    return svos

def get_compound_phrase(token):
    """複合語句を含む主語や目的語の完全なフレーズを取得"""
    phrase_parts = []

    for child in token.children:
        if child.dep_ in ["compound", "amod", "det", "poss"] and child.i < token.i:
            phrase_parts.append(child.text)

    phrase_parts.append(token.text)

    for child in token.children:
        if child.dep_ in ["compound", "prep"] and child.i > token.i:
            phrase_parts.append(child.text)

    return " ".join(phrase_parts)

def get_verb_phrase(token):
    """助動詞を含む動詞句全体を取得"""
    verb_parts = []
    for child in token.children:
        if child.dep_ in ["aux", "auxpass"] and child.i < token.i:
            verb_parts.append(child.text)
    verb_parts.append(token.text)
    return " ".join(verb_parts) if len(verb_parts) > 1 else None

# チェックボックスで詳細表示
show_debug = st.checkbox("詳細な解析結果を表示", value=False)

# 抽出ボタン
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    extract_button = st.button("🎯 SVOを抽出", type="primary", use_container_width=True)

# ボタンが押されたときの処理
if extract_button:
    if text:
        with st.spinner('解析中...'):
            doc = nlp(text)

            if show_debug:
                st.subheader("依存構造解析結果：")
                for sent in doc.sents:
                    with st.expander(f"文: {sent.text[:50]}..."):
                        debug_data = []
                        for token in sent:
                            debug_data.append({
                                "単語": token.text,
                                "品詞": token.pos_,
                                "依存関係": token.dep_,
                                "親": token.head.text if token.head != token else "ROOT"
                            })
                        st.table(debug_data)

            svos = extract_svo(doc)

            if svos:
                st.subheader("✨ 抽出されたSVO構造")
                for i, (s, v, o) in enumerate(svos, 1):
                    with st.container():
                        st.markdown(f"### 文 {i}")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("主語 (S)", s)
                        with col2:
                            st.metric("動詞 (V)", v)
                        with col3:
                            st.metric("目的語 (O)", o)
                        st.markdown("---")
                st.success(f"✅ {len(svos)}個のSVO構造を抽出しました！")
            else:
                st.warning("⚠️ SVO構造が見つかりませんでした。")
                st.info("""
                💡 **ヒント:**  
                - 完全なSVO構造を持つ文を入力してください  
                - 例: "John reads books." "She loves music."
                """)
    else:
        st.error("❌ 英文を入力してください。")

# フッター
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <small>Made with ❤️ using Streamlit and spaCy</small>
    </div>
    """,
    unsafe_allow_html=True
)
