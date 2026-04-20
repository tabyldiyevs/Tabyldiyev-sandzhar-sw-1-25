import streamlit as st
import pandas as pd
import os
from datetime import date

# Файл для хранения данных (Требование хакатона №24)
DATA_FILE = "student_budget.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Дата", "Категория", "Сумма", "Тип"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Загрузка базы
df = load_data()

st.set_page_config(page_title="Atyrau Student Budget", page_icon="💸")
st.title("💸 Студенческий бюджет (Атырау)")
st.write("Приложение для контроля расходов в общежитии.")

# Функция 1: Добавление записи (Требование №23)
st.sidebar.header("Добавить операцию")
with st.sidebar.form("add_form", clear_on_submit=True):
    op_type = st.radio("Тип", ["Расход", "Доход"])
    amount = st.number_input("Сумма (₸)", min_value=0, step=100)
    category = st.selectbox("Категория", ["Еда", "Транспорт", "Стипендия", "Учеба", "Связь", "Другое"])
    submitted = st.form_submit_button("Сохранить")

if submitted:
    if amount > 0: # Защита от неправильного ввода (Требование №25)
        new_entry = pd.DataFrame([[date.today(), category, amount, op_type]], 
                                 columns=["Дата", "Категория", "Сумма", "Тип"])
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
        st.sidebar.success("Запись добавлениа!")
    else:
        st.sidebar.error("Сумма должна быть больше 0")

# Функция 2: Просмотр и фильтрация (Требование №23)
st.subheader("📊 История ваших транзакций")
if not df.empty:
    filter_choice = st.multiselect("Фильтр по категориям:", df["Категория"].unique(), default=df["Категория"].unique())
    filtered_df = df[df["Категория"].isin(filter_choice)]
    st.dataframe(filtered_df, use_container_width=True)
    
    # Бонус: Визуализация (график трат)
    st.divider()
    st.subheader("Визуализация расходов")
    expenses_only = df[df["Тип"] == "Расход"]
    if not expenses_only.empty:
        st.bar_chart(expenses_only.groupby("Категория")["Сумма"].sum())
    else:
        st.info("Добавьте расходы, чтобы увидеть график.")
else:
    st.info("Данных пока нет. Добавьте первую операцию в боковом меню.")
