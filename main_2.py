import os
import json
from datetime import datetime
from typing import List ,Optional
import PyPDF2
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from markdown2 import markdown
import os

# from weasyprint import HTML


def load_file(path):
    with open(path , 'rb') as f:
        reader =PyPDF2.PdfReader(f)
        seperator=""
        return seperator.join(page.extract_text() or seperator for page in reader.pages)        

text=load_file('file.pdf')
class Annual_Report(BaseModel):
    company_name: str = Field(..., description="The name of the company as reported in the 10-K")
    cik: str = Field(..., description="Central Index Key (CIK) identifier assigned by the SEC")
    fiscal_year_end: datetime = Field(..., description="Fiscal year end date")
    filing_date: datetime = Field(..., description="Date when the 10-K was filed with the SEC")
    total_revenue: Optional[float] = Field(None, description="Total revenue for the fiscal year (in USD)")
    net_income: Optional[float] = Field(None, description="Net income (profit) for the fiscal year (in USD)")
    total_assets: Optional[float] = Field(None, description="Total assets at fiscal year end (in USD)")
    total_liabilities: Optional[float] = Field(None, description="Total liabilities at fiscal year end (in USD)")
    operating_cash_flow: Optional[float] = Field(None, description="Net cash provided by operating activities (in USD)")
    cash_and_equivalents: Optional[float] = Field(None, description="Cash and cash equivalents at fiscal year end (in USD)")
    num_employees: Optional[int] = Field(None, description="Number of employees reported")
    auditor: Optional[str] = Field(None, description="Name of the external auditor")
    business_description: Optional[str] = Field(None, description="Companys business overview (Item 1)")
    risk_factors: Optional[List[str]] = Field(None, description="Key risk factors (Item 1A)")
    management_discussion: Optional[List[str]] = Field(None, description="Managements Discussion & Analysis (Item 7)")


client =genai.Client(api_key='')

schema_definition = json.dumps(Annual_Report.model_json_schema(), indent=2, ensure_ascii=False)
prompt=f'Analyze the report and fill data model baed on it:\n\n{text}\n\n '
prompt+=f'the output must be in the specific format data format: \n\n{schema_definition}\n\n no extra field required'

# response =client.models.generate_content(

#     model='gemini-2.0-Pro' ,
#     contents=prompt,
#     config={
#         'reponse_mime_type' : 'application/json', 
#         'reponse_schema' : Annual_Report
#     }
# )
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt
)
# print(response.text)
ar= Annual_Report.model_validate_json(response.text)
print(ar)