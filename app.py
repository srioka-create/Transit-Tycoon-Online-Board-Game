import streamlit as st
import pandas as pd
import math

# Konfigurasi Halaman Web App
st.set_page_config(
    page_title="Transit Tycoon: City Operator Challenge",
    page_icon="🚌",
    layout="wide"
)

st.title("🚌 Transit Tycoon: City Operator Challenge")
st.caption("Game Simulasi & Game-based Learning Perencanaan Operasional Transportasi Umum")

# Inisialisasi Session State (Status Permainan)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'completed_levels' not in st.session_state:
    st.session_state.completed_levels = []

# Sidebar Informasi Tim & Skor
st.sidebar.header("🏆 Dashboard Tim Operator")
team_name = st.sidebar.text_input("Nama Tim / PT Operator:", "PT Transport Jaya")
st.sidebar.metric(label="Total Poin Kinerja (PK)", value=f"{st.session_state.score} PK")

st.sidebar.markdown("---")
st.sidebar.subheader("📍 Progress Board")
levels = ["Level 1: Load Factor", "Level 2: Rush Hour Headway", "Level 3: Final Boss - BRT Tender"]
for lvl in levels:
    status = "✅ Selesai" if lvl in st.session_state.completed_levels else "⏳ Belum"
    st.sidebar.write(f"**{lvl}:** {status}")

# Tampilan Utama Game
tab1, tab2, tab3 = st.tabs(["🟢 Level 1: Load Factor", "🟡 Level 2: Rush Hour Headway", "🔴 Level 3: Tender BRT Koridor 1"])

# ==========================================
# LEVEL 1
# ==========================================
with tab1:
    st.header("Level 1: The Load Factor Puzzle 🧩")
    st.write("""
    **Skenario:** Tim Anda dipercaya mengelola Rute Bus Kota A. 
    Kapasitas bus yang beroperasi adalah **50 penumpang** (20 duduk, 30 berdiri).
    Berdasarkan survei, tercatat total **1.850 penumpang.km** dan total armada beroperasi menghasilkan **2.000 bus.km**.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        ans_lf = st.number_input("Hitung Load Factor (%) rute tersebut:", min_value=0.0, max_value=200.0, step=0.1, key="l1")
        submit_l1 = st.button("Kirim Jawaban Level 1")
        
    if submit_l1:
        # Rumus LF = (Pnp.km / (Bus.km * Kapasitas)) * 100% ATAU versi sederhana dari data input
        # Berdasarkan formula: LF = (1850 / (2000 * (50/50))) = 92.5%
        # Dalam soal sederhana: 1850 / 2000 * 100% = 92.5%
        correct_lf = 92.5
        if math.isclose(ans_lf, correct_lf, abs_tol=0.5):
            st.success("🎉 JAWABAN BENAR! Load Factor = 92.5% (> 70%, Rute Sangat Layak & Efisien).")
            if "Level 1: Load Factor" not in st.session_state.completed_levels:
                st.session_state.score += 100
                st.session_state.completed_levels.append("Level 1: Load Factor")
                st.rerun()
        else:
            st.error("❌ Jawaban belum tepat. Gunakan rumus: LF = (∑Pnp.km / ∑Bus.km) x 100%")

# ==========================================
# LEVEL 2
# ==========================================
with tab2:
    st.header("Level 2: Rush Hour Headway ⏱️")
    st.write("""
    **Skenario:** Jam sibuk pagi (06.30 - 07.30) mencatat lonjakan **180 penumpang/jam** pada seksi tersibuk.
    Kapasitas per armada bus adalah **40 penumpang** dengan target rerata *Load Factor* sebesar **75%**.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        ans_headway = st.number_input("Hitung Headway ideal (dalam Menit):", min_value=0.0, max_value=60.0, step=0.1, key="l2")
        submit_l2 = st.button("Kirim Jawaban Level 2")
        
    if submit_l2:
        # Rumus: H = (60 * LF * K) / P = (60 * 0.75 * 40) / 180 = 10 menit
        correct_h = 10.0
        if math.isclose(ans_headway, correct_h, abs_tol=0.1):
            st.success("🎉 JAWABAN BENAR! Headway ideal = 10 Menit sekali antarbus.")
            if "Level 2: Rush Hour Headway" not in st.session_state.completed_levels:
                st.session_state.score += 150
                st.session_state.completed_levels.append("Level 2: Rush Hour Headway")
                st.rerun()
        else:
            st.error("❌ Jawaban belum tepat. Rumus: H = (60 x LF x K) / P")

# ==========================================
# LEVEL 3 (FINAL BOSS)
# ==========================================
with tab3:
    st.header("Level 3: Megatender BRT Koridor 1 🏆")
    st.markdown("""
    **Parameter Tender Kota X:**
    - Operasional: **06.00 - 21.00 WIB**
    - Penumpang Sesi Sibuk ($P$): **2.600 pnp/jam** (2.100 bus + 500 angkot)
    - Kapasitas Bus ($K$): **240 pnp** | Target $LF$: **90%**
    - Waktu Perjalanan PP ($T_{AB} + T_{BA}$): **120 menit**
    - Total Waktu Henti (12 Halte): **24 menit** 
    - Faktor Ketersediaan Armada ($f_A$): **1.0**
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        ans_ct = st.number_input("Waktu Sirkulasi CT (Menit):", min_value=0, key="ct")
    with col2:
        ans_h3 = st.number_input("Headway H (Menit):", min_value=0, key="h3")
    with col3:
        ans_ja = st.number_input("Jumlah Armada JA (Unit):", min_value=0, key="ja")
        
    submit_l3 = st.button("Submit Proposal Tender BRT")
    
    if submit_l3:
        # CT = 120 + 24 = 144 menit
        # H = (60 * 0.9 * 240) / 2600 = 4.98 -> dibulatkan 5 menit
        # JA = 144 / (5 * 1.0) = 28.8 -> dibulatkan 29 unit
        if ans_ct == 144 and ans_h3 == 5 and ans_ja == 29:
            st.balloons()
            st.success("🏆 CONGRATULATIONS! Proposal Anda memenangkan Tender BRT Koridor 1 Kota X!")
            if "Level 3: Final Boss - BRT Tender" not in st.session_state.completed_levels:
                st.session_state.score += 300
                st.session_state.completed_levels.append("Level 3: Final Boss - BRT Tender")
                st.rerun()
        else:
            st.error("❌ Proposal ditolak! Periksa kembali nilai CT (144), Headway (5), atau Pembulatan Armada (29).")

    # Fitur Preview Timetable
    if "Level 3: Final Boss - BRT Tender" in st.session_state.completed_levels:
        st.markdown("---")
        st.subheader("📅 Master Timetable (Hasil Output Perhitungan)")
        
        # Generator Timetable Otomatis
        start_time = pd.to_datetime("06:00", format="%H:%M")
        data = []
        for i in range(1, 30):
            dep_a = start_time + pd.Timedelta(minutes=(i-1)*5)
            arr_b = dep_a + pd.Timedelta(minutes=72)
            dep_b = arr_b
            arr_a = dep_b + pd.Timedelta(minutes=72)
            data.append({
                "No. Bus": f"Bus {i}",
                "Berangkat Terminal A": dep_a.strftime("%H:%M"),
                "Tiba Terminal B": arr_b.strftime("%H:%M"),
                "Berangkat Terminal B": dep_b.strftime("%H:%M"),
                "Tiba Terminal A (Selesai Rit 1)": arr_a.strftime("%H:%M")
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True)
