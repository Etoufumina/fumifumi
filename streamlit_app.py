import streamlit as st

# 初期データ
if "level" not in st.session_state:
    st.session_state.level = 1

if "exp" not in st.session_state:
    st.session_state.exp = 0

# 問題データ
question = {
    "text": "I ___ soccer yesterday.",
    "choices": ["play", "played", "playing", "plays"],
    "answer": "played",
    "exp": 20
}

# 必要経験値
def required_exp(level):
    return level * 100

# レベルアップ処理
def add_exp(amount):
    st.session_state.exp += amount

    while st.session_state.exp >= required_exp(st.session_state.level):
        st.session_state.exp -= required_exp(st.session_state.level)
        st.session_state.level += 1
        st.success(f"🎉 レベルアップ！ Lv.{st.session_state.level}")

# UI
st.title("英語クイズRPG")

st.write(f"## Lv.{st.session_state.level}")
st.progress(
    st.session_state.exp / required_exp(st.session_state.level)
)

st.write(question["text"])

answer = st.radio(
    "答えを選んでください",
    question["choices"]
)

if st.button("回答する"):
    if answer == question["answer"]:
        st.success("正解！ +20EXP")
        add_exp(question["exp"])
    else:
        st.error("不正解")
