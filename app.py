import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة والأسلوب البصري الملون (رسمية وحديثة)
st.set_page_config(page_title="منصة التحليل الإحصائي المتقدمة", page_icon="📊", layout="wide")

# تخصيص المظهر بألوان رسمية مريحة
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
    .stat-val { color: #1E3A8A; font-size: 28px; font-weight: bold; padding-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي للمنصة
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📊 لوحة التحكم والإحصائيات الرسمية المتقدمة</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 18px;'>نظام الفرز الثلاثي الذكي والتحليل التفاعلي</p>", unsafe_allow_html=True)
st.markdown("---")

# رفع الملف من القائمة الجانبية
st.sidebar.markdown("<h2 style='color: #1E3A8A;'>📂 تحميل البيانات</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("قم برفع ملف البيانات (Excel / CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # قراءة الملف تلقائياً
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # تنظيف مسميات الحقول من أي مسافات زائدة
    df.columns = df.columns.str.strip()
    all_cols = df.columns.tolist()
    
    # التعرف الذكي على حقول الفرز الثلاثة (المكتب، الوحدة، القسم) بناءً على الكلمات الدلالية
    col_office = next((c for c in all_cols if 'مكتب' in c or 'المكتب' in c), None)
    col_unit = next((c for c in all_cols if 'وحدة' in c or 'الوحدة' in c), None)
    col_dept = next((c for c in all_cols if 'قسم' in c or 'القسم' in c), None)
    
    # 2. قسم خيارات الفرز والتصفية الثلاثة (3 Filters) في الشريط الجانبي
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h2 style='color: #1E3A8A;'>🔍 خيارات التصفية والفرز</h2>", unsafe_allow_html=True)
    
    filtered_df = df.copy()
    
    # الفلتر الأول: المكتب
    if col_office:
        unique_offices = df[col_office].dropna().unique().tolist()
        selected_offices = st.sidebar.multiselect(f"🏢 تصفية حسب {col_office}:", unique_offices, default=unique_offices)
        filtered_df = filtered_df[filtered_df[col_office].isin(selected_offices)]
    else:
        st.sidebar.warning("⚠️ لم يتم العثور على حقل يحتوي على كلمة 'مكتب'")
        
    # الفلتر الثاني: الوحدة
    if col_unit:
        unique_units = df[col_unit].dropna().unique().tolist()
        selected_units = st.sidebar.multiselect(f"⚙️ تصفية حسب {col_unit}:", unique_units, default=unique_units)
        filtered_df = filtered_df[filtered_df[col_unit].isin(selected_units)]
    else:
        st.sidebar.warning("⚠️ لم يتم العثور على حقل يحتوي على كلمة 'وحدة'")
        
    # الفلتر الثالث: القسم
    if col_dept:
        unique_depts = df[col_dept].dropna().unique().tolist()
        selected_depts = st.sidebar.multiselect(f"🗂️ تصفية حسب {col_dept}:", unique_depts, default=unique_depts)
        filtered_df = filtered_df[filtered_df[col_dept].isin(selected_depts)]
    else:
        st.sidebar.warning("⚠️ لم يتم العثور على حقل يحتوي على كلمة 'قسم'")

    # 3. عرض بطاقات المؤشرات العامة الملونة (General Analytics Cards)
    st.markdown("### 📈 المؤشرات الإحصائية العامة للبيانات")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"<div class='stat-card' style='border-right-color: #2563EB;'><div class='stat-title'>📊 إجمالي السجلات الحالية</div><div class='stat-val'>{len(filtered_df)} <span style='font-size:14px; color:#64748B;'>من {len(df)}</span></div></div>", unsafe_allow_html=True)
    with c2:
        total_offices = filtered_df[col_office].nunique() if col_office else 0
        st.markdown(f"<div class='stat-card' style='border-right-color: #10B981;'><div class='stat-title'>🏢 المكاتب المشمولة بالتصفية</div><div class='stat-val'>{total_offices}</div></div>", unsafe_allow_html=True)
    with c3:
        total_units = filtered_df[col_unit].nunique() if col_unit else 0
        st.markdown(f"<div class='stat-card' style='border-right-color: #EF4444;'><div class='stat-title'>⚙️ الوحدات المشمولة بالتصفية</div><div class='stat-val'>{total_units}</div></div>", unsafe_allow_html=True)
    with c4:
        total_depts = filtered_df[col_dept].nunique() if col_dept else 0
        st.markdown(f"<div class='stat-card' style='border-right-color: #F59E0B;'><div class='stat-title'>🗂️ الأقسام المشمولة بالتصفية</div><div class='stat-val'>{total_depts}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # 4. ألسنة استعراض الأعداد التفصيلية (Tabs)
    st.markdown("### 🏢 استعراض الأعداد التفصيلية ونسب الاستحواذ")
    
    tab1, tab2, tab3 = st.tabs(["🏢 توزيع المكاتب", "⚙️ توزيع الوحدات", "🗂️ توزيع الأقسام"])
    
    # إحصائيات المكاتب
    with tab1:
        if col_office:
            count_office = filtered_df[col_office].value_counts().reset_index()
            count_office.columns = [col_office, 'العدد الحالي']
            count_office['النسبة المئوية (%)'] = ((count_office['العدد الحالي'] / len(filtered_df)) * 100).round(1)
            
            cl, cr = st.columns([2, 3])
            with cl:
                st.dataframe(count_office, use_container_width=True, hide_index=True)
            with cr:
                fig = px.bar(count_office, x=col_office, y='العدد الحالي', text='العدد الحالي', color=col_office, color_discrete_sequence=px.colors.sequential.Blugrn)
                fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا يمكن عرض إحصاء المكاتب لعدم توفر الحقل بالملف.")

    # إحصائيات الوحدات
    with tab2:
        if col_unit:
            count_unit = filtered_df[col_unit].value_counts().reset_index()
            count_unit.columns = [col_unit, 'العدد الحالي']
            count_unit['النسبة المئوية (%)'] = ((count_unit['العدد الحالي'] / len(filtered_df)) * 100).round(1)
            
            cl, cr = st.columns([2, 3])
            with cl:
                st.dataframe(count_unit, use_container_width=True, hide_index=True)
            with cr:
                fig = px.bar(count_unit, x=col_unit, y='العدد الحالي', text='العدد الحالي', color=col_unit, color_discrete_sequence=px.colors.sequential.Cividis)
                fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا يمكن عرض إحصاء الوحدات لعدم توفر الحقل بالملف.")

    # إحصائيات الأقسام
    with tab3:
        if col_dept:
            count_dept = filtered_df[col_dept].value_counts().reset_index()
            count_dept.columns = [col_dept, 'العدد الحالي']
            count_dept['النسبة المئوية (%)'] = ((count_dept['العدد الحالي'] / len(filtered_df)) * 100).round(1)
            
            cl, cr = st.columns([2, 3])
            with cl:
                st.dataframe(count_dept, use_container_width=True, hide_index=True)
            with cr:
                fig = px.bar(count_dept, x=col_dept, y='العدد الحالي', text='العدد الحالي', color=col_dept, color_discrete_sequence=px.colors.sequential.Plasma)
                fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا يمكن عرض إحصاء الأقسام لعدم توفر الحقل بالملف.")

    st.markdown("---")
    
    # 5. عرض الجدول النهائي
    with st.expander("👀 استعراض جدول البيانات الكامل المفرز والمطابق للفلاتر"):
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("💡 في انتظار رفع ملف البيانات من القائمة الجانبية لبدء الفرز والتحليل الإحصائي...")
