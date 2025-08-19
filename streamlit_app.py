import streamlit as st
import spacy
import subprocess
import sys
 
# spaCyモデルのインストールチェック
@st.cache_resource
def load_spacy_model():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        st.info("英語モデルをダウンロード中...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")
    return nlp
 
# spaCyモデルの読み込み
nlp = load_spacy_model()
 
st.title("英文SVO抽出アプリ")
 
# サンプル文の提供
sample_text = """John reads books.
Mary likes coffee.
The cat chased the mouse in the garden.
Students are studying mathematics.
She gave him a present."""
 
text = st.text_area(
    "英文を入力してください", 
    value=sample_text,
    height=200,
    help="英文を入力すると、SVO（主語・動詞・目的語）構造を抽出します"
)
 
def extract_svo(doc):
    """
    改良版SVO抽出関数
    各動詞を中心に、その主語と目的語を正しく関連付けて抽出
    """
    svos = []
    for sent in doc.sents:
        # 各文について処理
        for token in sent:
            # 動詞を中心に探索（ROOTまたは動詞）
            if token.pos_ == "VERB" or token.dep_ == "ROOT":
                subject = None
                verb = token.text
                obj = None
                # この動詞の子要素から主語と目的語を探す
                for child in token.children:
                    # 主語の検出（nsubj, nsubjpassなど）
                    if "subj" in child.dep_:
                        # 複合主語の場合、全体を取得
                        subject = get_compound_phrase(child)
                    # 直接目的語の検出（dobj）
                    elif child.dep_ == "dobj":
                        obj = get_compound_phrase(child)
                    # 前置詞目的語の検出（pobj）- 目的語がない場合の代替
                    elif child.dep_ == "pobj" and obj is None:
                        obj = get_compound_phrase(child)
                # 助動詞がある場合、動詞句全体を取得
                verb_phrase = get_verb_phrase(token)
                if verb_phrase:
                    verb = verb_phrase
                # SVO構造が完成している場合のみ追加
                if subject and verb and obj:
                    svos.append((subject, verb, obj))
    return svos
 
def get_compound_phrase(token):
    """
    複合語句（形容詞修飾など）を含む完全なフレーズを取得
    """
    phrase_parts = []
    # 左側の修飾語を取得
    for child in token.children:
        if child.dep_ in ["compound", "amod", "det", "poss"]:
            if child.i < token.i:  # トークンの前にある場合
                phrase_parts.append(child.text)
    # メイントークンを追加
    phrase_parts.append(token.text)
    # 右側の修飾語を取得
    for child in token.children:
        if child.dep_ in ["compound", "prep"]:
            if child.i > token.i:  # トークンの後にある場合
                phrase_parts.append(child.text)
    return " ".join(phrase_parts)
 
def get_verb_phrase(token):
    """
    助動詞を含む動詞句全体を取得
    """
    verb_parts = []
    # 助動詞を探す
    for child in token.children:
        if child.dep_ in ["aux", "auxpass"] and child.i < token.i:
            verb_parts.append(child.text)
    # 動詞自体を追加
    verb_parts.append(token.text)
    # 動詞句がある場合のみ返す
    if len(verb_parts) > 1:
        return " ".join(verb_parts)
    return None
 
# デバッグ情報表示のオプション
show_debug = st.checkbox("詳細な解析結果を表示", value=False)
 
if st.button("SVOを抽出", type="primary"):
    if text:
        doc = nlp(text)
        # デバッグ情報の表示
        if show_debug:
            st.subheader("依存構造解析結果：")
            for sent in doc.sents:
                st.write(f"**文:** {sent.text}")
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
            st.subheader("🎯 抽出されたSVO構造：")
            for i, (s, v, o) in enumerate(svos, 1):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"**主語:** {s}")
                with col2:
                    st.success(f"**動詞:** {v}")
                with col3:
                    st.warning(f"**目的語:** {o}")
        else:
            st.warning("SVO構造が見つかりませんでした。完全なSVO構造を持つ文を入力してください。")
            st.info("💡 ヒント: 「Subject + Verb + Object」の形式の文を入力してください。例: 'John reads books.'")
    else:
        st.error("英文を入力してください。")
 
# 使い方の説明
with st.expander("📖 使い方"):
    st.markdown("""
    ### このアプリについて
    このアプリは、英文から**SVO（主語・動詞・目的語）**構造を自動的に抽出します。
    ### 対応する文の例：
    - ✅ John reads books. （ジョンは本を読む）
    - ✅ The cat chased the mouse. （猫がネズミを追いかけた）
    - ✅ She is writing a letter. （彼女は手紙を書いている）
    ### 注意事項：
    - 完全なSVO構造を持つ文のみが抽出されます
    - 複雑な文章の場合、すべてのSVO構造が抽出されない場合があります
    - 受動態や特殊な構文には対応していない場合があります
    """)