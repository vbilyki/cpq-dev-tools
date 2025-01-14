# CPQ Dev Tools

This repository provides a collection of tools to interact with PandaDoc's CPQ API. These tools allow you to manage workflows, quotes, and rules efficiently.

## Getting Started

Follow these steps to set up and use the tools.

### 1. Prerequisites
- **Python 3.7+** installed on your computer.
- Basic understanding of command-line tools.
- Access to a PandaDoc account with CPQ features enabled.
- A Bearer Token (Private API key) for PandaDoc.

### 2. Setting Up the Environment
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd cpq-dev-tools
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Activate the virtual environment
   ```

3. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Your API Key**:
   Store your PandaDoc Bearer Token as an environment variable:
   ```bash
   export PANDADOC_API_KEY="your_bearer_token_here"
   ```

### 3. Using the Tools

#### Export Rules to a CSV File
This script fetches all rules for a specific quote and saves them into a CSV file.

1. Run the script:
   ```bash
   python3 examples/export_rules.py
   ```
2. Find the exported file in the project root directory as `exported_rules.csv`.

#### Import Rules from a CSV File
This script reads rules from a CSV file and imports them into a specified quote.

1. Ensure the file `exported_rules.csv` exists in the project root directory.
2. Run the script:
   ```bash
   python3 examples/import_rules.py
   ```
3. The rules will be added to the specified quote.

#### List All Rules for a Quote
This script retrieves and displays all rules for a specific quote in the console.

1. Run the script:
   ```bash
   python3 examples/list_rules.py
   ```

#### Delete All Rules from a Quote
This script deletes all rules from a specific quote.

1. Run the script:
   ```bash
   python3 examples/delete_rules.py
   ```

#### Generate Sample Rules
This script creates 50 sample rules for a quote, where the price equals the quantity.

1. Run the script:
   ```bash
   python3 examples/generate_rules.py
   ```

### 4. Troubleshooting

#### "PANDADOC_API_KEY environment variable is not set."
- Make sure you've exported your Bearer Token as an environment variable:
  ```bash
  export PANDADOC_API_KEY="your_bearer_token_here"
  ```

#### "Failed to fetch workflow."
- Verify that the `template_id` in the script is correct.
- Ensure your API key has access to the required PandaDoc resources.

#### "Quote with name '<quote_name>' not found."
- Confirm that the quote name matches the one in your workflow.
- Check the workflow template ID for accuracy.