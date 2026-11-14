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
COLOR_GREEN_BRIGHT  = "#22C55E"
COLOR_RED_BRIGHT    = "#EF4444"

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

    # Pembersihan tipe data tanggal dan duplikat ulasan sesuai notebook
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])
    orders_df['order_estimated_delivery_date'] = pd.to_datetime(orders_df['order_estimated_delivery_date'])
    order_reviews_df = order_reviews_df.drop_duplicates(subset='review_id')

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

    available_states = ["Semua Negara Bagian (All)"] + sorted(list(customers_df['state_full'].dropna().unique()))
    selected_state_option = st.selectbox("📍 Pilih Negara Bagian (State):", options=available_states, index=0)

main_orders_df = orders_df[
    (orders_df['order_purchase_timestamp'].dt.date >= start_date) &
    (orders_df['order_purchase_timestamp'].dt.date <= end_date)
]

if selected_state_option != "Semua Negara Bagian (All)":
    main_customers_df = customers_df[customers_df['state_full'] == selected_state_option]
else:
    main_customers_df = customers_df.copy()

valid_customer_ids = main_customers_df['customer_id']
main_orders_df = main_orders_df[main_orders_df['customer_id'].isin(valid_customer_ids)]

# Fungsi perhitungan yang 100% konsisten dengan notebook
def create_rfm_df(df):
    valid_orders = df[~df['order_status'].isin(['canceled', 'unavailable'])].copy()
    if valid_orders.empty:
        return pd.DataFrame(columns=['customer_unique_id', 'recency', 'frequency', 'monetary', 'customer_segment'])

    recent_date = valid_orders['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    order_spending = payments_df.groupby('order_id')['payment_value'].sum().reset_index()

    orders_with_spending = pd.merge(valid_orders, order_spending, on='order_id', how='left')
    orders_with_spending['payment_value'] = orders_with_spending['payment_value'].fillna(0)
    orders_with_spending = pd.merge(
        orders_with_spending,
        customers_df[['customer_id', 'customer_unique_id']],
        on='customer_id',
        how='left'
    )

    rfm = orders_with_spending.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
        'order_id': 'nunique',
        'payment_value': 'sum'
    }).reset_index()
    rfm.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']

    # Segmentasi RFM berbasis aturan frekuensi aktual (selaras dengan notebook)
    if len(rfm) >= 4:
        rfm['r_score'] = pd.qcut(rfm['recency'].rank(method='first'), q=4, labels=[4, 3, 2, 1]).astype(int)
        rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=4, labels=[1, 2, 3, 4]).astype(int)
    else:
        rfm['r_score'] = 2
        rfm['m_score'] = 2

    def score_frequency(freq):
        if freq == 1:
            return 1
        elif freq == 2:
            return 2
        elif freq == 3:
            return 3
        return 4

    rfm['f_score'] = rfm['frequency'].apply(score_frequency)
    rfm['rfm_score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']

    def segment_customer(row):
        if row['rfm_score'] >= 9 and row['frequency'] >= 2:
            return 'Champions'
        elif row['rfm_score'] >= 8:
            return 'Loyal Customers'
        elif row['rfm_score'] >= 6:
            return 'Potential Loyalist'
        return 'At Risk / Hibernating'

    rfm['customer_segment'] = rfm.apply(segment_customer, axis=1)
    return rfm

def create_product_summary(df):
    valid_orders = df[~df['order_status'].isin(['canceled', 'unavailable'])]
    items_merged = valid_orders.merge(order_items_df, on='order_id').merge(products_df, on='product_id')
    items_merged = items_merged.dropna(subset=['product_category_name'])
    prod_sum = items_merged.groupby('product_category_name').agg({
        'order_id': 'count',
        'price': 'sum'
    }).reset_index()
    prod_sum.columns = ['product_category_name', 'total_sold', 'total_revenue']
    return prod_sum

def create_payment_summary(df):
    pay_merged = df.merge(payments_df, on='order_id')
    pay_merged = pay_merged[pay_merged['payment_type'] != 'not_defined']

    pay_sum = pay_merged.groupby('payment_type').agg({
        'order_id': 'nunique',
        'payment_value': 'sum'
    }).reset_index().sort_values(by='order_id', ascending=False)

    pay_sum['payment_label'] = pay_sum['payment_type'].map(lambda x: PAYMENT_LABEL_MAP.get(x, x))
    return pay_sum

def create_state_summary(df):
    # Konsisten dengan EDA dan Pertanyaan 4 di notebook (berbasis payment_value seluruh pesanan)
    all_merged = df.merge(customers_df, on='customer_id').merge(payments_df, on='order_id')
    state_sum = all_merged.groupby('state_full').agg({
        'customer_unique_id': 'nunique',
        'payment_value': 'sum',
        'order_id': 'nunique'
    }).reset_index().sort_values(by='payment_value', ascending=False)
    return state_sum

def create_review_delay(df):
    # Konsisten dengan EDA dan Pertanyaan 5 di notebook (pesanan sudah tiba & stempel waktu penuh)
    delivered_orders = df[df['order_delivered_customer_date'].notna()].copy()
    orders_rev = pd.merge(delivered_orders, order_reviews_df, on='order_id', how='inner')
    orders_rev['delivery_status'] = orders_rev.apply(
        lambda row: 'Terlambat' if row['order_delivered_customer_date'] > row['order_estimated_delivery_date'] else 'Tepat Waktu',
        axis=1
    )
    rev_delay = orders_rev.groupby('delivery_status').agg(
        avg_score=('review_score', 'mean'),
        median_score=('review_score', 'median'),
        total_reviews=('review_id', 'count')
    ).reset_index().sort_values(by='avg_score', ascending=False)
    return rev_delay

rfm_df = create_rfm_df(main_orders_df)
product_summary = create_product_summary(main_orders_df)
payment_summary = create_payment_summary(main_orders_df)
state_summary = create_state_summary(main_orders_df)
review_by_delay = create_review_delay(main_orders_df)

# Total pendapatan keseluruhan konsisten dengan state_summary (seluruh transaksi pembayaran)
total_revenue_all = state_summary['payment_value'].sum()

st.markdown("<h1 style='color: #FFFFFF !important; font-weight: 900;'>⚡ E-Commerce Executive Data Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #F3F4F6 !important; font-weight: 600;'>Visualisasi interaktif analisis bisnis e-commerce Olist (Brasil) periode September 2016 – Oktober 2018.</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📦 Total Pesanan", value=f"{len(main_orders_df):,}")
with col2:
    st.metric("👥 Pelanggan Unik", value=f"{rfm_df['customer_unique_id'].nunique():,}")
with col3:
    st.metric("💰 Total Pendapatan", value=f"BRL {total_revenue_all:,.2f}")

st.markdown("---")

if selected_view in ["📌 Tampilkan Semua (Overview)", "🔥 Segmentasi Pelanggan (RFM)"]:
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>🔥 Analisis Perilaku & Segmentasi Pelanggan (RFM Analysis)</h3>", unsafe_allow_html=True)
    fig_rfm, ax_rfm = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))
    fig_rfm.patch.set_facecolor('#121212')

    sns.histplot(rfm_df['recency'], bins=25, kde=True, ax=ax_rfm[0], color=COLOR_BLUE_ELECTRIC, edgecolor="white")
    ax_rfm[0].set_title('Distribusi Recency (Hari)', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_rfm[0].set_xlabel('Hari Sejak Transaksi Terakhir', fontweight='bold', color='#FFFFFF')
    ax_rfm[0].set_ylabel('Jumlah Pelanggan', fontweight='bold', color='#FFFFFF')

    freq_labels = ['Single Order', 'Repeat Order']
    freq_values = [(rfm_df['frequency'] == 1).sum(), (rfm_df['frequency'] > 1).sum()]
    sns.barplot(
        x=freq_labels,
        y=freq_values,
        hue=freq_labels,
        ax=ax_rfm[1],
        palette=[COLOR_BLUE_ELECTRIC, COLOR_ORANGE_BRIGHT],
        legend=False,
        edgecolor="white"
    )
    ax_rfm[1].set_title('Distribusi Frequency (Repeat Order)', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_rfm[1].set_ylabel('Jumlah Pelanggan', fontweight='bold', color='#FFFFFF')

    max_freq = max(freq_values) if freq_values else 1
    ax_rfm[1].set_ylim(0, max_freq * 1.15)

    for p in ax_rfm[1].patches:
        ax_rfm[1].annotate(
            f'{int(p.get_height()):,}',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', color='white', fontweight='bold', fontsize=11
        )

    sns.histplot(rfm_df[rfm_df['monetary'] > 0]['monetary'], bins=30, kde=True, ax=ax_rfm[2], color=COLOR_ORANGE_BRIGHT, edgecolor=COLOR_YELLOW_BRIGHT)
    ax_rfm[2].set_title('Distribusi Total Belanja (Monetary)', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_rfm[2].set_xlabel('Pengeluaran / Pelanggan (BRL)', fontweight='bold', color='#FFFFFF')
    ax_rfm[2].set_ylabel('Jumlah Pelanggan', fontweight='bold', color='#FFFFFF')
    ax_rfm[2].set_xlim(0, 1500)

    for ax in ax_rfm:
        style_bold_axis_dark(ax)

    plt.tight_layout()
    st.pyplot(fig_rfm)

    # Grafik Segmentasi Pelanggan RFM (Analisis Lanjutan)
    if not rfm_df.empty:
        seg_order = ['Potential Loyalist', 'At Risk / Hibernating', 'Loyal Customers', 'Champions']
        seg_counts = rfm_df['customer_segment'].value_counts().reindex(seg_order).fillna(0).reset_index()
        seg_counts.columns = ['customer_segment', 'total_customers']
        seg_counts['percentage'] = (seg_counts['total_customers'] / len(rfm_df)) * 100

        fig_seg, ax_seg = plt.subplots(figsize=(14, 4))
        fig_seg.patch.set_facecolor('#121212')
        sns.barplot(
            data=seg_counts,
            x='total_customers',
            y='customer_segment',
            hue='customer_segment',
            palette=[COLOR_BLUE_ELECTRIC, COLOR_RED_BRIGHT, COLOR_CYAN_LIGHT, COLOR_GREEN_BRIGHT],
            legend=False,
            ax=ax_seg,
            edgecolor="white"
        )
        ax_seg.set_title('Distribusi Segmentasi Pelanggan Berdasarkan Skor RFM', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
        ax_seg.set_xlabel('Jumlah Pelanggan Unik', fontweight='bold', color='#FFFFFF')
        ax_seg.set_ylabel('Segmen Pelanggan', fontweight='bold', color='#FFFFFF')
        ax_seg.set_xlim(0, seg_counts['total_customers'].max() * 1.18)

        for p, pct in zip(ax_seg.patches, seg_counts['percentage']):
            ax_seg.annotate(
                f" {int(p.get_width()):,} ({pct:.2f}%)",
                (p.get_width(), p.get_y() + p.get_height() / 2.),
                ha='left', va='center', color='white', fontweight='bold', fontsize=10
            )

        style_bold_axis_dark(ax_seg)
        plt.tight_layout()
        st.pyplot(fig_seg)

    st.markdown("---")

if selected_view in ["📌 Tampilkan Semua (Overview)", "🛍️ Performa Kategori Produk"]:
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>🛍️ Top 5 Kategori Produk Berdasarkan Volume dan Pendapatan</h3>", unsafe_allow_html=True)
    top_vol = product_summary.sort_values(by='total_sold', ascending=False).head(5)
    top_rev = product_summary.sort_values(by='total_revenue', ascending=False).head(5)

    fig_prod, ax_prod = plt.subplots(nrows=1, ncols=2, figsize=(18, 4.5))
    fig_prod.patch.set_facecolor('#121212')

    sns.barplot(
        x='total_sold', y='product_category_name', data=top_vol,
        hue='product_category_name', palette='Oranges_r', legend=False, ax=ax_prod[0], edgecolor="white"
    )
    ax_prod[0].set_title('Top 5 Kategori Produk Berdasarkan Jumlah Terjual', fontsize=12, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_prod[0].set_xlabel('Jumlah Item Terjual', fontweight='bold', color='#FFFFFF')
    ax_prod[0].set_ylabel('Kategori Produk', fontweight='bold', color='#FFFFFF')

    sns.barplot(
        x='total_revenue', y='product_category_name', data=top_rev,
        hue='product_category_name', palette='Blues_r', legend=False, ax=ax_prod[1], edgecolor="white"
    )
    ax_prod[1].set_title('Top 5 Kategori Produk Berdasarkan Total Pendapatan (BRL)', fontsize=12, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_prod[1].set_xlabel('Total Pendapatan (BRL)', fontweight='bold', color='#FFFFFF')
    ax_prod[1].set_ylabel('')

    for ax in ax_prod:
        style_bold_axis_dark(ax)

    plt.tight_layout()
    st.pyplot(fig_prod)
    st.markdown("---")

if selected_view in ["📌 Tampilkan Semua (Overview)", "💳 Metode Pembayaran Favorit"]:
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>💳 Metode Pembayaran Paling Populer (Berdasarkan Pesanan Unik)</h3>", unsafe_allow_html=True)
    fig_pay, ax_pay = plt.subplots(figsize=(10, 4))
    fig_pay.patch.set_facecolor('#121212')

    sns.barplot(
        x='payment_label',
        y='order_id',
        data=payment_summary,
        hue='payment_label',
        palette=[COLOR_BLUE_ELECTRIC, COLOR_ORANGE_BRIGHT, COLOR_YELLOW_BRIGHT, COLOR_CYAN_LIGHT][:len(payment_summary)],
        legend=False,
        ax=ax_pay,
        edgecolor="white"
    )
    ax_pay.set_title('Distribusi Penggunaan Metode Pembayaran', fontsize=13, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_pay.set_xlabel('Jenis Pembayaran', fontweight='bold', color='#FFFFFF')
    ax_pay.set_ylabel('Jumlah Pesanan Unik', fontweight='bold', color='#FFFFFF')

    if len(payment_summary) > 0:
        ax_pay.set_ylim(0, payment_summary['order_id'].max() * 1.15)

    style_bold_axis_dark(ax_pay)

    for p in ax_pay.patches:
        ax_pay.annotate(
            f'{int(p.get_height()):,}',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', color='white', fontweight='bold', fontsize=11
        )

    plt.tight_layout()
    st.pyplot(fig_pay)
    st.markdown("---")

if selected_view == "📌 Tampilkan Semua (Overview)":
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>📍 Top 5 Negara Bagian Berdasarkan Pendapatan</h3>", unsafe_allow_html=True)
        fig_state, ax_state = plt.subplots(figsize=(7, 5))
        fig_state.patch.set_facecolor('#121212')
        top5_state = state_summary.head(5)
        sns.barplot(
            x='payment_value', y='state_full', data=top5_state,
            hue='state_full', palette='Blues_r', legend=False, ax=ax_state, edgecolor="white"
        )
        ax_state.set_title('Top 5 Negara Bagian (Total Pendapatan BRL)', fontsize=12, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=12)
        ax_state.set_xlabel('Total Pendapatan (BRL)', fontweight='bold', color='#FFFFFF')
        ax_state.set_ylabel('Negara Bagian', fontweight='bold', color='#FFFFFF')
        style_bold_axis_dark(ax_state)
        plt.tight_layout()
        st.pyplot(fig_state)

    with col_right:
        st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>🚚 Ketepatan Pengiriman Dibandingkan Skor Ulasan</h3>", unsafe_allow_html=True)
        fig_delay, ax_delay = plt.subplots(figsize=(7, 5))
        fig_delay.patch.set_facecolor('#121212')
        palette_delay = {'Tepat Waktu': COLOR_GREEN_BRIGHT, 'Terlambat': COLOR_RED_BRIGHT}
        sns.barplot(
            x='delivery_status', y='avg_score', data=review_by_delay,
            hue='delivery_status', palette=palette_delay, legend=False, ax=ax_delay, edgecolor="white"
        )
        ax_delay.set_title('Rata-Rata Skor Ulasan Pelanggan (Skala 1 - 5)', fontsize=12, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=12)
        ax_delay.set_xlabel('Status Ketepatan Pengiriman', fontweight='bold', color='#FFFFFF')
        ax_delay.set_ylabel('Rata-Rata Skor Ulasan', fontweight='bold', color='#FFFFFF')
        ax_delay.set_ylim(0, 5.5)
        style_bold_axis_dark(ax_delay)
        for p in ax_delay.patches:
            val = p.get_height()
            ax_delay.annotate(
                f"⭐ {val:.2f}",
                (p.get_x() + p.get_width() / 2., val),
                ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', color='white', fontweight='bold', fontsize=11
            )
        plt.tight_layout()
        st.pyplot(fig_delay)

elif selected_view == "📍 Performa Wilayah (State)":
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>📍 Performa Pendapatan Berdasarkan Negara Bagian di Brasil</h3>", unsafe_allow_html=True)
    fig_state, ax_state = plt.subplots(figsize=(10, 5))
    fig_state.patch.set_facecolor('#121212')
    top10_state = state_summary.head(10)
    sns.barplot(
        x='payment_value', y='state_full', data=top10_state,
        hue='state_full', palette='Blues_r', legend=False, ax=ax_state, edgecolor="white"
    )
    ax_state.set_title('Top 10 Negara Bagian Berdasarkan Total Pendapatan (BRL)', fontsize=14, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_state.set_xlabel('Total Pendapatan (BRL)', fontweight='bold', color='#FFFFFF')
    ax_state.set_ylabel('Negara Bagian', fontweight='bold', color='#FFFFFF')
    style_bold_axis_dark(ax_state)
    plt.tight_layout()
    st.pyplot(fig_state)

elif selected_view == "🚚 Logistik & Rating Kepuasan":
    st.markdown("<h3 style='color: #FFD700 !important; font-weight: 800;'>🚚 Pengaruh Ketepatan Pengiriman terhadap Skor Ulasan Pelanggan</h3>", unsafe_allow_html=True)
    fig_delay, ax_delay = plt.subplots(figsize=(10, 5))
    fig_delay.patch.set_facecolor('#121212')
    palette_delay = {'Tepat Waktu': COLOR_GREEN_BRIGHT, 'Terlambat': COLOR_RED_BRIGHT}
    sns.barplot(
        x='delivery_status', y='avg_score', data=review_by_delay,
        hue='delivery_status', palette=palette_delay, legend=False, ax=ax_delay, edgecolor="white"
    )
    ax_delay.set_title('Rata-Rata Skor Ulasan Berdasarkan Ketepatan Pengiriman', fontsize=14, fontweight='bold', color=COLOR_YELLOW_BRIGHT, pad=10)
    ax_delay.set_xlabel('Status Ketepatan Pengiriman', fontweight='bold', color='#FFFFFF')
    ax_delay.set_ylabel('Rata-Rata Skor Ulasan (Skala 1 - 5)', fontweight='bold', color='#FFFFFF')
    ax_delay.set_ylim(0, 5.5)
    style_bold_axis_dark(ax_delay)
    for p in ax_delay.patches:
        val = p.get_height()
        ax_delay.annotate(
            f"⭐ {val:.2f}",
            (p.get_x() + p.get_width() / 2., val),
            ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', color='white', fontweight='bold', fontsize=12
        )
    plt.tight_layout()
    st.pyplot(fig_delay)

st.caption("✨ Developed for Dicoding (Submission Proyek Analisis Data) — Luthfia Ramadhani")