import argparse
import os
import re

import requests
from rich.console import Console
from rich.progress import track

COMMIT_SEARCH_URL = "https://api.github.com/search/commits?q={}"
DIFF_URL = "https://github.com/{}/commit/{}.diff"
REGEX = r"^(?=.*(?:{})).*"

console = Console()


def verbose_print(message: str):
    if is_verbose:
        console.print(message)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="A Simple POC of a web scraper to demonstrate careless use of GitHub"
    )

    parser.add_argument(
        "--query",
        "-q",
        nargs="+",
        default=["deleted .env", "delete .env", "hide .env"],
        type=str,
        help="A list of commit messages to search for",
    )

    parser.add_argument(
        "--terms",
        "-t",
        nargs="+",
        default=["mongodb"],
        type=str,
        help="A list of terms to search for in  the commits",
    )

    parser.add_argument("--output", "-o", help="Output files path")

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose mode"
    )

    args = parser.parse_args()

    output_dir: str | None = args.output
    queries: list[str] = args.query
    terms: list[str] = args.terms
    is_verbose: bool = args.verbose

    return (output_dir, queries, terms, is_verbose)


def query_commits(query: str, output_dir: str | None) -> list[str]:
    url = COMMIT_SEARCH_URL.format(query.replace(" ", "+"))
    verbose_print(f"searching: {url}")

    response = requests.get(url)

    if response.status_code != requests.codes.ok:
        verbose_print(f"Request failed with status code {response.status_code}")
        verbose_print(response.text)

        return []

    data = response.json()

    commits = list(map(extract_commit_details, data["items"]))

    commit_diffs = map(
        lambda commit: get_commit_diff(commit[0], commit[1], output_dir),
        track(
            commits,
            disable=is_verbose,
            description=f'Searching for "{query}"',
        ),
    )

    contents = [diff for diff in commit_diffs if diff is not None]

    console.print(f"Managed to grab {len(contents)} commits!\n")

    return contents


def get_commit_diff(repository: str, commit_hash: str, output_dir: str | None):
    url = DIFF_URL.format(repository, commit_hash)

    try:
        response = requests.get(url)
        response.raise_for_status()

        if output_dir is None:
            verbose_print(f"[+] found {url}")
        else:
            file_path = os.path.join(
                output_dir, f"{repository.replace('/', '_')}_{commit_hash}.txt"
            )

            if os.path.exists(file_path):
                verbose_print(f"[ ] found already existing {url}")
            else:
                with open(file_path, "w") as json_file:
                    json_file.write(response.text)

                verbose_print(f"[+] grabbed {url}")

        return response.text
    except:
        verbose_print(f"[!] couldn't reach {url}")


def extract_commit_details(item):
    repository = item["repository"]["full_name"]
    commit_hash = item["sha"]

    return repository, commit_hash


def search_terms_in_commit(content: str, terms: list[str]):
    lines = content.split("\n")

    return list(
        filter(lambda line: re.search(REGEX.format("|".join(terms)), line), lines)
    )


def main():
    output_dir, queries, terms, verbose_mode = parse_arguments()

    global is_verbose
    is_verbose = verbose_mode

    query_results = list(map(lambda query: query_commits(query, output_dir), queries))

    if terms is not None:
        for query_result in query_results:
            for commit in query_result:
                for term_match in search_terms_in_commit(commit, terms):
                    console.print(term_match, style="red bold")


if __name__ == "__main__":
    main()
