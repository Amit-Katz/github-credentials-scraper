# Web Scraper for GitHub Commits

This Python script is a Proof of Concept (POC) for a web scraper designed to demonstrate the potential risks of careless use of GitHub. It allows you to search for commits containing sensitive credentials in public GitHub repositories.

## Usage

Before using this script, make sure you have Python installed on your system.

### Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/Amit-Katz/github-credentials-scraper.git
cd github-credentials-scraper
```

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Command Line Arguments

The script accepts the following command-line arguments:

- `--query`, `-q` (optional): A list of commit messages to search for. The default queries are ["deleted .env", "delete .env", "hide .env"].

- `--terms`, `-t` (optional): A list of terms to search for in the commit messages. The default term is "mongodb".

- `--output`, `-o` (optional): Path to the output directory where the results will be saved.

- `--verbose`, `-v` (optional): Enable verbose mode for more detailed output.

### Examples

#### Basic Usage

To search for the default commit messages and terms, simply run:

```bash
python scraper.py
```

#### Custom Queries and Terms

You can specify custom queries and terms using the `--query` and `--terms` options. For example:

```bash
python scraper.py --query "add secret key" "remove password" --terms "api_key" "password"
```

#### Saving Results to a directory

To save the results to a directory, use the `--output` option:

```bash
python scraper.py --output results
```

#### Verbose Mode

Enable verbose mode to see detailed output:

```bash
python scraper.py --verbose
```

## Disclaimer

This script is intended for educational purposes only and should not be used to violate GitHub's terms of service or any applicable laws. Always obtain proper authorization before scraping or accessing any website or service.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
