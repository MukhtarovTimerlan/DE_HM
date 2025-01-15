import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache
def load_data():
    return pd.read_csv('data/raw/moscow_flats_dataset.csv')

data = load_data()


st.title("EDA для недвижимости в Москве")


st.markdown("Этот дашборд позволяет исследовать основные зависимости в данных по недвижимости.")


num_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
st.sidebar.header("Настройки")
selected_columns = st.sidebar.multiselect("Выберите числовые колонки для анализа", num_columns, default=num_columns)


st.subheader("Распределение значений (Boxplots)")
fig, axes = plt.subplots(nrows=(len(selected_columns) + 1) // 2, ncols=2, figsize=(15, 5 * ((len(selected_columns) + 1) // 2)))
axes = axes.flatten()

for idx, feature in enumerate(selected_columns):
    sns.boxplot(x=data[feature], ax=axes[idx])
    axes[idx].set_title(f"Распределение {feature}")

for ax in axes[len(selected_columns):]:
    ax.remove()

st.pyplot(fig)

st.subheader("Гистограмма цен")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data['price'], bins=30, kde=True, ax=ax)
ax.set_title("Распределение цен")
ax.set_xlabel("Цена")
st.pyplot(fig)

st.subheader("Гистограммы других колонок")
for col in selected_columns:
    if col != 'price':
        st.subheader(f"Распределение {col}")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data[col], bins=30, kde=True, ax=ax)
        st.pyplot(fig)

st.subheader("Корреляции числовых данных")
fig, ax = plt.subplots(figsize=(10, 8))
corr_matrix = data[selected_columns].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Тепловая карта корреляций")
st.pyplot(fig)

st.subheader("Зависимость цены от других признаков")
fig, axes = plt.subplots(nrows=(len(selected_columns) + 1) // 2, ncols=2, figsize=(15, 5 * ((len(selected_columns) + 1) // 2)))
axes = axes.flatten()

for idx, feature in enumerate(selected_columns):
    if feature != 'price':
        data.plot(x=feature, y="price", kind="scatter", ax=axes[idx], title=f"Price vs {feature}")

for ax in axes[len(selected_columns):]:
    ax.remove()

plt.tight_layout()
st.pyplot(fig)
