"""
Cogaint Robust Demo Engine with AI
Handles OpenAI errors gracefully while preserving AI functionality
"""

import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

class CogaintLeanDemo:
    def __init__(self):
        # Initialize with proper error handling
        self.openai_client = None
        self.ai_enabled = False
        self.ai_error = None
        
        self._initialize_openai()
        
        # Demo companies with realistic data
        self.demo_companies = {
            "VelocitySnacks (High Performer)": {
                "name": "VelocitySnacks Co",
                "industry": "Food & Beverage",
                "revenue": 3500000,
                "inventory_turns": 12,
                "years_operating": 4,
                "description": "Fast-growing protein bar company with strong D2C sales",
                "skus": [
                    {"name": "Chocolate Protein Bar", "erp": "PB-CHOC-001", "wms": "PROTBAR_CHOC_12PK", 
                     "shopify": "protein-bar-chocolate", "monthly_velocity": 2500, "margin": 35},
                    {"name": "Vanilla Protein Bar", "erp": "PB-VAN-001", "wms": "PROTBAR_VAN_12PK",
                     "shopify": "protein-bar-vanilla", "monthly_velocity": 1800, "margin": 35}
                ]
            },
            "HealthyFoods (Medium Performer)": {
                "name": "HealthyFoods Inc",
                "industry": "Supplements", 
                "revenue": 1200000,
                "inventory_turns": 6,
                "years_operating": 2,
                "description": "Growing supplement brand with seasonal patterns",
                "skus": [
                    {"name": "Vitamin D3 Supplement", "erp": "VD3-5000-60", "wms": "VITAMIN_D3_60CT",
                     "shopify": "vitamin-d3-5000iu", "monthly_velocity": 800, "margin": 45}
                ]
            },
            "SlowMovers Co (Struggling)": {
                "name": "GourmetSauces Ltd",
                "industry": "Specialty Foods",
                "revenue": 800000,
                "inventory_turns": 2.5,
                "years_operating": 6,
                "description": "Premium sauce maker with inventory challenges",
                "skus": [
                    {"name": "Truffle Pasta Sauce", "erp": "GPS-TRUF-16", "wms": "SAUCE_TRUFFLE_16OZ",
                     "shopify": "gourmet-truffle-sauce", "monthly_velocity": 120, "margin": 25}
                ]
            }
        }
    
    def _initialize_openai(self):
        """Safely initialize OpenAI with detailed error reporting"""
        try:
            # Try Streamlit secrets first, then fall back to environment variables
            api_key = None
            
            # Check if running in Streamlit
            try:
                import streamlit as st
                if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                    api_key = st.secrets["OPENAI_API_KEY"]
                    print("🔐 Using Streamlit secrets for API key")
            except:
                pass
            
            # Fall back to environment variable
            if not api_key:
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    print("🔐 Using environment variable for API key")
            
            if not api_key:
                self.ai_error = "No OPENAI_API_KEY found in environment variables"
                print(f"⚠️ {self.ai_error}")
                return
            
            if not (api_key.startswith("sk-proj-") or api_key.startswith("sk-")):
                self.ai_error = f"Invalid API key format. Key should start with 'sk-proj-' or 'sk-'"
                print(f"⚠️ {self.ai_error}")
                return
            
            # Try to create the client
            self.openai_client = openai.OpenAI(api_key=api_key)
            
            # Test with a minimal API call
            test_response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            
            self.ai_enabled = True
            print("✅ OpenAI client initialized and tested successfully")
            
        except openai.AuthenticationError:
            self.ai_error = "OpenAI API key authentication failed - key may be invalid or expired"
            print(f"❌ {self.ai_error}")
        except openai.RateLimitError:
            self.ai_error = "OpenAI rate limit exceeded - may be out of credits"
            print(f"❌ {self.ai_error}")
        except Exception as e:
            self.ai_error = f"OpenAI initialization failed: {str(e)}"
            print(f"❌ {self.ai_error}")
    
    def get_ai_status(self):
        """Get current AI status for display in Streamlit"""
        if self.ai_enabled:
            return {"status": "enabled", "message": "AI features fully operational"}
        else:
            return {"status": "disabled", "message": f"AI disabled: {self.ai_error}"}
    
    def demonstrate_sku_fragmentation(self, company_key):
        """Show SKU fragmentation problem with AI solution when available"""
        
        company = self.demo_companies[company_key]
        sample_sku = company["skus"][0]
        
        # Show the fragmentation problem
        fragmented_data = {
            "ERP System": sample_sku["erp"],
            "WMS System": sample_sku["wms"], 
            "Shopify Store": sample_sku["shopify"],
            "Product Name": sample_sku["name"]
        }
        
        # Try AI analysis if available
        if self.ai_enabled and self.openai_client:
            try:
                ai_analysis = self._get_ai_sku_analysis(sample_sku)
                ai_source = "OpenAI GPT-4"
            except Exception as e:
                print(f"AI analysis failed: {e}, using enhanced fallback")
                ai_analysis = self._get_enhanced_fallback_analysis(sample_sku)
                ai_source = "Cogaint Logic Engine"
        else:
            ai_analysis = self._get_enhanced_fallback_analysis(sample_sku)
            ai_source = "Cogaint Logic Engine"
        
        # Add the AI source to the response
        ai_analysis["ai_source"] = ai_source
        
        return {
            "fragmented_data": fragmented_data,
            "ai_solution": ai_analysis,
            "time_saved": "2+ hours → 30 seconds",
            "accuracy": "95%+ with AI vs 60% manual",
            "ai_status": self.get_ai_status()
        }
    
    def _get_ai_sku_analysis(self, sample_sku):
        """Get real AI analysis of SKU fragmentation"""
        prompt = f"""
        Analyze these product identifiers from different business systems and determine if they refer to the same product:
        
        ERP SKU: {sample_sku['erp']}
        WMS SKU: {sample_sku['wms']}
        Shopify SKU: {sample_sku['shopify']}
        Product Name: {sample_sku['name']}
        
        Respond with valid JSON only:
        {{
            "same_product": true,
            "confidence": 95,
            "unified_name": "suggested product name",
            "reasoning": "detailed explanation of why these match",
            "risk_factors": ["any concerns"],
            "pattern_analysis": "analysis of naming patterns"
        }}
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _get_enhanced_fallback_analysis(self, sample_sku):
        """Enhanced fallback analysis when AI is not available"""
        
        # Analyze naming patterns
        erp_parts = sample_sku["erp"].split("-")
        wms_parts = sample_sku["wms"].split("_")
        shopify_parts = sample_sku["shopify"].split("-")
        
        confidence = 85
        reasoning = f"Pattern analysis of '{sample_sku['name']}':"
        
        # Check for common elements
        if any(part.lower() in sample_sku["name"].lower() for part in erp_parts):
            confidence += 5
            reasoning += " ERP code contains product identifiers."
        
        if any(part.lower() in sample_sku["name"].lower() for part in wms_parts):
            confidence += 5
            reasoning += " WMS code follows logical naming convention."
        
        if any(part in sample_sku["shopify"] for part in sample_sku["name"].lower().split()):
            confidence += 5
            reasoning += " Shopify URL matches product name structure."
        
        return {
            "same_product": True,
            "confidence": min(confidence, 98),
            "unified_name": sample_sku["name"],
            "reasoning": reasoning + f" All identifiers consistently reference the same {sample_sku['name']}.",
            "risk_factors": [] if confidence > 90 else ["Manual verification recommended"],
            "pattern_analysis": f"Detected consistent product patterns across {len([sample_sku['erp'], sample_sku['wms'], sample_sku['shopify']])} systems"
        }
    
    def calculate_business_score(self, company_key):
        """Business scoring with AI insights when available"""
        
        company = self.demo_companies[company_key]
        
        # Start with base score
        base_score = 50
        factors = []
        
        # Inventory velocity (40% weight)
        turns = company["inventory_turns"]
        if turns > 8:
            velocity_boost = 25
            factors.append(f"✅ Excellent inventory turns ({turns}x): +{velocity_boost}")
        elif turns > 4:
            velocity_boost = 15
            factors.append(f"✅ Good inventory turns ({turns}x): +{velocity_boost}")
        elif turns > 2:
            velocity_boost = 5
            factors.append(f"⚠️ Moderate inventory turns ({turns}x): +{velocity_boost}")
        else:
            velocity_boost = -15
            factors.append(f"❌ Slow inventory turns ({turns}x): {velocity_boost}")
        
        base_score += velocity_boost
        
        # Revenue size (20% weight)
        revenue = company["revenue"]
        if revenue > 5000000:
            revenue_boost = 15
            factors.append(f"✅ Large revenue (${revenue:,}): +{revenue_boost}")
        elif revenue > 1000000:
            revenue_boost = 10
            factors.append(f"✅ Good revenue (${revenue:,}): +{revenue_boost}")
        elif revenue < 500000:
            revenue_boost = -10
            factors.append(f"⚠️ Small revenue (${revenue:,}): {revenue_boost}")
        else:
            revenue_boost = 5
            factors.append(f"✅ Moderate revenue (${revenue:,}): +{revenue_boost}")
        
        base_score += revenue_boost
        
        # Industry risk (20% weight)
        industry_factors = {
            "Food & Beverage": (10, "Low risk, stable demand"),
            "Supplements": (5, "Moderate risk, growing market"),
            "Specialty Foods": (-5, "Higher risk, niche market"),
            "Beauty & Personal Care": (0, "Moderate risk, competitive")
        }
        
        industry_boost, industry_reason = industry_factors.get(company["industry"], (0, "Standard industry risk"))
        base_score += industry_boost
        factors.append(f"Industry ({company['industry']}): {'+' if industry_boost >= 0 else ''}{industry_boost} - {industry_reason}")
        
        # Experience factor (10% weight)
        years = company["years_operating"]
        if years > 5:
            experience_boost = 10
            factors.append(f"✅ Experienced operator ({years} years): +{experience_boost}")
        elif years > 2:
            experience_boost = 5
            factors.append(f"✅ Established business ({years} years): +{experience_boost}")
        else:
            experience_boost = -5
            factors.append(f"⚠️ Early stage ({years} years): {experience_boost}")
        
        base_score += experience_boost
        
        # AI insights (10% weight)
        ai_boost = self._get_ai_business_insights(company)
        base_score += ai_boost["adjustment"]
        factors.extend(ai_boost["factors"])
        
        final_score = max(0, min(100, base_score))
        
        return {
            "final_score": final_score,
            "factors": factors,
            "risk_category": self._get_risk_category(final_score),
            "recommended_rate": self._score_to_rate(final_score),
            "decision": self._get_decision(final_score),
            "ai_status": self.get_ai_status()
        }
    
    def _get_ai_business_insights(self, company):
        """AI-powered business insights when available"""
        
        if self.ai_enabled:
            try:
                # Get AI insights about the business
                insight_prompt = f"""
                Analyze this business profile and provide risk insights:
                Company: {company['name']}
                Industry: {company['industry']}
                Revenue: ${company['revenue']:,}
                Inventory Turns: {company['inventory_turns']}x
                Years Operating: {company['years_operating']}
                
                Provide a JSON response with:
                {{
                    "risk_adjustment": -10 to +10,
                    "key_insight": "one sentence insight"
                }}
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": insight_prompt}],
                    temperature=0.1,
                    max_tokens=100
                )
                
                ai_result = json.loads(response.choices[0].message.content)
                
                return {
                    "adjustment": ai_result.get("risk_adjustment", 0),
                    "factors": [f"🤖 AI Insight: {ai_result.get('key_insight', 'Analysis complete')}"]
                }
                
            except Exception as e:
                print(f"AI business insight failed: {e}")
                return self._get_fallback_business_insights(company)
        else:
            return self._get_fallback_business_insights(company)
    
    def _get_fallback_business_insights(self, company):
        """Fallback business insights"""
        if company["inventory_turns"] > 8:
            return {
                "adjustment": 10,
                "factors": ["🧠 Analysis: Strong operational efficiency indicators"]
            }
        elif company["inventory_turns"] < 3:
            return {
                "adjustment": -10,
                "factors": ["🧠 Analysis: Inventory management concerns detected"]
            }
        else:
            return {
                "adjustment": 0,
                "factors": ["🧠 Analysis: Standard operational patterns detected"]
            }
    
    def _get_risk_category(self, score):
        """Convert score to risk category"""
        if score >= 75:
            return "Low Risk"
        elif score >= 60:
            return "Medium Risk"
        elif score >= 45:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def _score_to_rate(self, score):
        """Convert score to interest rate"""
        if score >= 80:
            return 10.5
        elif score >= 70:
            return 12.5
        elif score >= 60:
            return 15.0
        elif score >= 50:
            return 17.5
        elif score >= 40:
            return 20.0
        else:
            return 22.0
    
    def _get_decision(self, score):
        """Get lending decision"""
        if score >= 60:
            return "APPROVED"
        elif score >= 45:
            return "APPROVED with conditions"
        elif score >= 30:
            return "REFER for manual review"
        else:
            return "DECLINED"
    
    def process_customer_upload(self, uploaded_data):
        """Process customer uploaded data for instant scoring"""
        try:
            revenue = uploaded_data.get("revenue", 1000000)
            inventory_turns = uploaded_data.get("inventory_turns", 4)
            industry = uploaded_data.get("industry", "General")
            years_operating = uploaded_data.get("years_operating", 2)
            
            base_score = 50
            
            # Apply scoring logic
            if inventory_turns > 8:
                base_score += 25
            elif inventory_turns > 4:
                base_score += 15
            elif inventory_turns < 2:
                base_score -= 15
            
            if revenue > 5000000:
                base_score += 15
            elif revenue > 1000000:
                base_score += 10
            elif revenue < 500000:
                base_score -= 10
            
            final_score = max(0, min(100, base_score))
            
            return {
                "score": final_score,
                "rate": self._score_to_rate(final_score),
                "decision": self._get_decision(final_score),
                "next_steps": "Contact us at cogaint.com to proceed",
                "ai_status": self.get_ai_status()
            }
            
        except Exception as e:
            return {
                "error": f"Processing failed: {str(e)}",
                "suggestion": "Please check your data format and try again"
            }

# Test function
if __name__ == "__main__":
    print("🧪 Testing Robust Demo Engine...")
    demo = CogaintLeanDemo()
    
    print(f"AI Status: {demo.get_ai_status()}")
    
    # Test scoring
    for company in list(demo.demo_companies.keys())[:1]:  # Test just one
        score_result = demo.calculate_business_score(company)
        print(f"✅ {company}: {score_result['final_score']}/100 → {score_result['recommended_rate']}%")
    
    print("🚀 Demo engine ready!")