import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="E-Commerce Executive Dashboard",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
    <style>
    .stAppViewContainer {
        background-color: #121212 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #FFFF00 !important;
        border-right: 2px solid #E6B800 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
        font-weight: 700;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #0f172a !important;
        opacity: 0.3;
    }
    section[data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    section[data-testid="stSidebar"] [data-testid="stImage"] img {
        transform: scale(1.25);
        margin-top: 10px;
        margin-bottom: 10px;
    }
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    .stMarkdown p {
        color: #F3F4F6 !important;
        font-weight: 600;
    }
    .stCaption {
        color: #9CA3AF !important;
        font-weight: 600;
    }
    div[data-testid="stMetric"] {
        background: #1e1e1e !important;
        border: 2px solid #FFD700 !important;
        border-radius: 14px;
        padding: 24px 15px !important;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2);
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }
    div[data-testid="stMetric"] > div {
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    div[data-testid="stMetric"] label {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 1.55rem !important;
        margin-bottom: 8px !important;
        text-align: center !important;
    }
    div[data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #FFD700 !important;
        font-weight: 900 !important;
        font-size: 2.3rem !important;
        white-space: nowrap;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

COLOR_BLUE_ELECTRIC = "#3B82F6"
COLOR_ORANGE_BRIGHT = "#FF6B00"
COLOR_YELLOW_BRIGHT = "#FFD700"
COLOR_CYAN_LIGHT    = "#00E5FF"

plt.style.use('dark_background')
sns.set_theme(style="darkgrid", rc={
    "axes.facecolor": "#1e1e1e",
    "figure.facecolor": "#121212",
    "text.color": "#FFFFFF",
    "axes.labelcolor": "#FFFFFF",
    "xtick.color": "#FFFFFF",
    "ytick.color": "#FFFFFF",
    "grid.color": "#2A2A2A",
    "font.weight": "bold",
    "axes.labelweight": "bold",
    "axes.titleweight": "bold"
})

def style_bold_axis_dark(ax):
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('bold')
        label.set_color('#FFFFFF')
        label.set_fontsize(10)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['left'].set_color('#444444')
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_visible(True)
    ax.spines['bottom'].set_color('#444444')
    ax.spines['bottom'].set_linewidth(1.2)

STATE_NAMES = {
    'SP': 'São Paulo (SP)', 'RJ': 'Rio de Janeiro (RJ)', 'MG': 'Minas Gerais (MG)',
    'RS': 'Rio Grande do Sul (RS)', 'PR': 'Paraná (PR)', 'SC': 'Santa Catarina (SC)',
    'BA': 'Bahia (BA)', 'DF': 'Distrito Federal (DF)', 'ES': 'Espírito Santo (ES)',
    'GO': 'Goiás (GO)', 'PE': 'Pernambuco (PE)', 'CE': 'Ceará (CE)',
    'PA': 'Pará (PA)', 'MT': 'Mato Grosso (MT)', 'MA': 'Maranhão (MA)',
    'MS': 'Mato Grosso do Sul (MS)', 'PB': 'Paraíba (PB)', 'PI': 'Piauí (PI)',
    'RN': 'Rio Grande do Norte (RN)', 'AL': 'Alagoas (AL)', 'SE': 'Sergipe (SE)',
    'TO': 'Tocantins (TO)', 'RO': 'Rondônia (RO)', 'AM': 'Amazonas (AM)',
    'AC': 'Acre (AC)', 'AP': 'Amapá (AP)', 'RR': 'Roraima (RR)'
}

PAYMENT_LABEL_MAP = {
    'credit_card': 'Kartu Kredit',
    'boleto': 'Boleto',
    'voucher': 'Voucher',
    'debit_card': 'Kartu Debit'
}

def get_data_path(filename):
    if os.path.exists(os.path.join("data", filename)):
        return os.path.join("data", filename)
    elif os.path.exists(os.path.join("..", "data", filename)):
        return os.path.join("..", "data", filename)
    return filename

@st.cache_data
def load_data():
    orders_df = pd.read_csv(get_data_path("orders_dataset.csv"))
    customers_df = pd.read_csv(get_data_path("customers_dataset.csv"))
    order_items_df = pd.read_csv(get_data_path("order_items_dataset.csv"))
    order_reviews_df = pd.read_csv(get_data_path("order_reviews_dataset.csv"))
    products_df = pd.read_csv(get_data_path("products_dataset.csv"))
    payments_df = pd.read_csv(get_data_path("order_payments_dataset.csv"))

    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])
    orders_df['order_estimated_delivery_date'] = pd.to_datetime(orders_df['order_estimated_delivery_date'])

    customers_df['state_full'] = customers_df['customer_state'].map(lambda x: STATE_NAMES.get(x, x))

    return orders_df, customers_df, order_items_df, order_reviews_df, products_df, payments_df

orders_df, customers_df, order_items_df, order_reviews_df, products_df, payments_df = load_data()

with st.sidebar:
    col_img1, col_img2, col_img3 = st.columns([0.5, 5, 0.5])
    with col_img2:
        st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", use_container_width=True)

    st.markdown("<h2 style='text-align: center; color: #0f172a !important; margin-top: 5px; margin-bottom: 15px;'>🎯 Executive Menu</h2>", unsafe_allow_html=True)

    selected_view = st.radio(
        "📊 **Pilih Fokus Analisis:**",
        options=[
            "📌 Tampilkan Semua (Overview)",
            "🔥 Segmentasi Pelanggan (RFM)",
            "🛍️ Performa Kategori Produk",
            "💳 Metode Pembayaran Favorit",
            "📍 Performa Wilayah (State)",
            "🚚 Logistik & Rating Kepuasan"
        ]
    )

    st.markdown("---")
    st.markdown("### 🔍 **Filter Data**")

    min_date = orders_df['order_purchase_timestamp'].min().date()
    max_date = orders_df['order_purchase_timestamp'].max().date()

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        start_date = st.date_input('📅 Tanggal Mulai:', min_value=min_date, max_value=max_date, value=min_date)
    with col_d2:
        end_date = st.date_input('📅 Tanggal Akhir:', min_value=min_date, max_value=max_date, value=max_date)

    st.markdown("---")

    available_states = ["Semua State (All)"] + sorted(list(customers_df['state_full'].dropna().unique()))
    selected_state_option = st.selectbox("📍 Pilih Negara Bagian (State):", options=available_states, index=0)

main_orders_df = orders_df[
    (orders_df['order_purchase_timestamp'].dt.date >= start_date) &
    (orders_df['order_purchase_timestamp'].dt.date <= end_date)
]

if selected_state_option != "Semua State (All)":
    main_customers_df = customers_df[customers_df['state_full'] == selected_state_option]
else:
    main_customers_df = customers_df.copy()

valid_customer_ids = main_customers_df['customer_id']
main_orders_df = main_orders_df[main_orders_df['customer_id'].isin(valid_customer_ids)]

def create_rfm_df(df):
    recent_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    order_spending = order_items_df.groupby('order_id')['price'].sum().reset_index()
    orders_with_spending = pd.merge(df, order_spending, on='order_id', how='left')
    orders_with_spending = pd.merge(orders_with_spending, customers_df[['customer_id', 'customer_unique_id']], on='customer_id', how='left')

    rfm = orders_with_spending.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
        'order_id': 'count',
        'price': 'sum'
    }).reset_index()
    rfm.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']
    return rfm

def create_product_summary(df):
    items_merged = df.merge(order_items_df, on='order_id').merge(products_df, on='product_id')
    prod_sum = items_merged.groupby('product_category_name').agg({
        'order_id': 'count',
        'price': 'sum'
    }).reset_index().sort_values(by='order_id', ascending=False)
    return prod_sum

def create_payment_summary(df):
    pay_merged = df.merge(payments_df, on='order_id')
    pay_merged = pay_merged[pay_merged['payment_type'] != 'not_defined']

    pay_sum = pay_merged.groupby('payment_type').agg({
        'order_id': 'count',
        'payment_value': 'sum'
    }).reset_index().sort_values(by='order_id', ascending=False)

    pay_sum['payment_label'] = pay_sum['payment_type'].map(lambda x: PAYMENT_LABEL_MAP.get(x, x))
    return pay_sum

def create_state_summary(df):
    all_merged = df.merge(customers_df, on='customer_id').merge(order_items_df, on='order_id')
    state_sum = all_merged.groupby('state_full').agg({
        'customer_unique_id': 'nunique',
        'price': 'sum',
        'order_id': 'count'
    }).reset_index().sort_values(by='price', ascending=False)
    return state_sum

def create_review_delay(df):
    orders_rev = pd.merge(df, order_reviews_df, on='order_id', how='inner')
    orders_rev['delay_days'] = (orders_rev['order_delivered_customer_date'] - orders_rev['order_estimated_delivery_date']).dt.days
    orders_rev['delivery_status'] = orders_rev['delay_days'].apply(lambda x: 'Terlambat' if x > 0 else 'Tepat Waktu')
    rev_delay = orders_rev.groupby('delivery_status').agg({
        'review_score': ['mean', 'median', 'count']
    }).reset_index()
    return rev_delay

rfm_df = create_rfm_df(main_orders_df)
product_summary = create_product_summary(main_orders_df)
payment_summary = create_payment_summary(main_orders_df)
state_summary = create_state_summary(main_orders_df)
review_by_delay = create_review_delay(main_orders_df)

st.markdown("<h1 style='color: #FFFFFF !important; font-weight: 900;'>⚡ E-Commerce Executive Data Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #F3F4F6 !important; font-weight: 600;'>Visualisasi interaktif analisis bisnis e-commerce dengan tingkat presisi tinggi.</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📦 Total Pesanan", value=f"{len(main_orders_df):,}")
with col2:
    st.metric("👥 Pelanggan Unik", value=f"{rfm_df['customer_unique_id'].nunique():,}")
with col3:
    st.metric("💰 Total Pendapatan", value=f"BRL {rfm_df['monetary'].sum():,.2f}")

st.markdown("---")

if selected_view in ["📌 Tampilkan Semua (Overview)", "🔥 Segmentasi Pelanggan (RFM)"]:
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>🔥 Segmentasi Pelanggan (RFM Analysis)</h3>", unsafe_allow_html=True)
    fig_rfm, ax_rfm = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))
    fig_rfm.patch.set_facecolor('#121212')

    sns.histplot(rfm_df['recency'], bins=25, kde=True, ax=ax_rfm[0], color=COLOR_BLUE_ELECTRIC, edgecolor="white")
    ax_rfm[0].set_title('Distribusi Recency (Hari)', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_rfm[0].set_xlabel('Hari Sejak Transaksi Terakhir', fontweight='bold', color='#FFFFFF')
    ax_rfm[0].set_ylabel('Jumlah Pelanggan', fontweight='bold', color='#FFFFFF')

    sns.barplot(
        x=['Single Order', 'Repeat Order'],
        y=[(rfm_df['frequency'] == 1).sum(), (rfm_df['frequency'] > 1).sum()],
        ax=ax_rfm[1],
        palette=[COLOR_BLUE_ELECTRIC, COLOR_ORANGE_BRIGHT],
        edgecolor="white"
    )
    ax_rfm[1].set_title('Distribusi Frequency (Repeat Order)', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_rfm[1].set_ylabel('Jumlah Pelanggan', fontweight='bold', color='#FFFFFF')

    max_freq = max((rfm_df['frequency'] == 1).sum(), (rfm_df['frequency'] > 1).sum())
    ax_rfm[1].set_ylim(0, max_freq * 1.15)

    for p in ax_rfm[1].patches:
        ax_rfm[1].annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()),
                           ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', color='white', fontweight='bold', fontsize=11)

    sns.histplot(rfm_df[rfm_df['monetary'] > 0]['monetary'], bins=30, kde=True, ax=ax_rfm[2], color=COLOR_ORANGE_BRIGHT, edgecolor=COLOR_YELLOW_BRIGHT)
    ax_rfm[2].set_title('Distribusi Total Spending (Monetary)', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_rfm[2].set_xlabel('Pengeluaran / Transaksi (BRL)', fontweight='bold', color='#FFFFFF')
    ax_rfm[2].set_ylabel('Jumlah Pelanggan', fontweight='bold', color='#FFFFFF')
    ax_rfm[2].set_xlim(0, 1500)

    for ax in ax_rfm:
        style_bold_axis_dark(ax)

    plt.tight_layout()
    st.pyplot(fig_rfm)
    st.markdown("---")

if selected_view in ["📌 Tampilkan Semua (Overview)", "🛍️ Performa Kategori Produk"]:
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>🛍️ Top 5 Kategori Produk Terlaris</h3>", unsafe_allow_html=True)
    fig_prod, ax_prod = plt.subplots(figsize=(10, 4))
    fig_prod.patch.set_facecolor('#121212')
    sns.barplot(x='order_id', y='product_category_name', data=product_summary.head(5), palette='Oranges_r', ax=ax_prod, edgecolor="white")
    ax_prod.set_title('5 Kategori Produk dengan Jumlah Pesanan Tertinggi', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_prod.set_xlabel('Jumlah Item Terjual', fontweight='bold', color='#FFFFFF')
    ax_prod.set_ylabel('Kategori Produk', fontweight='bold', color='#FFFFFF')
    style_bold_axis_dark(ax_prod)
    st.pyplot(fig_prod)
    st.markdown("---")

if selected_view in ["📌 Tampilkan Semua (Overview)", "💳 Metode Pembayaran Favorit"]:
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>💳 Metode Pembayaran Paling Populer</h3>", unsafe_allow_html=True)
    fig_pay, ax_pay = plt.subplots(figsize=(10, 4))
    fig_pay.patch.set_facecolor('#121212')

    sns.barplot(
        x='payment_label',
        y='order_id',
        data=payment_summary,
        palette=[COLOR_BLUE_ELECTRIC, COLOR_ORANGE_BRIGHT, COLOR_YELLOW_BRIGHT, COLOR_CYAN_LIGHT],
        ax=ax_pay,
        edgecolor="white"
    )
    ax_pay.set_title('Distribusi Penggunaan Metode Pembayaran', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_pay.set_xlabel('Jenis Pembayaran', fontweight='bold', color='#FFFFFF')
    ax_pay.set_ylabel('Total Transaksi', fontweight='bold', color='#FFFFFF')

    if len(payment_summary) > 0:
        ax_pay.set_ylim(0, payment_summary['order_id'].max() * 1.15)

    style_bold_axis_dark(ax_pay)

    for p in ax_pay.patches:
        ax_pay.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', color='white', fontweight='bold', fontsize=11)

    plt.tight_layout()
    st.pyplot(fig_pay)
    st.markdown("---")

if selected_view == "📌 Tampilkan Semua (Overview)":
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>📍 Top 5 State Berdasarkan Pendapatan</h3>", unsafe_allow_html=True)
        fig_state, ax_state = plt.subplots(figsize=(7, 5))
        fig_state.patch.set_facecolor('#121212')
        sns.barplot(x='price', y='state_full', data=state_summary.head(5), palette='Blues_r', ax=ax_state, edgecolor="white")
        ax_state.set_title('Top 5 State (Total BRL)', fontsize=12, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=12)
        ax_state.set_xlabel('Total Pendapatan (BRL)', fontweight='bold', color='#FFFFFF')
        ax_state.set_ylabel('State', fontweight='bold', color='#FFFFFF')
        style_bold_axis_dark(ax_state)
        plt.tight_layout()
        st.pyplot(fig_state)

    with col_right:
        st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>🚚 Keterlambatan Pengiriman vs Review Score</h3>", unsafe_allow_html=True)
        fig_delay, ax_delay = plt.subplots(figsize=(7, 5))
        fig_delay.patch.set_facecolor('#121212')
        sns.barplot(x='delivery_status', y=('review_score', 'mean'), data=review_by_delay, palette=[COLOR_ORANGE_BRIGHT, COLOR_BLUE_ELECTRIC], ax=ax_delay, edgecolor="white")
        ax_delay.set_title('Rata-rata Rating Bintang (Review Score)', fontsize=12, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=12)
        ax_delay.set_xlabel('Status Pengiriman', fontweight='bold', color='#FFFFFF')
        ax_delay.set_ylabel('Rating (1-5)', fontweight='bold', color='#FFFFFF')
        ax_delay.set_ylim(0, 5.8)
        style_bold_axis_dark(ax_delay)
        for index, row in review_by_delay.iterrows():
            val = row[('review_score', 'mean')]
            ax_delay.text(index, val + 0.15, f"⭐ {val:.2f}", ha='center', color='white', fontweight='bold', fontsize=11)
        plt.tight_layout()
        st.pyplot(fig_delay)

elif selected_view == "📍 Performa Wilayah (State)":
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>📍 Performa Pendapatan Berdasarkan State</h3>", unsafe_allow_html=True)
    fig_state, ax_state = plt.subplots(figsize=(10, 5))
    fig_state.patch.set_facecolor('#121212')
    sns.barplot(x='price', y='state_full', data=state_summary.head(10), palette='Blues_r', ax=ax_state, edgecolor="white")
    ax_state.set_title('Top 10 State Berdasarkan Pendapatan (BRL)', fontsize=14, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_state.set_xlabel('Total Pendapatan (BRL)', fontweight='bold', color='#FFFFFF')
    ax_state.set_ylabel('State', fontweight='bold', color='#FFFFFF')
    style_bold_axis_dark(ax_state)
    st.pyplot(fig_state)

elif selected_view == "🚚 Logistik & Rating Kepuasan":
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>🚚 Pengaruh Delivery Delay terhadap Review Score</h3>", unsafe_allow_html=True)
    fig_delay, ax_delay = plt.subplots(figsize=(10, 5))
    fig_delay.patch.set_facecolor('#121212')
    sns.barplot(x='delivery_status', y=('review_score', 'mean'), data=review_by_delay, palette=[COLOR_ORANGE_BRIGHT, COLOR_BLUE_ELECTRIC], ax=ax_delay, edgecolor="white")
    ax_delay.set_title('Rata-rata Rating Bintang Kepuasan Pelanggan', fontsize=14, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_delay.set_xlabel('Status Pengiriman', fontweight='bold', color='#FFFFFF')
    ax_delay.set_ylabel('Rating (1-5)', fontweight='bold', color='#FFFFFF')
    ax_delay.set_ylim(0, 5.8)
    style_bold_axis_dark(ax_delay)
    for index, row in review_by_delay.iterrows():
        val = row[('review_score', 'mean')]
        ax_delay.text(index, val + 0.15, f"⭐ {val:.2f}", ha='center', color='white', fontweight='bold', fontsize=12)
    st.pyplot(fig_delay)

st.caption("✨ Developed for Dicoding (Submission Proyek Analisis Data) — Luthfia Ramadhani")
