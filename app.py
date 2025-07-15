# প্রয়োজনীয় লাইব্রেরি ইম্পোর্ট করা
import streamlit as st
import pandas as pd

# --- অ্যাপের শিরোনাম এবং প্রাথমিক কনফিগারেশন ---
st.set_page_config(page_title="ডেটা সার্চ অ্যাপ", layout="wide")
st.title("📊 এক্সেল ডেটা সার্চ অ্যাপ")
st.write("যেকোনো কলাম অনুযায়ী ডেটা সার্চ করুন।")

# --- ডেটা লোড করার ফাংশন এবং ক্যাশিং ---
# @st.cache_data ব্যবহার করলে অ্যাপ দ্রুত কাজ করে, কারণ এটি বারবার ফাইল লোড করে না
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: '{file_path}' ফাইলটি খুঁজে পাওয়া যায়নি। দয়া করে সঠিক স্থানে ফাইলটি রাখুন।")
        return None
    except Exception as e:
        st.error(f"একটি অপ্রত্যাশিত ত্রুটি ঘটেছে: {e}")
        return None

# ডেটা ফাইল লোড করা
df = load_data('data.xlsx')

# ডেটা সফলভাবে লোড হলে বাকি অ্যাপ দেখাবে
if df is not None:
    
    # --- সাইডবার: সার্চ অপশনগুলো দেখানোর জন্য ---
    st.sidebar.header("সার্চ অপশন")

    # কলাম সিলেক্ট করার অপশন
    # df.columns.tolist() স্বয়ংক্রিয়ভাবে এক্সেলের সব কলামের নাম নিয়ে আসবে
    search_column = st.sidebar.selectbox(
        "কোন কলামে সার্চ করতে চান?",
        options=df.columns.tolist(),
        index=1  # ডিফল্ট হিসেবে দ্বিতীয় কলামটি (পণ্যের নাম) সিলেক্ট করা থাকবে
    )

    # সার্চ করার জন্য টেক্সট ইনপুট বক্স
    search_query = st.sidebar.text_input(
        f"'{search_column}' অনুযায়ী সার্চ করুন:",
        placeholder="এখানে সার্চ করুন..."
    )

    # --- মূল পেইজ: ফলাফল প্রদর্শন ---
    st.divider() # একটি বিভাজক রেখা

    # যদি সার্চ বক্সে কিছু লেখা হয়
    if search_query:
        # .str.contains() ব্যবহার করে সার্চ করা হচ্ছে। case=False মানে ছোট/বড় হাতের অক্ষর মিলিয়ে দেখবে না।
        mask = df[search_column].astype(str).str.contains(search_query, case=False, na=False)
        result_df = df[mask]

        st.write(f"'{search_query}' এর জন্য **{len(result_df)}** টি ফলাফল পাওয়া গেছে:")
        
        # ফলাফল দেখানো হচ্ছে
        st.dataframe(result_df, use_container_width=True)

    # যদি সার্চ বক্স খালি থাকে, তাহলে পুরো ডেটা দেখানো হবে
    else:
        st.write("সম্পূর্ণ ডেটা টেবিল:")
        st.dataframe(df, use_container_width=True)