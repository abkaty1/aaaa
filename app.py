import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الواجهة الرسمية والألوان الذكية
st.set_page_config(page_title="منصة التحليل الإحصائي المرنة", page_icon="📊", layout="wide")

# تصميم بطاقات المؤشرات الرقمية بصرياً
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stat-card {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-right: 6px solid #2563EB;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .stat-title { color: #475569; font-size: 15px; font-weight: bold; }
    .stat-val { color: #1E3A8A; font-size: 28px; font-weight: bold; padding-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# العناوين الرئيسية
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📊 منصة الفرز الذكي وتحليل الحقول المتعددة</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 18px;'>قم باختيار وتحديد أي حقول ترغب بالفرز والتصفية بناءً عليها ديناميكياً</p>", unsafe_allow_html=True)
st.markdown("---")

# رفع ملف البيانات من الشريط الجانبي
st.sidebar.markdown("<h2 style='color: #2563EB;'>📂 تحميل الملف</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("قم برفع ملف البيانات (Excel / CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # قراءة البيانات بشكل مرن
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # تنظيف وتجهيز أسماء الأعمدة
    df.columns = df.columns.str.strip()
    all_columns = df.columns.tolist()
    
    # 2. محرك التصفية الديناميكي متعدد الخيارات
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h2 style='color: #2563EB;'>🔍 فلاتر مخصصة</h2>", unsafe_allow_html=True)
    
    # خيار تحديد أسماء الحقول المراد الفرز بناءً عليها
    selected_filter_columns = st.sidebar.multiselect(
        "اختر الحقول التي ترغب في الفرز بها (يمكنك اختيار أكثر من حقل):",
        options=all_columns,
        help="اختر أي اسم عمود من ملفك ليظهر لك فلتر خاص به فوراً"
    )
    
    # تطبيق الفلاتر المختارة بالتتابع على البيانات
    filtered_df = df.copy()
    
    if selected_filter_columns:
        for col in selected_filter_columns:
            # جلب القيم الفريدة وغير الفارغة للعمود المحدد
            unique_values = df[col].dropna().unique().tolist()
            # إنشاء صندوق تصفية متعدد الخيارات لكل عمود يتم اختياره
            selected_values = st.sidebar.multiselect(
                f"🎯 تصفية حسب ({col}):", 
                options=unique_values, 
                default=unique_values
            )
            # تحديث البيانات بناءً على القيم المحددة
            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]
    else:
        st.sidebar.info("💡 يمكنك اختيار حقل أو أكثر من القائمة أعلاه لبدء الفرز المتقدم.")

    # 3. عرض المؤشرات العامة المتغيرة مع الفرز
    st.markdown("### 📈 الخلاصة الإحصائية العامة للبيانات")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"<div class='stat-card' style='border-right-color: #2563EB;'><div class='stat-title'>📊 إجمالي السجلات بعد التصفية</div><div class='stat-val'>{len(filtered_df)} <span style='font-size:14px; color:#64748B;'>من {len(df)}</span></div></div>", unsafe_allow_html=True)
    with c2:
        num_fields = len(selected_filter_columns)
        st.markdown(f"<div class='stat-card' style='border-right-color: #10B981;'><div class='stat-title'>🛠️ عدد حقول الفرز النشطة</div><div class='stat-val'>{num_fields}</div></div>", unsafe_allow_html=True)
    with c3:
        total_cols = len(all_columns)
        st.markdown(f"<div class='stat-card' style='border-right-color: #F59E0B;'><div class='stat-title'>🗂️ إجمالي أعمدة الملف المتوفرة</div><div class='stat-val'>{total_cols}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # 4. استعراض الأعداد التفصيلية والرسوم البيانية بناءً على الحقول النشطة
    st.markdown("### 🏢 توزيع الأعداد والنسب المئوية للحقول المختارة")
    
    if selected_filter_columns:
        # إنشاء ألسنة تفاعلية ديناميكياً لكل حقل اختاره المستخدم للفرز
        tabs = st.tabs([f"📊 {col}" for col in selected_filter_columns])
        
        for tab, col_name in zip(tabs, selected_filter_columns):
            with tab:
                st.markdown(f"**📈 تحليل توزيبي شامل لحقل: `{col_name}`**")
                
                # حساب التكرارات والنسب المئوية
                count_data = filtered_df[col_name].value_counts().reset_index()
                count_data.columns = [col_name, 'العدد (Count)']
                count_data['النسبة المئوية (%)'] = ((count_data['العدد (Count)'] / len(filtered_df)) * 100).round(1)
                
                # عرض البيانات والرسوم بجانب بعضهما
                col_table, col_chart = st.columns([2, 3])
                with col_table:
                    st.dataframe(count_data, use_container_width=True, hide_index=True)
                with col_chart:
                    fig = px.bar(
                        count_data, 
                        x=col_name, 
                        y='العدد (Count)', 
                        text='العدد (Count)', 
                        color=col_name, 
                        color_discrete_sequence=px.colors.qualitative.Safe
                    )
                    fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ يرجى تحديد حقل واحد على الأقل من القائمة الجانبية لعرض جداول الأعداد والرسوم البيانية الخاصة به.")

    st.markdown("---")
    
    # 5. عرض الجدول النهائي المفرز بالكامل
    with st.expander("👀 استعراض قاعدة البيانات الكاملة والمحدثة وفقاً للفرز والتصفية"):
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("💡 في انتظار رفع ملف البيانات (Excel / CSV) من الشريط الجانبي للبدء في الفرز الديناميكي...")
