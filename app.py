import streamlit as st
import pandas as pd
from pipeline import clean_artisan_image, parse_voice_and_extract_wisdom, calculate_dynamic_price

st.set_page_config(page_title="KalaSetu Prototype", layout="wide")

st.title("🌾 KalaSetu: Smart Artisan Cataloging Engine")
st.caption("Smart India Hackathon 2026 — Team CodeLoom (PS: SIH26090)")

tab1, tab2 = st.tabs(["🚀 Voice-to-Listing Live Demo", "📊 Reference Dataset & Price Benchmark"])

with tab1:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("1. Artisan Input (Voice & Raw Photo)")
        
        audio_choice = st.selectbox(
            "Select Spoken Voice Input (Regional Dialect Sample)",
            [
                "Mitti hum Narmada kinare se laate hain, isme thandak rehti hai aur paani meetha banta hai. (Clay Pot)",
                "Channapatna ki lakdi aur haldi ka rang use kiya hai taaki bache muh me le toh koi poison na ho. (Wooden Toy)",
                "Hamne natural neem aur flower extract se yeh painting banayi hai jo 50 saal tak fade nahi hogi. (Madhubani)"
            ]
        )
        
        uploaded_image = st.file_uploader("Upload Unprocessed Craft Photo", type=["jpg", "png", "jpeg"])
        
        st.markdown("**Production Estimates**")
        c1, c2, c3 = st.columns(3)
        mat_cost = c1.number_input("Raw Material Cost (₹)", value=250, step=50)
        hours = c2.number_input("Labor Time (Hours)", value=12, step=1)
        tier = c3.selectbox("Craft Complexity", options=[1, 2, 3], format_func=lambda x: {1: "Standard", 2: "Intricate", 3: "Mastercraft"}[x])

        process_btn = st.button("Generate Catalog Listing", type="primary")

    with col_right:
        st.subheader("2. AI Photo Studio & Wisdom Extraction")
        
        if process_btn:
            with st.spinner("Executing Indic NLP, Image Segmentation & Price Inference..."):
                parsed = parse_voice_and_extract_wisdom(audio_choice)
                pricing = calculate_dynamic_price(mat_cost, hours, tier)

                if uploaded_image:
                    cleaned_bytes = clean_artisan_image(uploaded_image.read())
                    st.image(cleaned_bytes, caption="AI Photo Studio: Clean White Canvas", width=280)
                else:
                    st.info("Upload an image on the left to see live background removal.")

                st.success("✅ **Wisdom Layer Documented:**")
                st.write(f"> *\"{parsed['wisdom_layer']}\"*")

                st.markdown("### 🛍️ Generated Listing")
                st.write(f"**English Title:** {parsed['title_en']}")
                st.write(f"**Hindi Title:** {parsed['title_hi']}")
                st.write(f"**Keywords:** {', '.join(parsed['suggested_tags'])}")

                st.markdown("### 💰 Dynamic Pricing Assistant")
                p1, p2, p3 = st.columns(3)
                p1.metric("Fair Price (Direct)", f"₹{pricing['fair_price_inr']}")
                p2.metric("Market Range", f"₹{pricing['suggested_range'][0]} - ₹{pricing['suggested_range'][1]}")
                p3.metric("Middleman Buyout", f"₹{pricing['middleman_comparison_inr']}", delta=f"-₹{pricing['fair_price_inr'] - pricing['middleman_comparison_inr']}", delta_color="inverse")

                st.markdown("### 📤 Marketplace Direct Integration")
                gem_payload = {
                    "product_name": parsed["title_en"],
                    "category": parsed["category"],
                    "unit_price": pricing["fair_price_inr"],
                    "provenance_wisdom": parsed["wisdom_layer"],
                    "compliance_standard": "GeM-Handicraft-V2"
                }
                st.json(gem_payload)

with tab2:
    st.subheader("Ground Truth Training Dataset (60 Sample Crafts)")
    df_preview = pd.read_csv("artisan_dataset_60.csv")
    st.dataframe(df_preview, use_container_width=True)