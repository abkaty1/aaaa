import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات المنصة والهوية البصرية لنظام نور
st.set_page_config(page_title="نظام التقارير والإحصاء (هوية نور)", page_icon="🎓", layout="wide")

# تخصيص التصميم والألوان لتطابق روح نظام نور (الأخضر الداكن والرمادي والخطوط الرسمية)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    /* شريط العنوان الملون */
    .noor-header {
        background-color: #12543e; /* الأخضر الداكن لمنصة نور */
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .noor-subtitle { color: #e2e8f0; font-size: 16px; margin-top: 5px; }
    /* بطاقات المؤشرات الرقمية */
    .stat-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 8px;
        border-top: 4px solid #12543e;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }
    .stat-title { color: #64748B; font-size: 14px; font-weight: bold; }
    .stat-val { color: #12543e; font-size: 26px; font-weight: bold; padding-top: 5px; }
    /* تنسيق الفلاتر */
    div[data-testid="stExpander"] { border: 1px solid #e2e8f0; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# ترويسة الصفحة الرسمية بنمط نظام نور
st.markdown("""
    <div class='noor-header'>
        <h1 style='color: white; margin: 0;'>🎓 نظام الإحصاء والمؤشرات المتقدم</h1>
        <div class='noor-subtitle'>المعاينة الذكية للبيانات التعليمية - مستوحى من نظام نور الرسمي</div>
    </div>
""", unsafe_allow_html=True)

# رفع الملف من القائمة الجانبية للحفاظ على الترتيب العلوى للفلاتر
st.sidebar.markdown("<h3 style='color: #12543e; text-align:center;'>📂 بوابة رفع الملفات</h3>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("يرجى اختيار أو سحب ملف البيانات (Excel / CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # قراءة البيانات
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    all_cols = df.columns.tolist()
    
    # محرك البحث الذكي للربط التلقائي للأعمدة
    col_edu_type = next((c for c in all_cols if any(k in c for k in ['نوع التعليم', 'التعليم'])), None)
    col_office   = next((c for c in all_cols if any(k in c for k in ['مكتب', 'المكتب'])), None)
    col_unit     = next((c for c in all_cols if any(k in c for k in ['وحدة', 'الوحدة'])), None)
    col_dept     = next((c for c in all_cols if any(k in c for k in ['قسم', 'القسم'])), None)
    col_stage    = next((c for c in all_cols if any(k in c for k in ['المرحلة', 'مرحلة'])), None)
    col_gender   = next((c for c in all_cols if any(k in c for k in ['الجنس', 'جنس', 'النوع'])), None)

    # 2. لوحة الفلاتر العلوية على شكل قوائم منسدلة (نظام نور)
    st.markdown("### 🔍 محددات البحث والفرز")
    
    # توزيع القوائم المنسدلة الستة في شبكة مرتبة (3 أعمدة في صفين)
    row1_c1, row1_c2, row1_c3 = st.columns(3)
    row2_c1, row2_c2, row2_c3 = st.columns(3)
    
    filtered_df = df.copy()

    # الصف الأول من الفلاتر المنسدلة
    with row1_c1:
        if col_edu_type:
            opts = ["الكل"] + df[col_edu_type].dropna().unique().tolist()
            sel = st.selectbox("🎓 نوع التعليم:", opts)
            if sel != "الكل": filtered_df = filtered_df[filtered_df[col_edu_type] == sel]
        else: st.caption("❌ حقل 'نوع التعليم' غير موجود")

    with row1_c2:
        if col_office:
            opts = ["الكل"] + df[col_office].dropna().unique().tolist()
            sel = st.selectbox("🏢 المكتب:", opts)
            if sel != "الكل": filtered_df = filtered_df[filtered_df[col_office] == sel]
        else: st.caption("❌ حقل 'المكتب' غير موجود")

    with row1_c3:
        if col_unit:
            opts = ["الكل"] + df[col_unit].dropna().unique().tolist()
            sel = st.selectbox("⚙️ الوحدة:", opts)
            if sel != "الكل": filtered_df = filtered_df[filtered_df[col_unit] == sel]
        else: st.caption("❌ حقل 'الوحدة' غير موجود")

    # الصف الثاني من الفلاتر المنسدلة
    with row2_c1:
        if col_dept:
            opts = ["الكل"] + df[col_dept].dropna().unique().tolist()
            sel = st.selectbox("🗂️ القسم:", opts)
            if sel != "الكل": filtered_df = filtered_df[filtered_df[col_dept] == sel]
        else: st.caption("❌ حقل 'القسم' غير موجود")

    with row2_c2:
        if col_stage:
            opts = ["الكل"] + df[col_stage].dropna().unique().tolist()
            sel = st.selectbox("🏫 المرحلة الدراسية:", opts)
            if sel != "الكل": filtered_df = filtered_df[filtered_df[col_stage] == sel]
        else: st.caption("❌ حقل 'المرحلة' غير موجود")

    with row2_c3:
        if col_gender:
            opts = ["الكل"] + df[col_gender].dropna().unique().tolist()
            sel = st.selectbox("👥 الجنس / النوع:", opts)
            if sel != "الكل": filtered_df = filtered_df[filtered_df[col_gender] == sel]
        else: st.caption("❌ حقل 'الجنس' غير موجود")

    st.markdown("---")

    # 3. عرض بطاقات التقارير الإجمالية (نور ديزاين)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='stat-card'><div class='stat-title'>📊 إجمالي السجلات الحالية</div><div class='stat-val'>{len(filtered_df)} <span style='font-size:13px; color:#64748B;'>من {len(df)}</span></div></div>", unsafe_allow_html=True)
    with c2:
        val = filtered_df[col_office].nunique() if col_office else 0
        st.markdown(f"<div class='stat-card'><div class='stat-title'>🏢 المكاتب النشطة</div><div class='stat-val'>{val}</div></div>", unsafe_allow_html=True)
    with c3:
        val = filtered_df[col_stage].nunique() if col_stage else 0
        st.markdown(f"<div class='stat-card'><div class='stat-title'>🏫 المراحل التعليمية</div><div class='stat-val'>{val}</div></div>", unsafe_allow_html=True)
    with c4:
        val = filtered_df[col_gender].nunique() if col_gender else 0
        st.markdown(f"<div class='stat-card'><div class='stat-title'>👥 الفئات المستهدفة</div><div class='stat-val'>{val}</div></div>", unsafe_allow_html=True)

    # 4. ألسنة تفصيلية إحصائية مريحة للعين مع رسوم بيانية منسقة
    st.markdown("### 📊 الجداول والبيانات التحليلية")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎓 نوع التعليم", "🏢 المكاتب", "⚙️ الوحدات", "🗂️ الأقسام", "🏫 المراحل", "👥 الجنس"
    ])
    
    # مصفوفة الألوان والبيانات لبناء المخططات بروح نظام نور المتناسقة
    noor_palette = ["#12543e", "#2a6f57", "#448b72", "#60a88e", "#7dc5aa", "#9be3c7"]
    target_tabs = [
        (tab1, col_edu_type, "نوع التعليم"), (tab2, col_office, "المكاتب"),
        (tab3, col_unit, "الوحدات"), (tab4, col_dept, "الأقسام"),
        (tab5, col_stage, "المراحل"), (tab6, col_gender, "الجنس")
    ]

    for tab, col_name, label in target_tabs:
        with tab:
            if col_name and col_name in filtered_df.columns:
                st.markdown(f"**📈 مسح إحصائي لبيانات: `{col_name}`**")
                
                # بناء الجدول الإحصائي
                count_df = filtered_df[col_name].value_counts().reset_index()
                count_df.columns = [col_name, 'العدد']
                count_df['النسبة مئوية (%)'] = ((count_df['العدد'] / len(filtered_df)) * 100).round(1)
                
                col_l, col_r = st.columns([4, 6])
                with col_l:
                    st.dataframe(count_df, use_container_width=True, hide_index=True)
                with col_r:
                    fig = px.bar(count_df, x=col_name, y='العدد', text='العدد', color_discrete_sequence=noor_palette)
                    fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"الحقل الخاص بـ '{label}' لم يتم تحديده أو التعرف عليه في ملفك بعد.")

    st.markdown("---")
    
    # 5. استعراض الجدول الكامل المفرز بنمط نظام نور للبيانات
    with st.expander("👀 استعراض بيان البيانات المفرزة الكامل"):
        st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("💡 في انتظار رفع ملف البيانات (Excel / CSV) من البوابة الجانبية لتنشيط فلاتر نظام نور الذكية...")
