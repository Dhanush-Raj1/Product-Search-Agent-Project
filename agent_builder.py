import os
from exception import CustomException

from agno.agent import Agent, RunResponse
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.exa import ExaTools
from agno.tools.serpapi import SerpApiTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.baidusearch import BaiduSearchTools
from agno.models.openrouter import OpenRouter
from agno.models.google import Gemini

from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
Together_api= os.getenv("TOGETHER_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
EXA_API_KEY= os.getenv("EXA_API_KEY")
SERP_API_KEY= os.getenv("SERP_API_KEY")


@dataclass
class ProductAgent: 
    """
    Build a product search agent 
    and returns the findings from the agent
    """
    def build_agent(self)->Agent:
        try:
            #llm_model = Together(id="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",  #meta-llama/Llama-3.3-70B-Instruct-Turbo-Free
                        #api_key=Together_api)                                          #deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free
            
            llm_model = Gemini(id="gemini-2.5-flash-lite",
                               api_key=GOOGLE_API_KEY,
                               temperature=0.1,
                               max_output_tokens=2048,) 
            
            #llm_model = OpenRouter(id="meta-llama/llama-4-maverick:free")      

            web_search_agent = Agent(
                name="Product search agent",
                role="Search the web for price related information of various products and represent the findings.",
                model=llm_model,
                tools=[
                    DuckDuckGoTools(), 
                    # ExaTools(include_domains=[
                    #     "amazon.in", "flipkart.com", "indiamart.com", "snapdeal.com", "myntra.com", "pricehistory.in", "pricebefore.com"
                    #     ]),
                    SerpApiTools(api_key=SERP_API_KEY),
                    #GoogleSearchTools(),
                    BaiduSearchTools(), 
                ],
                description=[
                    "You are a product search expert that finds CURRENT and VERIFIED pricing information."
                ],
                instructions="""
                    YOU MUST FOLLOW THIS EXACT SEQUENCE - DO NOT SKIP ANY STEP:
    
                    Step 1: Use DuckDuckGoTools to search for the product
                    Step 2: Use SerpApiTools to search for the same product
                    Step 3: Use GoogleSearchTools to search for the same product
                    Step 4: Use BaiduSearchTools to search for the same product
                    Step 5: ONLY AFTER completing all searches, compile the results

                    MANDATORY RULES:
                    - You MUST call DuckDuckGoTools at least once
                    - You MUST call SerpApiTools at least once  
                    - You MUST call GoogleSearchTools at least once
                    - You MUST call BaiduSearchTools at least once
                    - Each tool must search on amazon.in, flipkart.com, and indiamart.com and other relevant sites, sellers as well
                    - Do NOT skip any tool even if you think you have enough information
                    - All four tools MUST be executed before providing final response

                    Instructions:
                        1. Search Instructions:
                            - For each product, construct specific search queries like:
                              * "{product name} price in amazon.in"
                              * "{product name} price in flipkart.com"
                              * "{product name} price in indiamart.com"
                              * "{product name} price in snapdeal.com"
                              * "{product name} price in myntra.com"
                              * "{product name} price in zeptonow.com"
                            - Search for multiple variations (different sizes, colors, editions)
                            - Look for current deals, discounts, and offers
                            - Check both product listings and price comparison sites

                        2. Price Extraction:
                            - Extract EXACT prices with currency symbols (₹)
                            - Note the specific variant (size, color, edition, etc.)
                            - Capture any discounts or offers (e.g., "50% off", "₹500 coupon")
                            - Check for shipping costs - mention if free shipping
                            - Note stock availability

                        3. Search Scope:
                            - Check in the following website: 
                                - amazon.in, 
                                - flipkart.com, 
                                - indiamart.com
                                - snapdeal.com, 
                                - myntra.com (for specific categories)
                            - Also check in pricehistory.in, pricebefore.com for price trends
                            - Check other potential sellers from the internet search results

                        4. Verification:
                            - Cross-verify prices from multiple search results
                            - Check product authenticity (official seller vs third-party)
                            - Note seller ratings and reviews if available
                            - Mention warranty information
                        
                    CRITICAL: YOU MUST PROVIDE ACCURATE, EXACT PRICES FOUND DURING THE SEARCHES. 
                    VERY CRITICAL: CHECK FOR LATEST PRICES, DO NOT PROVIDE OUTDATED INFORMATION. CHECK ONLY IN LATEST SEARCH RESULTS. 

                    GEOGRAPHIC RESTRICTION - CRITICAL REQUIREMENT:
                    - ALL searches MUST be restricted to INDIA (.in domains)
                    - ONLY search for products available in INDIA
                    - Use search queries with these modifiers:
                        * "site:amazon.in {product}"
                        * "site:flipkart.com {product}"
                        * "{product} price India INR"
                        * "{product} buy India"
                    - REJECT any results from amazon.com, amazon.co.uk, ebay.com, walmart.com
                    - ONLY accept results showing prices in ₹ (Indian Rupees)
                    - If you find prices in $, £, €, or other currencies, IGNORE them             
                """,
                goal="Retrieve information from online sources and represent the findings.",
                expected_output="""
                    ## Product Information:
                        - Product Name and exact specifications
                        - Category and brand
                        - Available variants (if any)
                
                    ## Price Comparison Table:
                        ### Amazon.in
                            - Price: 
                                - ₹XXX for [Variant 1]
                                - ₹XXX for [Variant 2]
                                - ₹XXX for [Variant n]
                            [NOTE: Include the price for each variant found, if no variants, just list the single price]
                            - Discounts/Offers: [Details]
                            - Shipping Cost: [₹XXX or Free]
                            - Stock Availability: [In Stock/Out of Stock]
                            - Seller: [Official/Third-party, Rating if available]

                        ### Flipkart.com
                            - Price: 
                                - ₹XXX for [Variant 1]
                                - ₹XXX for [Variant 2]
                                - ₹XXX for [Variant n]
                            [NOTE: Include the price for each variant found, if no variants, just list the single price]
                            - Discounts/Offers: [Details]
                            - Shipping Cost: [₹XXX or Free]
                            - Stock Availability: [In Stock/Out of Stock]
                            - Seller: [Official/Third-party, Rating if available]

                        ### IndiaMART.com
                            - Price: 
                                - ₹XXX for [Variant 1]
                                - ₹XXX for [Variant 2]
                                - ₹XXX for [Variant n]
                            [NOTE: Include the price for each variant found, if no variants, just list the single price]
                            - Discounts/Offers: [Details]
                            - Shipping Cost: [₹XXX or Free]
                            - Stock Availability: [In Stock/Out of Stock]
                            - Seller: [Official/Third-party, Rating if available]

                        ### Snapdeal.com
                            - Price: 
                                - ₹XXX for [Variant 1]
                                - ₹XXX for [Variant 2]
                                - ₹XXX for [Variant n]
                            [NOTE: Include the price for each variant found, if no variants, just list the single price]
                            - Discounts/Offers: [Details]
                            - Shipping Cost: [₹XXX or Free]
                            - Stock Availability: [In Stock/Out of Stock]
                            - Seller: [Official/Third-party, Rating if available]

                        ### Myntra.com
                            - Price: 
                                - ₹XXX for [Variant 1]
                                - ₹XXX for [Variant 2]
                                - ₹XXX for [Variant n]
                            [NOTE: Include the price for each variant found, if no variants, just list the single price]
                            - Discounts/Offers: [Details]
                            - Shipping Cost: [₹XXX or Free]
                            - Stock Availability: [In Stock/Out of Stock]
                            - Seller: [Official/Third-party, Rating if available]

                        ### Other Sellers [NOTE: List any other sellers if any, Enter the name of other sellers/websites if found]
                            - Price: 
                                - ₹XXX for [Variant 1]
                                - ₹XXX for [Variant 2]
                                - ₹XXX for [Variant n]
                            [NOTE: Include the price for each variant found, if no variants, just list the single price]
                            - Discounts/Offers: [Details]
                            - Shipping Cost: [₹XXX or Free]
                            - Stock Availability: [In Stock/Out of Stock]
                            - Seller: [Official/Third-party, Rating if available]

                    ## Best Deals:
                        - **Lowest Price**: ₹XXX on [Website] for [Variant]
                        - **Best Value**: ₹XXX on [Website] (considering shipping + quality)
                        - **Current Offers**: List any active discount codes or cashback
                        
                    ## Money-Saving Tips:
                        - **Price Summary**: Summarize Price difference between variants across different platforms
                        - **Deal Highlights**: Highlight any exclusive deals or bundles
                        - **Alternative Options**: Alternative products with similar features
                
                    ## Sources: 
                           - Mention the Links 
                    [CRITICAL: Mention the direct clickable links to each product page]

                """,
                tool_call_limit=20,
                #reasoning=True,
                structured_outputs=True,
                show_tool_calls=True,
                markdown=True      
            )

            return web_search_agent
        except Exception as e:
            raise CustomException(e)
    
    def perform_task(self, task: str)->str:
        try:
            agent = self.build_agent()
            response: RunResponse = agent.run(task)
            #response = agent.print_response(task, stream=True)
            return response
        except Exception as e:
            raise CustomException(e)