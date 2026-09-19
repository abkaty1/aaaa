import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الواجهة الرسمية الملونة والعصرية
st.set_page_config(page_title="منصة التحليل الإحصائي التعليمي", page_icon="📊", layout="wide")

# تخصيص مظهر بطاقات العرض الرقمية (CSS مخصص)
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stat-card {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-right: 6px solid #1E3A8A;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .stat-title { color: #475569; font-size: 15px; font-weight: bold; }
    .stat-val { color: #1E3A8A; font-size: 26px; font-weight: bold; padding-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# العناوين الرئيسية للمنصة
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📊 لوحة التحكم والإحصائيات التعليمية المتقدمة</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 18px;'>منظومة الفرز والتحليل المتقدمة بناءً على التصنيفات المحددة</p>", unsafe_allow_html=True)
st.markdown("---")

# رفع ملف البيانات من الشريط الجانبي
st.sidebar.markdown("<h2 style='color: #1E3A8A;'>📂 تحميل الملف</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("قم برفع ملف البيانات (Excel / CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # قراءة البيانات تلقائياً
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # تنظيف مسميات الحقول من المسافات الزائدة
    df.columns = df.columns.str.strip()
    all_cols = df.columns.tolist()
    
    # محرك البحث الذكي لربط الأعمدة بالفلاتر بناءً على الكلمات الدلالية
    col_edu_type = next((c for c in all_cols if any(k in c for k in ['نوع التعليم', 'التعليم', 'نوع تعليم'])), None)
    col_office   = next((c for c in all_cols if any(k in c for k in ['مكتب', 'المكتب'])), None)
    col_unit     = next((c for c in all_cols if any(k in c for k in ['وحدة', 'الوحدة'])), None)
    col_dept     = next((c for c in all_cols if any(k in c for k in ['قسم', 'القسم'])), None)
    col_stage    = next((c for c in all_cols if any(k in c for k in ['المرحلة', 'مرحلة', 'المرحله', 'مرحله'])), None)
    col_gender   = next((c for c in all_cols if any(k in c for k in ['الجنس', 'جنس', 'النوع', 'نوع'])), None)
    
    # 2. قسم الفلاتر المتخصصة في الشريط الجانبي
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h2 style='color: #1E3A8A;'>🔍 فلاتر التصفية المتخصصة</h2>", unsafe_allow_html=True)
    
    filtered_df = df.copy()
    
    # فلتر 1: نوع التعليم
    if col_edu_type:
        unique_edu = df[col_edu_type].dropna().unique().tolist()
        selected_edu = st.sidebar.multiselect(f"🎓 نوع التعليم:", unique_edu, default=unique_edu)
        filtered_df = filtered_df[filtered_df[col_edu_type].isin(selected_edu)]
        
    # فلتر 2: المكتب
    if col_office:
        unique_offices = df[col_office].dropna().unique().tolist()
        selected_offices = st.sidebar.multiselect(f"🏢 المكتب:", unique_offices, default=unique_offices)
        filtered_df = filtered_df[filtered_df[col_office].isin(selected_offices)]
        
    # فلتر 3: الوحدة
    if col_unit:
        unique_units = df[col_unit].dropna().unique().tolist()
        selected_units = st.sidebar.multiselect(f"⚙️ الوحدة:", unique_units, default=unique_units)
        filtered_df = filtered_df[filtered_df[col_unit].isin(selected_units)]
        
    # فلتر 4: القسم
    if col_dept:
        unique_depts = df[col_dept].dropna().unique().tolist()
        selected_depts = st.sidebar.multiselect(f"🗂️ القسم:", unique_depts, default=unique_depts)
        filtered_df = filtered_df[filtered_df[col_dept].isin(selected_depts)]

    # فلتر 5: المرحلة
    if col_stage:
        unique_stages = df[col_stage].dropna().unique().tolist()
        selected_stages = st.sidebar.multiselect(f"🏫 المرحلة الدراسية:", unique_stages, default=unique_stages)
        filtered_df = filtered_df[filtered_df[col_stage].isin(selected_stages)]

    # فلتر 6: الجنس
    if col_gender:
        unique_genders = df[col_gender].dropna().unique().tolist()
        selected_genders = st.sidebar.multiselect(f"👥 الجنس / النوع:", unique_genders, default=unique_genders)
        filtered_df = filtered_df[filtered_df[col_gender].isin(selected_genders)]

    # 3. عرض بطاقات المؤشرات العامة الملونة
    st.markdown("### 📈 الخلاصة الإحصائية العامة للبيانات")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"<div class='stat-card' style='border-right-color: #2563EB;'><div class='stat-title'>📊 إجمالي السجلات الحالي</div><div class='stat-val'>{len(filtered_df)} <span style='font-size:14px; color:#64748B;'>من {len(df)}</span></div></div>", unsafe_allow_html=True)
    with c2:
        total_offices = filtered_df[col_office].nunique() if col_office else 0
        st.markdown(f"<div class='stat-card' style='border-right-color: #10B981;'><div class='stat-title'>🏢 المكاتب المشمولة</div><div class='stat-val'>{total_offices}</div></div>", unsafe_allow_html=True)
    with c3:
        total_stages = filtered_df[col_stage].nunique() if col_stage else 0
        st.markdown(f"<div class='stat-card' style='border-right-color: #EF4444;'><div class='stat-title'>🏫 المراحل المشمولة</div><div class='stat-val'>{total_stages}</div></div>", unsafe_allow_html=True)
    with c4:
        total_edu = filtered_df[col_edu_type].nunique() if col_edu_type else 0
        st.markdown(f"<div class='stat-card' style='border-right-color: #F59E0B;'><div class='stat-title'>🎓 أنواع التعليم النشطة</div><div class='stat-val'>{total_edu}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # 4. ألسنة استعراض الأعداد والتمثيل البياني للتصنيفات الستة (Tabs)
    st.markdown("### 🏢 استعراض توزيع الأعداد ونسب الاستحواذ التفصيلية")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎓 نوع التعليم", "🏢 المكاتب", "⚙️ الوحدات", "🗂️ الأقسام", "🏫 المراحل", "👥 الجنس"
    ])
    
    # قائمة الإعدادات الخاصة بالألسنة لربط البيانات تلقائياً
    target_tabs = [
        (tab1, col_edu_type, px.colors.sequential.Blugrn, "نوع التعليم"),
        (tab2, col_office, px.colors.sequential.Cividis, "المكاتب"),
        (tab3, col_unit, px.colors.sequential.Plasma, "الوحدات"),
        (tab4, col_dept, px.colors.sequential.Viridis, "الأقسام"),
        (tab5, col_stage, px.colors.sequential.RdBu, "المراحل"),
        (tab6, col_gender, px.colors.sequential.Sunset, "الجنس")
    ]

    for tab, col_name, color_scale, label in target_tabs:
        with tab:
            if col_name and col_name in filtered_df.columns:
                st.markdown(f"**📊 تحليل حقل المعاينة الحالي: `{col_name}`**")
                
                # حساب الأعداد والنسب المئوية
                count_df = filtered_df[col_name].value_counts().reset_index()
                count_df.columns = [col_name, 'العدد الحالي']
                count_df['النسبة المئوية (%)'] = ((count_df['العدد الحالي'] / len(filtered_df)) * 100).round(1)
                
                col_left, col_right = st.columns()
                with col_left:
                    st.dataframe(count_df, use_container_width=True, hide_index=True)
                with col_right:
                    fig = px.bar(count_df, x=col_name, y='العدد الحالي', text='العدد الحالي',
                                 color=col_name, color_discrete_sequence=color_scale)
                    fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"⚠️ الحقل المخصص لـ '{label}' لم يتم العثور عليه بالملف، تأكد من مسمى العمود في ملف الإكسل المرفوع.")

    st.markdown("---")
    
    # 5. عرض جدول البيانات المفرز النهائي 
    with st.expander("👀 استعراض قاعدة البيانات الكاملة والمحدثة وفقاً للتصفية الحالية"):
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("💡 في انتظار رفع ملف البيانات (Excel / CSV) من الشريط الجانبي لتفعيل الفلاتر الستة والرسوم البيانية الملونة...")
