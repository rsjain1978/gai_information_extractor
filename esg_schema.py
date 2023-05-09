from pydantic import BaseModel, Field, validator
from typing import List, Optional
from kor import from_pydantic

class ESGInformation(BaseModel):
    name: str = Field(
        description="The name of the company",
    )
    carbon_emission_target_year: Optional[str] = Field(
        description="Year by when carbon emission target would be met. Extract as a digit.",
    )
    carbon_emission_target: Optional[str] = Field(
        description="Any specific carbon emission targets that have been mentioned",
    )
    key_committements: Optional[str] = Field(
        description="Committments or goals which a company has setup for ESG governance",
    )
    policies: Optional[str] = Field(
        description="Goverment policies or companies internal policies for ESG",
    )
    environment: Optional[str] = Field(
        description="Environment related comment or statement",
    )    
    employees: Optional[str] = Field(
        description="Employees related comment or statement",
    )    
    fund: Optional[str] = Field(
        description="Investment product, mutual fund, Investment portfolio",
    )   
    aum: Optional[str] = Field(
        description="Assets under management in a fund or a portfolio",
    )  
    oversight: Optional[str] = Field(
        description="Oversight structure to monitor adoption",
    )  
    incentives: Optional[str] = Field(
        description="Incentives or benefits structure to promote adoption and oversight",
    )  
    key_speakers: Optional[str] = Field(
        description="Individuals or personalities who have been mentioned",
    )                 
    @validator("name")
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Name must not be empty")
        return v


schema, extraction_validator = from_pydantic(
    ESGInformation,
    description="Extract information about a company's esg information including their name, year, month and carbon_emission_target.",
    examples=[
        (            
            "[Tesla plans to cut down it's carbon emission to 10% by 2030]",
            {
                "name": "Tesla", 
                "carbon_emission_target": "10%", 
                "carbon_emission_target_year": "2030",
                "key_committements":"We will only invest in companies which have net zero carbon emission",
                "environment":"",
                "employees":"",
                "fund":"",
                "aum":"",
                "oversight":"",
                "incentives":"",
                "key_speakers":""                             
            }
        ),
        (            
            "[XYZ said it is working for gender equality in leadership roles]",
            {
                "name": "XYZ", 
                "carbon_emission_target": "", 
                "carbon_emission_target_year": "",
                "key_committements":"Working for gener equality in leadership roles",
                "environment":"",
                "employees":"Lack gender equality in leadership roles",
                "fund":"",
                "aum":"",
                "oversight":"",
                "incentives":"",
                "key_speakers":"" 
            }
        ),
        (            
            "[ABC manages $10million in it's ESG Investment portfolio]",
            {
                "name": "ABC", 
                "carbon_emission_target": "", 
                "carbon_emission_target_year": "",
                "key_committements":"",
                "environment":"",
                "employees":"",
                "fund":"ESG Investment portfolio",
                "aum":"$10million",
                "oversight":"",
                "incentives":"",
                "key_speakers":""                
            }
        ),
        (            
            "[We expect companies to have a robust corporate governance framework that can define longterm, innovative strategies and implement them for the benefit of all stakeholders. Vision and effective oversight are key to building a company with sustainable long-term success. . we believe that how management teams are paid plays a powerful role in creating value for our clients and ensuring equitable outcomes for a range of stakeholders. We promote clear, simple and well-designed remuneration structures that incentivise senior managers to deliver on company strategy while aligning with the interests of shareholders and other key stakeholders]",
            {          
                "name": "", 
                "carbon_emission_target": "", 
                "carbon_emission_target_year": "",
                "key_committements":"",
                "environment":"",
                "employees":"",
                "fund":"",
                "aum":"",
                "oversight":"We expect companies to have a robust corporate governance framework that can define longterm, innovative strategies and implement them for the benefit of all stakeholders",
                "incentives":"We promote clear,simple and well-designed remuneration structures that incentivise senior managers to deliver on company strategy",
                "key_speakers":""
            }
        )          
    ],
    many=True,
)
