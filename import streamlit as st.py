import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(page_title="محلل ملفات إكسل", layout="wide")
st.title("📊 نظام رفع ومعالجة ملفات Excel")

# أداة رفع الملف
uploaded_file = st.file_uploader("قم باختيار ملف إكسل لرفعه", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # قراءة ملف الإكسل
        df = pd.read_excel(uploaded_file)
        
        st.success("تم رفع الملف وقراءته بنجاح!")
        
        # 1. عرض البيانات الأساسية
        st.header("📋 معاينة البيانات")
        st.dataframe(df.head(10)) # عرض أول 10 أسطر
        
        # 2. عرض معلومات وإحصائيات عامة
        st.header("📉 إحصائيات عامة")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("عدد الأسطر (الصفوف)", df.shape[0])
        with col2:
            st.metric("عدد الأعمدة", df.shape[1])
        with col3:
            st.metric("القيم المفقودة (الفارغة)", df.isna().sum().sum())
            
        # 3. تحليل الأعمدة الرقمية تلقائياً
        st.header("🔢 التحليل الرقمي للأعمدة")
        st.write(df.describe()) # يعرض المتوسط، الحساب، أعلى وأقل قيمة
        
        # 4. رسم بياني تفاعلي تلقائي
        st.header("📊 رسوم بيانية تفاعلية")
        
        # اختيار الأعمدة للرسم البياني
        all_columns = df.columns.tolist()
        x_axis = st.selectbox("اختر عمود المحور الأفقي (X):", all_columns)
        y_axis = st.selectbox("اختر عمود المحور الرأسي (Y):", all_columns)
        
        if x_axis and y_axis:
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"رسم بياني لـ {y_axis} مقابل {x_axis}")
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة الملف: {e}")
else:
    st.info("💡 رجاءً قم برفع ملف Excel من الأداة أعلاه لبدء التحليل.")

