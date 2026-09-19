import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة الرسمية
st.set_page_config(page_title="منصة الإحصائيات الرسمية", page_icon="📊", layout="wide")

st.title("📊 منصة تحليل البيانات واستخراج الإحصائيات")
st.markdown("---")

# رفع الملف
uploaded_file = st.file_uploader("قم برفع ملف البيانات الخاص بك (Excel أو CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # قراءة الملف ذكيًا حسب نوعه
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # 1. قسم الإحصائيات العامة (General Statistics)
    st.subheader("📋 نظرة عامة وإحصائيات شاملة")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="إجمالي عدد السجلات (الأعمدة)", value=df.shape[0])
    with col2:
        st.metric(label="عدد الحقول (المتغيرات)", value=df.shape[1])
    with col3:
        st.metric(label="الحقول التي تحتوي على قيم فارغة", value=df.isna().sum().sum())
        
    st.markdown("---")
    
    # 2. قسم الإحصائيات حسب التصنيف (Filtered Statistics)
    st.subheader("🔍 الإحصائيات والأعداد حسب التصنيفات")
    
    # اختيار العمود المراد التصنيف بناءً عليه
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if categorical_columns:
        selected_column = st.selectbox("اختر حقل التصنيف لعرض الأعداد:", categorical_columns)
        
        # حساب الأعداد والنسب المئوية
        stats_df = df[selected_column].value_counts().reset_index()
        stats_df.columns = [selected_column, 'العدد (Count)']
        stats_df['النسبة المئوية (%)'] = (stats_df['العدد (Count)'] / len(df) * 100).round(2)
        
        # عرض البيانات في جدولين ومنحنى بياني
        col_table, col_chart = st.columns([1, 1])
        
        with col_table:
            st.write(f"**جدول توزيبي لـ {selected_column}**")
            st.dataframe(stats_df, use_container_width=True)
            
        with col_chart:
            st.write("**التمثيل البياني للتصنيف**")
            fig = px.bar(stats_df, x=selected_column, y='العدد (Count)', text='العدد (Count)', color=selected_column)
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.warning("لم يتم العثور على حقول تصنيفية (نصية) في الملف المرفق.")

    # 3. عرض البيانات كاملة
    with st.expander("👀 استعراض ملف البيانات بالكامل"):
        st.dataframe(df)
else:
    st.info("💡 يرجى رفع ملف البيانات من القائمة أعلاه للبدء في استعراض الإحصائيات.")
