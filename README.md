import streamlit as st
import spacy
import en_core_web_sm  # 直接インポート

# Streamlit Share用のモデル読み込み
@st.cache_resource
def load_spacy_model():
    """Streamlit Share環境でも動作するモデル読み込み"""
    try:
        # 方法1: 直接読み込み（Streamlit Share推奨）
        nlp = en_core_web_sm.load()
    except:
        try:
            # 方法2: 通常の読み込み（ローカル環境）
            nlp = spacy.load("en_core_web_sm")
        except:
            st.error("spaCyモデルの読み込みに失敗しました。")
            st.stop()
    return nlp

# spaCyモデルの読み込み
nlp = load_spacy_model()

st.title("🔍 英文SVO抽出アプリ")
st.markdown("英文から**主語(Subject)・動詞(Verb)・目的語(Object)**を自動抽出します")

# サイドバーに説明を追加
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

# メインコンテンツ
sample_text = """John reads books.
Mary likes coffee.
The cat chased the mouse in the garden.
Students are studying mathematics.
She gave him a present."""

text = st.text_area(
    "英文を入力してください", 
    value=sample_text,
    height=150,
    help="英文を入力すると、SVO構造を抽出します"
)

def extract_svo(doc):
    """改良版SVO抽出関数"""
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
    """複合語句を含む完全なフレーズを取得"""
    phrase_parts = []
    
    for child in token.children:
        if child.dep_ in ["compound", "amod", "det", "poss"]:
            if child.i < token.i:
                phrase_parts.append(child.text)
    
    phrase_parts.append(token.text)
    
    for child in token.children:
        if child.dep_ in ["compound", "prep"]:
            if child.i > token.i:
                phrase_parts.append(child.text)
    
    return " ".join(phrase_parts)

def get_verb_phrase(token):
    """助動詞を含む動詞句全体を取得"""
    verb_parts = []
    
    for child in token.children:
        if child.dep_ in ["aux", "auxpass"] and child.i < token.i:
            verb_parts.append(child.text)
    
    verb_parts.append(token.text)
    
    if len(verb_parts) > 1:
        return " ".join(verb_parts)
    return None

# デバッグ情報表示のオプション
show_debug = st.checkbox("詳細な解析結果を表示", value=False)

# 抽出ボタン
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    extract_button = st.button("🎯 SVOを抽出", type="primary", use_container_width=True)

if extract_button:
    if text:
        with st.spinner('解析中...'):
            doc = nlp(text)
            
            # デバッグ情報の表示
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
            
            # SVO抽出
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
                
                # 結果のサマリー
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