from flask import Flask, request, render_template_string
import fitz
import os
from openai import OpenAI
import threading
import re
from flask_cors import CORS

client = OpenAI(
    api_key="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",
)

def get_string_between_backticks(text):
    pattern = r'```(.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return None

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text


def compare_pdfs_request(pdf1_path,pdf2_path):
 
    if not pdf1_path or not pdf2_path:
        return



   
    text1 = extract_text_from_pdf(pdf1_path)
    text2 = extract_text_from_pdf(pdf2_path)

    response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"""
Let's analyze and compare the fees charged by Service Provider 1 and Service Provider 2 based on the provided information. We need a thorough analysis that includes both the total fees and the fees as a percentage of the transaction amounts.

### Service Provider 1:
{text1}

### Service Provider 2:
{text2}
"""+"""
Make Sure Give response as html side by side comparison and use boxes to represent data and if data releted to credit or debits card use colorfull boxes to represent for each cards and also make sure show cards sub types.

make sure you use structure like this

```<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Service Provider Fee Comparison</title>
    <style>
        body {
            font-family: 'Georgia', serif;
            color: #333;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            display: flex;
            justify-content: space-between;
            padding: 20px;
            flex-wrap: wrap;
        }
        .box {
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            flex: 1 1 300px; /* Flex properties for responsiveness */
            max-width: 45%; /* Maximum width for larger screens */
            margin: 10px; /* Margin around boxes */
        }
        .card {
            margin-bottom: 20px;
            border-left: 5px solid #2196F3;
            padding-left: 10px;
        }
        .subtitle {
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 5px; /* Added margin at the bottom */
        }
        .header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        .card-types {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            gap: 5px;
            flex-wrap: wrap; /* Allow wrapping for smaller screens */
        }
        .card-types div {
            flex: 1 1 30%; /* Flex properties for card types */
            margin: 0 5px;
            padding: 10px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            min-width: 100px; /* Minimum width for card types */
        }
        .mastercard {
            background-color: #FFA500;
        }
        .amex {
            background-color: #1E90FF;
        }
        .visa {
            background-color: #32CD32;
        }
        pre {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap;
            margin: 10px 0; /* Added margin above and below */
        }

        @media (max-width: 768px) {
            .box {
                max-width: 100%; /* Full width on small screens */
                margin: 10px 0; /* Adjusted margin for small screens */
            }
            .card-types div {
                flex: 1 1 100%; /* Full width for card types on small screens */
                margin: 5px 0; /* Margin adjustments */
            }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="box">
        <div class="header">
            <div>Service Provider 1</div>
            <div>01/01/18 - 01/31/18</div>
        </div>

        <div class="subtitle">Total Fees Charged:</div>
        <div>$986.40</div>

        <div class="subtitle">Total Transaction Amounts:</div>
        <div>$39,024.95</div>

        <div class="subtitle">Fees as a Percentage of Transaction Amounts:</div>
        <div>2.53%</div>

        <div class="subtitle card">Card-Specific Fee Comparison:</div>
        <div class="card-types">
            <div class="mastercard">
                <div>Mastercard</div>
                <div>Fees Charged: $217.49</div>
                <div>Fees Percentage: 2.5%</div>
            </div>
            <div class="amex">
                <div>American Express</div>
                <div>Fees Charged: $270.79</div>
                <div>Fees Percentage: 2.5%</div>
            </div>
            <div class="visa">
                <div>Visa</div>
                <div>Fees Charged: $497.59</div>
                <div>Fees Percentage: 2.5%</div>
            </div>
        </div>

        <div class="subtitle">Average Ticket Amount:</div>
        <div>Mastercard: $966.65</div>
        <div>Amex: $2,084.31</div>
        <div>Visa: $947.79</div>

        <div class="subtitle">Adjustments/Chargebacks:</div>
        <div>None</div>
    </div>

    <div class="box">
        <div class="header">
            <div>Service Provider 2</div>
            <div>03/01/16 - 03/31/16</div>
        </div>

        <div class="subtitle">Total Fees Charged:</div>
        <div>$401.70</div>

        <div class="subtitle">Total Transaction Amounts:</div>
        <div>$12,267.59</div>

        <div class="subtitle">Fees as a Percentage of Transaction Amounts:</div>
        <div>3.27%</div>

        <div class="subtitle card">Card-Specific Fee Comparison:</div>
        <div class="card-types">
            <div class="mastercard">
                <div>Mastercard</div>
                <div>Fees Charged: $31.51</div>
                <div>Fees Percentage: 1.69%</div>
            </div>
            <div class="amex">
                <div>American Express</div>
                <div>Fees Charged: $145.20</div>
                <div>Fees Percentage: 2.89%</div>
            </div>
            <div class="visa">
                <div>Visa</div>
                <div>Fees Charged: $87.17</div>
                <div>Fees Percentage: 1.69%</div>
            </div>
        </div>

        <div class="subtitle">Average Ticket Amount:</div>
        <div>Mastercard: $29.59</div>
        <div>Amex: $45.26</div>
        <div>Visa: $32.04</div>

        <div class="subtitle">Adjustments/Chargebacks:</div>
        <div>None</div>
    </div>
</div>

<div class="container">
    <div class="box">
        <div class="subtitle">Line-by-Line Comparison:</div>
        <pre>
Fees Charged by Service Provider 1
  Mastercard: $217.49
  Amex: $270.79
  Visa: $497.59
  Total Fees: $986.40

Fees Charged by Service Provider 2
  Mastercard: $31.51
  Amex: $145.20
  Visa: $87.17
  Total Fees: $401.70
        </pre>
    </div>
    <div class="box">
        <div class="subtitle">Overall Analysis:</div>
        <div>
            Service Provider 1 has lower fees for Mastercard and Visa but higher overall fees and higher fees as a percentage of transaction amounts compared to Service Provider 2. Service Provider 2 has higher fees for American Express but overall lower fees for Mastercard and Visa.
        </div>
    </div>
</div>

</body>
</html>
```

Please provide the following detailed analysis:

1. Total Fees Charged:
   - Calculate the total fees charged by each service provider.
   - Formula: Total Fees = Sum of all fees

2. Total Transaction Amounts:
   - Calculate the total transaction amounts for each service provider.
   - Formula: Total Transaction Amounts = Sum of all transaction amounts

3. Fees as a Percentage of Transaction Amounts:
   - For each service provider, calculate the fees as a percentage of the total transaction amounts.
   - Formula: Fees Percentage = (Total Fees / Total Transaction Amounts) * 100

4. Card-Specific Fee Comparison:
   - For each card type (e.g., Visa, Mastercard, American Express), provide the fees charged by each service provider.
   - For each card type, calculate the fees as a percentage of the total transaction amounts for that card type.
   - Identify which service provider charges higher fees for each card type.
   - Provide the difference in fees for each card type and the percentage difference.
   - Formula: Fees Percentage by Card Type = (Total Fees for Card Type / Total Transaction Amounts for Card Type) * 100
   - Formula: Difference in Fees = Fees of Provider 1 - Fees of Provider 2
   - Formula: Percentage Difference = (Difference in Fees / Fees of Provider 2) * 100

5. Line-by-Line Comparison:
   - Provide a detailed, line-by-line comparison of all charges, including transaction fees, processing fees, service fees, chargebacks, and any other relevant fees.
   - Highlight the differences in charges for each line item.

6. Average Ticket Amount Comparison:
   - Compare the average ticket amounts for each card type.
   - Formula: Average Ticket Amount = Total Transaction Amounts for Card Type / Number of Transactions for Card Type

7. Adjustments/Chargebacks:
   - Compare any adjustments or chargebacks between the two service providers.

8. Overall Analysis:
   - Summarize which service provider has lower overall fees and lower fees as a percentage of transaction amounts.
   - Provide a detailed explanation of which provider is better based on your analysis, including a breakdown of all fee differences and percentage differences.

Make sure to include specific details for each card type and charge type to give a comprehensive comparison.
"""}



            ],
            max_tokens=2500
        )

    response = response.choices[0].message.content
    result =  get_string_between_backticks(response)
    return result
   

    


  


app = Flask(__name__)
CORS(app)

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

@app.route('/compare_pdfs', methods=['POST'])
def compare_pdfs():
    if 'pdf1' not in request.files or 'pdf2' not in request.files:
        return "Please upload both PDF files.", 400

    pdf1 = request.files['pdf1']
    pdf2 = request.files['pdf2']

    pdf1_path = f"./pdfs/{pdf1.filename}"
    pdf2_path = f"./pdfs/{pdf2.filename}"

    pdf1.save(pdf1_path)
    pdf2.save(pdf2_path)


    result = compare_pdfs_request(pdf1_path,pdf2_path)


    return render_template_string(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
