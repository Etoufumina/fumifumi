import streamlit as st
import random

# =========================
# カスタムCSS（レトロRPGテーマ）
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323:wght@400&display=swap');

/* 全体背景 */
.stApp {
    background-color: #0d0d1a;
    background-image:
        radial-gradient(ellipse at 20% 50%, #1a0a2e 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, #0a1a2e 0%, transparent 60%);
}

/* メインコンテンツ幅 */
.block-container {
    max-width: 720px !important;
    padding: 2rem 2rem !important;
}

/* タイトル */
h1 {
    font-family: 'Press Start 2P', monospace !important;
    color: #ffe066 !important;
    font-size: 1.2rem !important;
    text-shadow: 3px 3px 0px #b8860b, 0 0 20px #ffe06688 !important;
    text-align: center !important;
    letter-spacing: 2px !important;
    margin-bottom: 1.5rem !important;
}

/* h2 / h3 */
h2, h3 {
    font-family: 'Press Start 2P', monospace !important;
    color: #7ecfff !important;
    font-size: 0.75rem !important;
    text-shadow: 2px 2px 0px #0066aa !important;
}

/* 通常テキスト */
p, div, label, span {
    font-family: 'VT323', monospace !important;
    color: #e8e8d0 !important;
    font-size: 1.3rem !important;
}

/* 問題文カード */
.question-box {
    background: #111128;
    border: 3px solid #4444aa;
    border-image: none;
    box-shadow: 4px 4px 0px #2222aa, inset 0 0 30px #00001a;
    padding: 1.5rem 2rem;
    margin: 1rem 0 1.5rem 0;
    font-family: 'VT323', monospace;
    font-size: 1.6rem;
    color: #ffffff;
    line-height: 1.8;
    position: relative;
}
.question-box::before {
    content: '▶ ';
    color: #ffe066;
}

/* EXPバー */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00ff88, #00ccff) !important;
    box-shadow: 0 0 8px #00ff8888 !important;
}
.stProgress > div > div > div {
    background: #222244 !important;
    border: 2px solid #4444aa !important;
}

/* ラジオボタン */
.stRadio > div {
    background: #111128 !important;
    border: 2px solid #333366 !important;
    border-radius: 0 !important;
    padding: 0.8rem 1rem !important;
    margin: 0.3rem 0 !important;
    transition: border-color 0.15s, background 0.15s !important;
}
.stRadio > div:hover {
    border-color: #7777ff !important;
    background: #1a1a3a !important;
}
.stRadio label {
    font-family: 'VT323', monospace !important;
    font-size: 1.4rem !important;
    color: #ccccff !important;
    cursor: pointer !important;
}

/* ボタン */
.stButton > button {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.6rem !important;
    background: #1a1a3a !important;
    color: #ffe066 !important;
    border: 3px solid #ffe066 !important;
    border-radius: 0 !important;
    padding: 0.6rem 1.2rem !important;
    box-shadow: 4px 4px 0px #b8860b !important;
    transition: all 0.1s !important;
    letter-spacing: 1px !important;
}
.stButton > button:hover:not(:disabled) {
    background: #ffe066 !important;
    color: #0d0d1a !important;
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px #b8860b !important;
}
.stButton > button:active:not(:disabled) {
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0px #b8860b !important;
}
.stButton > button:disabled {
    opacity: 0.4 !important;
    cursor: not-allowed !important;
}

/* 正解・不正解メッセージ */
.stSuccess, .stError {
    font-family: 'VT323', monospace !important;
    font-size: 1.4rem !important;
    border-radius: 0 !important;
    border-left: 4px solid !important;
}
.stSuccess {
    background: #001a00 !important;
    border-color: #00ff88 !important;
    color: #00ff88 !important;
}
.stError {
    background: #1a0000 !important;
    border-color: #ff4444 !important;
    color: #ff4444 !important;
}

/* 難易度バッジ */
.badge {
    display: inline-block;
    font-family: 'Press Start 2P', monospace;
    font-size: 0.55rem;
    padding: 0.35rem 0.8rem;
    border: 2px solid;
    letter-spacing: 1px;
    margin-left: 0.5rem;
    vertical-align: middle;
}
.badge-easy   { color: #00ff88; border-color: #00ff88; background: #001a0d; box-shadow: 2px 2px 0 #00aa44; }
.badge-medium { color: #ffcc00; border-color: #ffcc00; background: #1a1000; box-shadow: 2px 2px 0 #aa8800; }
.badge-hard   { color: #ff4466; border-color: #ff4466; background: #1a0008; box-shadow: 2px 2px 0 #aa0022; }

/* 難易度アップ通知 */
.diff-up {
    font-family: 'Press Start 2P', monospace;
    font-size: 0.6rem;
    color: #ff4466;
    background: #1a0008;
    border: 2px solid #ff4466;
    box-shadow: 3px 3px 0 #aa0022;
    padding: 0.7rem 1rem;
    margin: 0.5rem 0;
    text-align: center;
    letter-spacing: 1px;
}

/* タイトル画面 */
.title-screen {
    text-align: center;
    padding: 2rem 0;
}
.title-logo {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.1rem;
    color: #ffe066;
    text-shadow: 4px 4px 0px #b8860b, 0 0 30px #ffe06699;
    line-height: 2.2;
    margin-bottom: 2rem;
}
.diff-card {
    background: #111128;
    border: 3px solid #333366;
    box-shadow: 4px 4px 0 #111144;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
}
.diff-card-easy   { border-left: 6px solid #00ff88; }
.diff-card-medium { border-left: 6px solid #ffcc00; }
.diff-card-hard   { border-left: 6px solid #ff4466; }
.diff-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 0.65rem;
    margin-bottom: 0.3rem;
}
.diff-desc {
    font-family: 'VT323', monospace;
    font-size: 1.2rem;
    color: #aaaacc;
}


/* サイドバー非表示 */
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# =========================
# 問題データ（各難易度10問）
# =========================

easy_questions = [
    {"text": "I ___ soccer yesterday.", "choices": ["play", "played", "playing", "plays"], "answer": "played", "exp": 10},
    {"text": "She ___ happy.", "choices": ["is", "are", "am", "be"], "answer": "is", "exp": 10},
    {"text": "They ___ students.", "choices": ["is", "am", "are", "be"], "answer": "are", "exp": 10},
    {"text": "He ___ to school every day.", "choices": ["go", "goes", "going", "went"], "answer": "goes", "exp": 10},
    {"text": "I ___ a book now.", "choices": ["read", "reads", "am reading", "was reading"], "answer": "am reading", "exp": 10},
    {"text": "We ___ dinner at 7 pm yesterday.", "choices": ["eat", "ate", "eating", "eats"], "answer": "ate", "exp": 10},
    {"text": "This is ___ apple.", "choices": ["a", "an", "the", "-"], "answer": "an", "exp": 10},
    {"text": "She ___ English well.", "choices": ["speak", "speaks", "speaking", "spoken"], "answer": "speaks", "exp": 10},
    {"text": "I ___ TV when she called.", "choices": ["watch", "watches", "was watching", "am watching"], "answer": "was watching", "exp": 10},
    {"text": "There ___ two cats on the table.", "choices": ["is", "are", "am", "be"], "answer": "are", "exp": 10},
]

medium_questions = [
    {"text": "If I ___ rich, I would travel the world.", "choices": ["am", "was", "were", "be"], "answer": "were", "exp": 20},
    {"text": "He has lived here ___ 2019.", "choices": ["for", "since", "during", "from"], "answer": "since", "exp": 20},
    {"text": "By the time she arrived, we ___ waiting for an hour.", "choices": ["have been", "had been", "were", "are"], "answer": "had been", "exp": 20},
    {"text": "She suggested ___ a walk.", "choices": ["take", "to take", "taking", "took"], "answer": "taking", "exp": 20},
    {"text": "I wish I ___ harder when I was young.", "choices": ["study", "studied", "had studied", "have studied"], "answer": "had studied", "exp": 20},
    {"text": "The cake ___ by my mother.", "choices": ["make", "made", "was made", "is making"], "answer": "was made", "exp": 20},
    {"text": "He talked as if he ___ everything.", "choices": ["knows", "knew", "had known", "know"], "answer": "knew", "exp": 20},
    {"text": "I ___ him since last Monday.", "choices": ["don't see", "didn't see", "haven't seen", "hadn't seen"], "answer": "haven't seen", "exp": 20},
    {"text": "It is important that he ___ on time.", "choices": ["is", "be", "was", "were"], "answer": "be", "exp": 20},
    {"text": "She is used to ___ early.", "choices": ["wake", "woke", "waking", "waken"], "answer": "waking", "exp": 20},
]

hard_questions = [
    {"text": "Hardly ___ when the train left.", "choices": ["I arrived", "had I arrived", "I had arrived", "arrived I"], "answer": "had I arrived", "exp": 30},
    {"text": "No sooner ___ than it started raining.", "choices": ["we arrived", "had we arrived", "we had arrived", "arrived we"], "answer": "had we arrived", "exp": 30},
    {"text": "Not until midnight ___ to sleep.", "choices": ["she went", "did she go", "she did go", "went she"], "answer": "did she go", "exp": 30},
    {"text": "Little ___ that he was being watched.", "choices": ["he knew", "knew he", "did he know", "he did know"], "answer": "did he know", "exp": 30},
    {"text": "___ harder, he would have passed the exam.", "choices": ["If he studied", "Had he studied", "If he had study", "He had studied"], "answer": "Had he studied", "exp": 30},
    {"text": "The findings, ___ last week, surprised everyone.", "choices": ["publish", "published", "publishing", "to publish"], "answer": "published", "exp": 30},
    {"text": "It was not until she left ___ realized how much he loved her.", "choices": ["that he", "when he", "which he", "and he"], "answer": "that he", "exp": 30},
    {"text": "She is ___ the most talented student I have ever taught.", "choices": ["by far", "so far", "as far", "thus far"], "answer": "by far", "exp": 30},
    {"text": "No matter ___ hard you try, you cannot do it alone.", "choices": ["what", "how", "however", "whatever"], "answer": "how", "exp": 30},
    {"text": "___ to his advice, she would have succeeded.", "choices": ["If she listened", "Had she listened", "She had listened", "If she had listen"], "answer": "Had she listened", "exp": 30},
]

# =========================
# 初期データ
# =========================

for key, val in [
    ("game_started", False), ("selected_difficulty", None),
    ("level", 1), ("exp", 0), ("current_question", None),
    ("question_number", 1), ("answered", False),
    ("used_easy", []), ("used_medium", []), ("used_hard", []),
    ("prev_difficulty", "easy"), ("diff_up_msg", False)
]:
    if key not in st.session_state:
        st.session_state[key] = val

# =========================
# ロジック関数
# =========================

def required_exp(level):
    return level * 100

def get_difficulty(level):
    if level < 5:
        return "easy"
    elif level < 10:
        return "medium"
    else:
        return "hard"

def add_exp(amount):
    st.session_state.exp += amount
    while st.session_state.exp >= required_exp(st.session_state.level):
        st.session_state.exp -= required_exp(st.session_state.level)
        st.session_state.level += 1
        st.balloons()
        st.success(f"★ LEVEL UP！ Lv.{st.session_state.level} に上がった！")
        # 難易度が変わったか確認
        new_diff = get_difficulty(st.session_state.level)
        if new_diff != st.session_state.prev_difficulty:
            st.session_state.prev_difficulty = new_diff
            st.session_state.diff_up_msg = True

def get_next_question():
    diff = st.session_state.selected_difficulty
    if diff == "easy":
        pool, used_key = easy_questions, "used_easy"
    elif diff == "medium":
        pool, used_key = medium_questions, "used_medium"
    else:
        pool, used_key = hard_questions, "used_hard"

    used = st.session_state[used_key]
    remaining = [i for i in range(len(pool)) if i not in used]
    if not remaining:
        st.session_state[used_key] = []
        remaining = list(range(len(pool)))

    idx = random.choice(remaining)
    st.session_state[used_key].append(idx)

    question = pool[idx].copy()
    choices = question["choices"][:]
    random.shuffle(choices)
    question["choices"] = choices
    return question

# 初回問題生成
if st.session_state.game_started and st.session_state.current_question is None:
    st.session_state.current_question = get_next_question()

# =========================
# UI描画
# =========================

st.title("⚔️ 英語クイズRPG ⚔️")

# -----------------------------------------------
# タイトル画面（難易度選択）
# -----------------------------------------------
if not st.session_state.game_started:

    st.markdown('<div class="title-screen">', unsafe_allow_html=True)
    st.markdown(
        '<div class="title-logo">ENGLISH<br>QUEST</div>',
        unsafe_allow_html=True
    )
    st.markdown("### 難易度を選んでください", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="diff-card diff-card-easy">'
            '<div class="diff-title" style="color:#00ff88">🟢 やさしい</div>'
            '<div class="diff-desc">基本的な文法<br>中学レベル<br>+10 EXP/問</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("やさしい でスタート"):
            st.session_state.selected_difficulty = "easy"
            st.session_state.game_started = True
            st.rerun()

    with col2:
        st.markdown(
            '<div class="diff-card diff-card-medium">'
            '<div class="diff-title" style="color:#ffcc00">🟡 ふつう</div>'
            '<div class="diff-desc">仮定法・受動態<br>高校レベル<br>+25 EXP/問</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("ふつう でスタート"):
            st.session_state.selected_difficulty = "medium"
            st.session_state.game_started = True
            st.rerun()

    with col3:
        st.markdown(
            '<div class="diff-card diff-card-hard">'
            '<div class="diff-title" style="color:#ff4466">🔴 むずかしい</div>'
            '<div class="diff-desc">倒置・高度な構文<br>大学入試レベル<br>+50 EXP/問</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("むずかしい でスタート"):
            st.session_state.selected_difficulty = "hard"
            st.session_state.game_started = True
            st.rerun()

# -----------------------------------------------
# ゲーム画面
# -----------------------------------------------
else:
    question = st.session_state.current_question
    level = st.session_state.level
    diff = st.session_state.selected_difficulty
    diff_label = {"easy": "やさしい", "medium": "ふつう", "hard": "むずかしい"}[diff]
    diff_class = {"easy": "badge-easy", "medium": "badge-medium", "hard": "badge-hard"}[diff]

    st.markdown(
        f'## Lv.{level}　<span class="badge {diff_class}">{diff_label}</span>',
        unsafe_allow_html=True
    )

    exp_ratio = st.session_state.exp / required_exp(level)
    st.progress(exp_ratio)
    st.markdown(f"EXP：{st.session_state.exp} / {required_exp(level)}")

    st.markdown("---")

    st.markdown(f"### 問題 {st.session_state.question_number}")
    st.markdown(
        f'<div class="question-box">{question["text"]}</div>',
        unsafe_allow_html=True
    )

    selected = st.radio(
        "こたえを選んでください",
        question["choices"],
        key=f"radio_{st.session_state.question_number}"
    )

    st.markdown("")

    # 難易度ごとのEXP（問題データのexpより優先）
    diff_exp = {"easy": 10, "medium": 25, "hard": 50}[diff]

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("⚔️ 回答する", disabled=st.session_state.answered):
            if selected == question["answer"]:
                add_exp(diff_exp)
                st.success(f"✔ せいかい！　+{diff_exp} EXP　獲得！")
            else:
                st.error(f"✘ ちがう！　正解は「{question['answer']}」だった！")
            # 正解・不正解どちらもすぐ次の問題へ
            import time
            time.sleep(1.2)
            st.session_state.current_question = get_next_question()
            st.session_state.question_number += 1
            st.session_state.answered = False
            st.rerun()

    with col2:
        if st.button("🏠 タイトルへ"):
            for key in ["game_started", "selected_difficulty", "level", "exp",
                        "current_question", "question_number", "answered",
                        "used_easy", "used_medium", "used_hard",
                        "prev_difficulty", "diff_up_msg"]:
                del st.session_state[key]
            st.rerun()