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
    /* بطاقات المؤشرات الرقمية العامة */
    .stat-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 8px;
        border-top: 4px solid #12543e;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }
    /* بطاقات المؤشرات الخاصة والمطابقة */
    .stat-card-special {
        background-color: #f0fdf4;
        padding: 18px;
        border-radius: 8px;
        border-top: 4px solid #16a34a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }
    .stat-title { color: #64748B; font-size: 14px; font-weight: bold; }
    .stat-val { color: #12543e; font-size: 24px; font-weight: bold; padding-top: 5px; }
    .stat-val-special { color: #166534; font-size: 26px; font-weight: bold; padding-top: 5px; }
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

# رفع الملف من القائمة الجانبية
st.sidebar.markdown("<h3 style='color: #12543e; text-align:center;'>📂 بوابة رفع الملفات</h3>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("يرجى اختيار أو سحب ملف البيانات (Excel / CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # قراءة البيانات وتجهيزها
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    all_cols = df.columns.tolist()
    
    # محرك الربط الذكي بالخلفية للتعرف على الحقول تلقائياً
    col_edu_type = next((c for c in all_cols if any(k in c for k in ['نوع التعليم', 'التعليم', 'تعليم'])), all_cols if all_cols else None)
    col_dept     = next((c for c in all_cols if any(k in c for k in ['قسم', 'القسم'])), all_cols if len(all_cols) > 1 else None)
    col_gender   = next((c for c in all_cols if any(k in c for k in ['الجنس', 'جنس', 'النوع', 'نوع'])), all_cols if len(all_cols) > 2 else None)
    col_students = next((c for c in all_cols if any(k in c for k in ['طلاب', 'الطلاب', 'طالب', 'عدد الطلاب'])), None)
    col_schools  = next((c for c in all_cols if any(k in c for k in ['عدد المدارس', 'المدارس', 'مدرسة'])), None)

    # تحويل البيانات إلى أرقام بشكل آمن لمنع الأخطاء الحسابية
    if col_students and col_students in df.columns:
        df[col_students] = pd.to_numeric(df[col_students], errors='coerce').fillna(0)
    if col_schools and col_schools in df.columns:
        df[col_schools] = pd.to_numeric(df[col_schools], errors='coerce').fillna(0)

    # 2. لوحة الفلاتر العلوية على شكل قوائم منسدلة (نظام نور)
    st.markdown("### 🔍 محددات البحث والفرز")
    
    row_c1, row_c2, row_c3 = st.columns(3)
    filtered_df = df.copy()

    # القوائم المنسدلة الثلاثة
    with row_c1:
        if col_edu_type and col_edu_type in df.columns:
            opts_edu = ["الكل"] + df[col_edu_type].dropna().unique().tolist()
            sel_edu = st.selectbox("🎓 نوع التعليم:", opts_edu)
            if sel_edu != "الكل": 
                filtered_df = filtered_df[filtered_df[col_edu_type] == sel_edu]
        else:
            sel_edu = "الكل"

    with row_c2:
        if col_dept and col_dept in df.columns:
            opts_dept = ["الكل"] + df[col_dept].dropna().unique().tolist()
            sel_dept = st.selectbox("🗂️ القسم:", opts_dept)
            if sel_dept != "الكل": 
                filtered_df = filtered_df[filtered_df[col_dept] == sel_dept]
        else:
            sel_dept = "الكل"

    with row_c3:
        if col_gender and col_gender in df.columns:
            opts_gender = ["الكل"] + df[col_gender].dropna().unique().tolist()
            sel_gender = st.selectbox("👥 الجنس / النوع:", opts_gender)
            if sel_gender != "الكل": 
                filtered_df = filtered_df[filtered_df[col_gender] == sel_gender]
        else:
            sel_gender = "الكل"

    st.markdown("---")

    # 3. حساب القيم الكلية العامة والفرعية الحالية المحدثة ديناميكياً بناءً على السجلات
    if col_schools and col_schools in filtered_df.columns:
        current_schools_total = int(filtered_df[col_schools].sum())
        global_schools_raw = int(df[col_schools].sum())
    else:
        current_schools_total = len(filtered_df)
        global_schools_raw = len(df)
        
    if col_students and col_students in filtered_df.columns:
        current_students_total = int(filtered_df[col_students].sum())
        global_students_raw = int(df[col_students].sum())
    else:
        current_students_total = 0
        global_students_raw = 0

    # 4. عرض بطاقات التقارير الإجمالية العامة المحدثة (تعديل مسمى مجموع المدارس وحذف الإجمالي المكرر)
    st.markdown("### 📈 الخلاصة الإحصائية العامة للبيانات")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='stat-card'><div class='stat-title'>🏢 مجموع المدارس</div><div class='stat-val'>{current_schools_total:,} <span style='font-size:12px; color:#64748B;'>من {global_schools_raw:,}</span></div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card'><div class='stat-title'>👥 إجمالي الطلاب الحالي</div><div class='stat-val'>{current_students_total:,} <span style='font-size:12px; color:#64748B;'>من {global_students_raw:,}</span></div></div>", unsafe_allow_html=True)
    with c3:
        val = filtered_df[col_dept].nunique() if (col_dept and col_dept in filtered_df.columns) else 0
        st.markdown(f"<div class='stat-card'><div class='stat-title'>🗂️ الأقسام النشطة</div><div class='stat-val'>{val}</div></div>", unsafe_allow_html=True)
    with c4:
        val = filtered_df[col_gender].nunique() if (col_gender and col_gender in filtered_df.columns) else 0
        st.markdown(f"<div class='stat-card'><div class='stat-title'>👥 الفئات المستهدفة</div><div class='stat-val'>{val}</div></div>", unsafe_allow_html=True)

    # 5. قسم إحصائيات المطابقة الخاصة بالقسم ونوع التعليم المحددين
    if sel_edu != "الكل" and sel_dept != "الكل":
        st.markdown("### 🎯 إحصائيات المطابقة الخاصة بالقسم ونوع التعليم المحددين")
        sc1, sc2 = st.columns(2)
        
        with sc1:
            if col_schools and col_schools in filtered_df.columns:
                total_schools_sum = filtered_df[col_schools].sum()
                st.markdown(f"<div class='stat-card-special'><div class='stat-title'>🏢 مجموع المدارس المطابقة</div><div class='stat-val-special'>{int(total_schools_sum):,} مدرسة</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='stat-card-special'><div class='stat-title'>🏢 مجموع المدارس المطابقة</div><div class='stat-val-special'>{len(filtered_df):,} مدرسة</div></div>", unsafe_allow_html=True)
                
        with sc2:
            if col_students and col_students in filtered_df.columns:
                total_students_sum = filtered_df[col_students].sum()
                st.markdown(f"<div class='stat-card-special'><div class='stat-title'>👥 مجموع الطلاب المشمولين</div><div class='stat-val-special'>{int(total_students_sum):,} طالب</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='stat-card-special'><div class='stat-title'>👥 مجموع الطلاب المطابقين</div><div class='stat-val-special' style='font-size:16px; color:#991b1b;'>0 طالب</div></div>", unsafe_allow_html=True)
                
        st.markdown("---")

    # 6. ألسنة تفصيلية إحصائية حرة ومباشرة الظهور تدمج المدارس وإجمالي الطلاب من الملف
    st.markdown("### 📊 الجداول والبيانات التحليلية")
    tab1, tab2, tab3 = st.tabs([
        "🎓 نوع التعليم", "🗂️ الأقسام", "👥 الجنس"
    ])
    
    noor_palette = ["#12543e", "#2a6f57", "#448b72", "#60a88e", "#7dc5aa", "#9be3c7"]
    target_tabs = [
        (tab1, col_edu_type, "نوع التعليم"),
        (tab2, col_dept, "الأقسام"),
        (tab3, col_gender, "الجنس")
    ]

    for tab, col_name, label in target_tabs:
        with tab:
            if col_name and col_name in filtered_df.columns:
                st.markdown(f"**📈 مسح إحصائي تحليلي لبيانات: `{col_name}`**")
                
                total_filtered_len = len(filtered_df) if len(filtered_df) > 0 else 1
                
                # استخدام طريقة الربط التجميعي المستقر والآمن
                count_series = filtered_df.groupby(col_name).size()
                
                if col_students and col_students in filtered_df.columns:
                    sum_series = filtered_df.groupby(col_name)[col_students].sum()
                    count_df = pd.concat([count_series, sum_series], axis=1).reset_index()
                    count_df.columns = [col_name, 'العدد (المدارس)', 'إجمالي عدد الطلاب']
                else:
                    count_df = count_series.reset_index()
                    count_df.columns = [col_name, 'العدد (المدارس)']
                
