import os
from exception import CustomException

from agno.agent import Agent, RunResponse
from agno.tools.exa import ExaTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.serpapi import SerpApiTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.together import Together

from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

Together_api= os.getenv("TOGETHER_API_KEY")
os.environ["EXA_API_KEY"] = os.getenv("EXA_API_KEY")


@dataclass
class ProductAgent: 
    """
    Build a product search agent 
    and returns the findings from the agent
    """
    def build_agent(self)->Agent:
        try:
            llm_model = Together(id="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",  #meta-llama/Llama-3.3-70B-Instruct-Turbo-Free
                        api_key=Together_api)                                          #deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free
            
            web_search_agent = Agent(
                name="Product search agent",
                role="Search the web for product information and represent the findings.",
                model=llm_model,
                tools=[
                    #DuckDuckGoTools(), 
                    ExaTools(include_domains=["https://www.amazon.in/", "https://www.flipkart.com/", "https://www.indiamart.com/"]), 
                    SerpApiTools(api_key=os.getenv("SERPAPI_API_KEY")),
                    GoogleSearchTools(),
                ],
                description=["You are a product search expert capable of finding relevant information from the web related to various products."],
                instructions="""
                    1. Search Instructions:
                        - You MUST use ALL available tools: DuckDuckGoTools, ExaTools, SerpApiTools, GoogleSearchTools.
                        - Utilize all the tools to find the most relevant information.
                        - Retrieve relevant links and summarize insights from web pages.
                        - Prioritize official sources, product websites, and reputable reviews. 
                        - Summarize the findings from all the tools used.

                    2. Price Retrieval:
                        - Extract product prices from different sources.
                        - Convert prices to INR if in other currencies.

                    3. Search Scope:
                        - Websites to search: amazon.in, flipkart.in. indiamart.com

                    4. Formatting:
                        - You must display the information in bullet points as a list especially the prices 
                        - Structure responses using markdown.
                        - Provide a final summary and best price recommendations.

                    IMPORTANT NOTE: USE ALL THE TOOLS MENTIONED IN THE AGENT.
                    IMPORTANT NOTE: SEARCH THROUGH VARIOUS ECOMMERCE WEBSITES MENTIONED IN SEARCH SCOPE.
                    IMPORTANT NOTE: CONVERT THE PRICES TO INR IF IN OTHER CURRENCIES.
                    IMORTANT NOTE: DISPLAY THE INFORMATION IN BULLET POINTS AS A LIST.
                    IMPORTNAT NOTE: DO NOT DISPLAY YOUR REASONING IN THE RESPONSE.
                """,
                goal="Retrieve information from online sources and represent the findings.",
                expected_output="""
                    ## Product Information:
                        - Mention the product information
                        - Mention the main aim of the report

                    ## Price Comparison:
                        - List down the prices of the product from different websites. 
                        - DISPLAY THE PRICE INFORMATION IN BULLET POINTS AS A LIST.
                        - Differentiate between the prices for different types of the product, 
                            For Examples : books can be categoried into paperback, hardcover, kindle etc...
                        - Compare between the prices of the product from different websites.
                        - Mention the prices of the product in INR.

                    ## Final Summary:
                        - Mention the prices from different websites.
                        - Differentiate between the prices for different types of the product.
                        - Mention the best price available.
                        - Mention the best website to buy the product.

                    ## Sources: 
                        - Include the sources of your findings. 
                        - Mention links to the sources of your findings.
                        - Include the links to the websites from where the information is retrieved.
                """,
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



