"""
Cogaint Clean Demo App
Fixed syntax errors, works with simplified engine
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import json
import time
from demo_engine import CogaintLeanDemo

# Page configuration
st.set_page_config(
    page_title="Cogaint: SKU-Velocity Lending Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .success-rate {
        background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .warning-rate {
        background: linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .danger-rate {
        background: linear-gradient(90deg, #ef4444 0%, #f87171 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'demo_engine' not in st.session_state:
    st.session_state.demo_engine = CogaintLeanDemo()

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Cogaint: SKU-Velocity Lending</h1>
        <h3>Get Better Rates on Your Best-Performing Inventory</h3>
        <p>AI-powered financing that rewards performance • $500K-$5M loans • 10-22% rates based on velocity</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🎯 Demo Navigation")
    demo_section = st.sidebar.selectbox(
        "Choose Demo Section:",
        ["🏠 Value Proposition", "🔍 SKU Intelligence", "📊 Business Scoring", "💰 Rate Calculator", "📈 Upload Your Data"]
    )
    
    # Demo sections
    if demo_section == "🏠 Value Proposition":
        show_value_proposition()
    elif demo_section == "🔍 SKU Intelligence":
        show_sku_intelligence()
    elif demo_section == "📊 Business Scoring":
        show_business_scoring()
    elif demo_section == "💰 Rate Calculator":
        show_rate_calculator()
    elif demo_section == "📈 Upload Your Data":
        show_customer_upload()

def show_value_proposition():
    st.header("💡 The Cogaint Advantage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("❌ Traditional Lending")
        st.markdown("""
        - 18-22% for all businesses
        - 2-8 weeks for decisions
        - Ignores performance
        - Manual underwriting
        """)
        
        st.markdown("""
        <div class="danger-rate">
            <h3>Traditional: 18-22%</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("✅ Cogaint Solution")
        st.markdown("""
        - 10-22% based on velocity
        - <24 hour decisions
        - Rewards performance
        - AI-powered analysis
        """)
        
        st.markdown("""
        <div class="success-rate">
            <h3>Cogaint: 10-18%</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("💰 Potential Savings")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Loan Amount", "$1,000,000")
    with col2:
        st.metric("Rate Savings", "8% lower")
    with col3:
        st.metric("Annual Savings", "$80,000")

def show_sku_intelligence():
    st.header("🔍 AI-Powered SKU Intelligence")
    
    company_options = list(st.session_state.demo_engine.demo_companies.keys())
    selected_company = st.selectbox("Choose a demo company:", company_options)
    
    if st.button("🧠 Analyze SKU Fragmentation", type="primary"):
        with st.spinner("Running AI analysis..."):
            time.sleep(1)
            frag_result = st.session_state.demo_engine.demonstrate_sku_fragmentation(selected_company)
        
        st.subheader("❌ The Fragmentation Problem")
        frag_data = frag_result["fragmented_data"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.code(f"ERP:\n{frag_data['ERP System']}")
        with col2:
            st.code(f"WMS:\n{frag_data['WMS System']}")
        with col3:
            st.code(f"Shopify:\n{frag_data['Shopify Store']}")
        with col4:
            st.code(f"Product:\n{frag_data['Product Name']}")
        
        st.error("Traditional systems see: 4 different products ❌")
        
        st.divider()
        st.subheader("✅ Cogaint AI Solution")
        
        ai_solution = frag_result["ai_solution"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("AI recognizes: 1 unified product ✅")
            st.markdown(f"**Name:** {ai_solution['unified_name']}")
            st.markdown(f"**Confidence:** {ai_solution['confidence']}%")
        with col2:
            st.metric("Time Saved", frag_result["time_saved"])
            st.metric("Accuracy", frag_result["accuracy"])
        
        st.info(f"**Reasoning:** {ai_solution['reasoning']}")

def show_business_scoring():
    st.header("📊 Business Assessment")
    
    company_options = list(st.session_state.demo_engine.demo_companies.keys())
    
    st.subheader("🏆 Company Comparison")
    
    for company_key in company_options:
        company_info = st.session_state.demo_engine.demo_companies[company_key]
        scoring_result = st.session_state.demo_engine.calculate_business_score(company_key)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"**{company_info['name']}**")
        with col2:
            st.markdown(f"Revenue: ${company_info['revenue']:,}")
        with col3:
            st.markdown(f"Score: {scoring_result['final_score']}/100")
        with col4:
            st.markdown(f"Rate: {scoring_result['recommended_rate']}%")
    
    st.divider()
    selected_company = st.selectbox("Select for detailed analysis:", company_options)
    
    if st.button("📈 Analyze Company", type="primary"):
        with st.spinner("Running analysis..."):
            time.sleep(1)
            scoring_result = st.session_state.demo_engine.calculate_business_score(selected_company)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            score = scoring_result['final_score']
            if score >= 70:
                st.markdown(f'<div class="success-rate"><h3>Score: {score}/100</h3></div>', unsafe_allow_html=True)
            elif score >= 50:
                st.markdown(f'<div class="warning-rate"><h3>Score: {score}/100</h3></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="danger-rate"><h3>Score: {score}/100</h3></div>', unsafe_allow_html=True)
        
        with col2:
            st.metric("Rate", f"{scoring_result['recommended_rate']}%")
            st.metric("Category", scoring_result['risk_category'])
        
        with col3:
            decision = scoring_result['decision']
            if "APPROVED" in decision:
                st.success(f"✅ {decision}")
            else:
                st.warning(f"⚠️ {decision}")
        
        st.subheader("📋 Scoring Factors")
        for factor in scoring_result['factors']:
            st.markdown(f"- {factor}")

def show_rate_calculator():
    st.header("💰 Rate Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        revenue = st.number_input("Annual Revenue ($)", value=2000000)
        inventory_turns = st.slider("Inventory Turns", 0.5, 20.0, 6.0)
        years_operating = st.number_input("Years Operating", value=3)
        
    with col2:
        industry = st.selectbox("Industry", [
            "Food & Beverage", "Supplements", "Beauty & Personal Care"
        ])
        loan_amount = st.number_input("Loan Amount ($)", value=1000000)
    
    if st.button("🎯 Calculate Rate", type="primary"):
        with st.spinner("Calculating..."):
            time.sleep(1)
            
            temp_data = {
                "revenue": revenue,
                "inventory_turns": inventory_turns,
                "industry": industry,
                "years_operating": years_operating
            }
            
            result = st.session_state.demo_engine.process_customer_upload(temp_data)
        
        if "error" not in result:
            rate = result['rate']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if rate <= 12:
                    st.markdown(f'<div class="success-rate"><h3>Rate: {rate}%</h3></div>', unsafe_allow_html=True)
                elif rate <= 18:
                    st.markdown(f'<div class="warning-rate"><h3>Rate: {rate}%</h3></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="danger-rate"><h3>Rate: {rate}%</h3></div>', unsafe_allow_html=True)
            
            with col2:
                st.metric("Score", f"{result['score']}/100")
            
            with col3:
                traditional_rate = 20.0
                savings = (traditional_rate - rate) * 0.01 * loan_amount
                if savings > 0:
                    st.metric("Annual Savings", f"${savings:,.0f}")

def show_customer_upload():
    st.header("📈 Upload Your Data")
    
    with st.form("customer_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name")
            revenue = st.number_input("Annual Revenue ($)", value=1000000)
            inventory_value = st.number_input("Inventory Value ($)", value=200000)
            
        with col2:
            industry = st.selectbox("Industry", ["Food & Beverage", "Supplements", "Other"])
            years = st.number_input("Years Operating", value=2)
            loan_amount = st.number_input("Desired Loan ($)", value=500000)
        
        submitted = st.form_submit_button("🚀 Get My Rate", type="primary")
        
        if submitted and company_name:
            with st.spinner("Analyzing..."):
                time.sleep(2)
                
                turns = (revenue * 0.7) / inventory_value if inventory_value > 0 else 4.0
                
                data = {
                    "company_name": company_name,
                    "revenue": revenue,
                    "inventory_turns": turns,
                    "industry": industry,
                    "years_operating": years
                }
                
                result = st.session_state.demo_engine.process_customer_upload(data)
            
            if "error" not in result:
                st.success("✅ Analysis Complete!")
                
                rate = result['rate']
                decision = result['decision']
                
                col1, col2 = st.columns(2)
                with col1:
                    if rate <= 12:
                        st.markdown(f'<div class="success-rate"><h3>Your Rate: {rate}%</h3></div>', unsafe_allow_html=True)
                    elif rate <= 18:
                        st.markdown(f'<div class="warning-rate"><h3>Your Rate: {rate}%</h3></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="danger-rate"><h3>Your Rate: {rate}%</h3></div>', unsafe_allow_html=True)
                
                with col2:
                    if "APPROVED" in decision:
                        st.success(f"✅ {decision}")
                    else:
                        st.warning(f"⚠️ {decision}")
                
                if st.button("📞 Schedule Call", type="primary"):
                    st.balloons()
                    st.success("Thank you! Our team will contact you within 24 hours.")

def show_footer():
    st.divider()
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p><strong>🚀 Cogaint</strong> - AI-Powered Inventory Financing</p>
        <p>Visit <a href="https://cogaint.com" target="_blank">cogaint.com</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()