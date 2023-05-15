from pydantic import BaseModel, Field, validator
from typing import List, Optional
from kor import from_pydantic

class ESGInformation(BaseModel):
    name: str = Field(
        description="The name of the company, stock, equity",
    )
    fair_value: Optional[str] = Field(
        description="Often expressed as the fair price at which the stock is a good buy.",
    )
    uncertainity: Optional[str] = Field(
        description="Any specific information which would indicate that their is uncertainity around the company's potential or future growth.",
    )
    consider_buy: Optional[str] = Field(
        description="price at which one could consider buying this stock",
    )
    consider_sell: Optional[str] = Field(
        description="price at which one could consider selling this stock",
    )
    bullish_views: Optional[str] = Field(
        description="Comments, views or opinions which suggest that the stock might a good buy at fair price",
    )
    bearish_views: Optional[str] = Field(
        description="Comments, views or opinions which suggest that the stock might be seeing or about see pricing pressures.",
    )
    macro_views: Optional[str] = Field(
        description="Comments, views or opinions about overall market or country or region in which the company is operating.",
    )    
    interesting_numbers: Optional[str] = Field(
        description="Sales, revenue, earning or performance numbers mentioned in the document about the company; capture along with the context they have been mentioned",
    )                        
    @validator("name")
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Name must not be empty")
        return v


schema, extraction_validator = from_pydantic(
    ESGInformation,
    description="Extract information about a company's esg information including their name, year, month and carbon_emission_target.",
    examples=[(            
            "[While the overall backdrop for Higher One is positive, the \
firm faces a few risks. Transaction processors and banks\
may compete directly with Higher One in the coming\
years, attracted by the company’s strong economic\
returns. Additionally, this upstart entrepreneurial venture\
faces operational and strategic challenges as it grows in\
size and maturity]",
            {
                "name": "Higher One", 
                "fair_value": "", 
                "uncertainity": "While the overall backdrop is positive, the \
firm faces a few risks",
                "consider_buy":"",
                "consider_sell":"",
                "bullish_views":"",
                "bearish_views":"",
                "macro_views":""                 
            }
        ),
        (            
            "[Higher One’s business model results in regularly recurring revenue in the \
            form of banking and software fees from the rather noncyclical higher education \
            market. Higher One generates attractive economic profits with 50%-plus returns \
            on invested capital expected for years to come. Higher One has increased sales \
            60%-80% in each of the past three years and is on pace for similar expansion \
            through the first quarter of 2010. \
            Intense competition looms from banks and technology firms, which could temper \
            returns and growth prospects. Higher One has a limited record as a large national \
            service provider. Like all upstart entrepreneurial ventures, Higher One will face \
            new operational and strategic challenges as its business grows]",            
            {
                "name": "", 
                "fair_value": "", 
                "uncertainity": "",
                "bullish_views":"Regularly recurring revenue, generates attractive economic profits ",
                "bearish_views":"Intense competition looms from banks and technology firms, which could temper \
                returns and growth prospects",
                "consider_buy":"",
                "consider_sell":"",
                "macro_views":""                                               
            }
        ),
        (            
            "[Consider Sell 50.00 USD Consider Buy 12.50 USD]",            
            {
                "name": "", 
                "fair_value": "", 
                "uncertainity": "",
                "bullish_views":"Regularly recurring revenue, generates attractive economic profits ",
                "bearish_views":"Intense competition looms from banks and technology firms, which could temper \
                returns and growth prospects",
                "consider_buy":"50.00 USD",
                "consider_sell":"12.50 USD",
                "macro_views":""                            
            }
        ),
(            
            "[As global light-vehicle demand recovers, we \
expect GM’s earnings to grow considerably, thanks to a\
dramatically lower cost base than old GM]",            
            {
                "name": "", 
                "fair_value": "", 
                "uncertainity": "",
                "bullish_views":"",
                "bearish_views":"",
                "consider_buy":"",
                "consider_sell":"",
                "macro_views":"As global light-vehicle demand recovers"                             
            }
        ),        
        (            
            "[Fair Value 25.00 USD]",            
            {
                "name": "", 
                "fair_value": "25.00 USD", 
                "uncertainity": "",
                "bullish_views":"",
                "bearish_views":"",
                "consider_buy":"",
                "consider_sell":"",
                "macro_views":""          
            }
        )],
    many=True,
)
