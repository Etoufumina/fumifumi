import streamlit as st
import random

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

if "used_easy" not in st.session_state:
    st.session_state.used_easy = []

if "used_medium" not in st.session_state:
    st.session_state.used_medium = []

if "used_hard" not in st.session_state:
    st.session_state.used_hard = []

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
# レベル別問題取得（重複なし・選択肢シャッフル）
# =========================

def get_next_question():
    level = st.session_state.level

    if level < 5:
        pool = easy_questions
        used_key = "used_easy"
    elif level < 10:
        pool = medium_questions
        used_key = "used_medium"
    else:
        pool = hard_questions
        used_key = "used_hard"

    used = st.session_state[used_key]

    # 全問出題済みならリセット
    remaining = [i for i in range(len(pool)) if i not in used]
    if not remaining:
        st.session_state[used_key] = []
        remaining = list(range(len(pool)))

    idx = random.choice(remaining)
    st.session_state[used_key].append(idx)

    question = pool[idx].copy()

    # 選択肢をシャッフル
    choices = question["choices"][:]
    random.shuffle(choices)
    question["choices"] = choices

    return question

# =========================
# 初回問題生成
# =========================

if st.session_state.current_question is None:
    st.session_state.current_question = get_next_question()

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
    key=f"radio_{st.session_state.question_number}"
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
    st.session_state.current_question = get_next_question()
    st.session_state.question_number += 1
    st.session_state.answered = False
    st.rerun()