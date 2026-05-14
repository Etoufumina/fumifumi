import streamlit as st
import random
import streamlit as st
import random

# =========================
# 初期データ
# =========================

if "level" not in st.session_state:
    st.session_state.level = 1

if "exp" not in st.session_state:
    st.session_state.exp = 0

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "answered" not in st.session_state:
    st.session_state.answered = False

# =========================
# 問題データ
# =========================

easy_questions = [
    {
        "text": "I ___ soccer yesterday.",
        "choices": ["play", "played", "playing", "plays"],
        "answer": "played",
        "exp": 10
    },
    {
        "text": "She ___ happy.",
        "choices": ["is", "are", "am", "be"],
        "answer": "is",
        "exp": 10
    }
]

medium_questions = [
    {
        "text": "If I ___ rich, I would travel the world.",
        "choices": ["am", "was", "were", "be"],
        "answer": "were",
        "exp": 20
    },
    {
        "text": "He has lived here ___ 2019.",
        "choices": ["for", "since", "during", "from"],
        "answer": "since",
        "exp": 20
    }
]

hard_questions = [
    {
        "text": "Hardly ___ when the train left.",
        "choices": ["I arrived", "had I arrived", "I had arrived", "arrived I"],
        "answer": "had I arrived",
        "exp": 30
    },
    {
        "text": "No sooner ___ than it started raining.",
        "choices": ["we arrived", "had we arrived", "we had arrived", "arrived we"],
        "answer": "had we arrived",
        "exp": 30
    }
]

# =========================
# 必要経験値
# =========================

def required_exp(level):
    return level * 100

# =========================
# レベルアップ
# =========================

def add_exp(amount):
    st.session_state.exp += amount

    while st.session_state.exp >= required_exp(st.session_state.level):
        st.session_state.exp -= required_exp(st.session_state.level)
        st.session_state.level += 1
        st.balloons()
        st.success(f"🎉 レベルアップ！ Lv.{st.session_state.level}")

# =========================
# レベル別問題取得
# =========================

def get_question_pool():
    level = st.session_state.level

    if level < 5:
        return easy_questions
    elif level < 10:
        return medium_questions
    else:
        return hard_questions

# =========================
# ランダム問題
# =========================

def generate_random_question():
    questions = get_question_pool()
    return random.choice(questions)

# =========================
# 初回問題生成
# =========================

if st.session_state.current_question is None:
    st.session_state.current_question = generate_random_question()

question = st.session_state.current_question

# =========================
# UI
# =========================

st.title("🎮 英語クイズRPG")

st.write(f"## Lv.{st.session_state.level}")

exp_ratio = st.session_state.exp / required_exp(st.session_state.level)
st.progress(exp_ratio)

st.write(
    f"EXP: {st.session_state.exp} / "
    f"{required_exp(st.session_state.level)}"
)

st.write(f"### 問題 {st.session_state.question_number}")
st.write(question["text"])

selected = st.radio(
    "選択してください",
    question["choices"],
    key=f"radio_{st.session_state.question_number}"  # ← キー名を明示的に変更
)

# =========================
# 回答ボタン
# =========================

if st.button("回答する", disabled=st.session_state.answered):

    st.session_state.answered = True

    if selected == question["answer"]:
        st.success(f"正解！ +{question['exp']} EXP")
        add_exp(question["exp"])
    else:
        st.error(f"不正解！ 正解: {question['answer']}")

# =========================
# 次の問題
# =========================

if st.button("次の問題へ"):
    st.session_state.current_question = generate_random_question()
    st.session_state.question_number += 1
    st.session_state.answered = False   # ← 回答済みフラグをリセット
    st.rerun()