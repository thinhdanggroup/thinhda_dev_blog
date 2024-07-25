import os
import re
import openai
import tiktoken
import pandas as pd
import html2text
from logger import logger
from atlassian import Confluence
from bs4 import BeautifulSoup
from typing import List
from math import ceil
from io import StringIO

# ------------- Shared variables ------------- #
from models import ConfluencePage
from llm import count_tokens

# ------------------ Config ------------------ #
from dotenv import load_dotenv

load_dotenv()
confluence_url = os.environ.get("CONFLUENCE_URL")
confluence_username = os.environ.get("CONFLUENCE_USERNAME")
confluence_api_token = os.environ.get("CONFLUENCE_API_TOKEN")

# Config for splitting large pages
max_tokens_per_page = 500
max_characters_per_page = (
    max_tokens_per_page * 3.3
)  # One word consists of 3.3 tokens on average
min_characters_per_page = max_characters_per_page / 3
max_rows_per_table = 20
marker = "\n##"


class SourceCollector:
    def __init__(
        self,
        root_folder: str = "tmp",
        limit: int = 0,
    ):
        self.total_records = 0
        self.root_folder = root_folder
        self.limit = limit
        self.counter = 0
        self.cache_id_name = {}
        self.indexing = {}
        self.parent_and_children = {}

        if not os.path.exists(root_folder):
            os.makedirs(root_folder)

    def replace_structured_macros(self, html: str) -> str:
        soup = BeautifulSoup(html, features="html.parser")

        for tag in soup.find_all("ac:structured-macro"):

            if tag.get("ac:name") == "code":
                code = soup.new_tag("code")
                code.string = tag.get_text()
                tag.replace_with(code)

        return soup.prettify(formatter=None)

    def split_table(self, table_df):

        result_dfs = []

        # Split into chunks
        runs = ceil(len(table_df) / max_rows_per_table)

        for i in range(0, len(table_df), max_rows_per_table):
            chunk = table_df[i : i + max_rows_per_table]
            result_dfs.append(chunk)

        return result_dfs

    def replace_table(self, match: re.Match):

        table_html = match.group(0)
        table_html_io = StringIO(table_html)
        pandas_tables = pd.read_html(table_html_io, header=0)
        table_df = pandas_tables[0]
        table_text = ""

        # Split big tables
        if len(table_df) > max_rows_per_table:
            table_dfs = self.split_table(table_df)

            for table_df in table_dfs:
                # Insert markdown headline before table als marker
                # which will be used to split large pages into smaller chunks
                table_text += (
                    "\n" + marker + table_df.to_markdown(tablefmt="jira", index=False)
                )

        else:
            table_text += (
                marker
                + " Tabelle:\n"
                + table_df.to_markdown(tablefmt="jira", index=False)
            )

        # Replace multiple blanks
        table_text = re.sub(r" {2,}", " ", table_text, flags=re.DOTALL)

        return table_text

    # def split_string_by_markers(
    #     self, input_string: str, marker: str, min_chunk_size: int, max_chunk_size: int
    # ) -> List:

    #     result = []
    #     current_chunk = ""

    #     splits = input_string.split(marker)

    #     for split in splits:

    #         # Füge Split zu aktuellem Chunk hinzu, wenn wir dadurch innerhalb der Obergrenze bleiben
    #         if len(current_chunk) + len(split) + len(marker) <= max_chunk_size:
    #             current_chunk += split + marker

    #         # Obergrenze würde durch Hinzufügen des Splitz gesprengt
    #         else:
    #             # Wenn vor Hinzufügen Mindestgrenze erreicht ist, beende aktuellen Chunk und
    #             # starte mit neuem Chunk mit aktuellem Split darin
    #             if len(current_chunk) >= min_chunk_size:
    #                 result.append(current_chunk[:-3])
    #                 current_chunk = split + marker

    #             # Wenn du dich entscheiden musst zwischen nicht erreichter Mindestgröße
    #             # und gesprengter Obergrenze, opfere im Zweifel die Obergrenze
    #             else:
    #                 current_chunk += split + marker
    #                 result.append(current_chunk[:-3])
    #                 current_chunk = ""

    #     if current_chunk:
    #         result.append(current_chunk[:-3])

    #     return result

    # ----------------- Functions ---------------- #
    def connect_to_confluence(self) -> Confluence:
        url = confluence_url
        username = confluence_username
        api_token = confluence_api_token

        confluence = Confluence(
            url=url, username=username, password=api_token, cloud=True
        )

        return confluence

    def get_confluence_pages(self, space: str) -> list:

        confluence = self.connect_to_confluence()

        # There is a limit of how many pages we can retrieve one at a time.
        # So we retrieve 100 at a time and loop until we know we retrieved all of them.
        keep_going = True
        start = 0
        limit = 100

        pages = []

        while keep_going:
            results = confluence.get_all_pages_from_space(
                space,
                start=start,
                limit=100,
                status=None,
                expand="body.storage",
                content_type="page",
            )

            pages.extend(results)

            logger.info(f"Fetched {len(pages)} pages from Confluence")

            # TODO: process new page
            self.process_new_pages(space, results)

            if len(results) < limit:
                keep_going = False
            else:
                start = start + limit
                # TODO: remove this
                # keep_going = False

        return pages

    def process_new_pages(self, space, pages):
        pages = self.filter_pages(pages)
        logger.info(str(len(pages)) + " pages after filtering")

        for page in pages:
            id = page["id"]
            title = page["title"]
            link = confluence_url + "wiki/spaces/" + space + "/pages/" + page["id"]
            # body = self.transform_html_to_text(page["body"]["storage"]["value"])
            # page_content = "\n*" + title + "*\n" + body  # markdown for <h1>

            # Add to list
            page_data = ConfluencePage(
                id=id,
                space=space,
                title=title,
                page_content=link,
                link=link,
                num_tokens=0,
            )

            self.export_page(page_data)

    def filter_pages(self, pages: list) -> list:

        date_pattern = r"\d{4}-\d{2}-\d{2}"

        # Exclude pages without content
        condition1 = lambda page: len(page["body"]["storage"]["value"]) > 0

        # Exclude meeting notes (incl. retros) containing a date like "02-23-2023"
        condition2 = lambda page: not re.match(date_pattern, page["title"])

        # ToDo: Exclude pages with "archiv" in path

        allowed_pages = [
            page for page in pages if condition1(page) and condition2(page)
        ]

        return allowed_pages

    def export_page(
        self, page: ConfluencePage, insert: bool = True
    ) -> List[ConfluencePage]:
        if self.counter >= self.limit and self.limit > 0:
            print("Limit reached")
            return
        # export page to markdown
        file_name = f"{self.root_folder}/{page.title.replace('/','-')}.pdf"

        if os.path.exists(file_name):
            print(f"File {file_name} already exists")
            return

        confluence = self.connect_to_confluence()
        print("Exporting page " + page.title)
        try:
            pagePdf = confluence.export_page(page.id)
        except Exception as e:
            print("Error exporting page " + page.title, e)
            return
        print("Exported page " + page.title)

        with open(file_name, "wb") as file:
            file.write(pagePdf)
        self.counter += 1

    def transform_html_to_text(self, html):

        # html2text does not understand confluence's macro-tags
        # Convert them to corresponding standard tags
        if "<ac:structured-macro" in html:
            html = self.replace_structured_macros(html)

        # Convert HTML to text
        # html2text does not excell in rendering tables, so bypass them for now
        text_maker = html2text.HTML2Text()
        text_maker.bypass_tables = True
        text_maker.body_width = 500
        text = text_maker.handle(html)

        # Convert tables
        pattern = r"<table>.*?</table>"
        matches = re.findall(pattern, text, flags=re.DOTALL)
        text = re.sub(pattern, self.replace_table, text, flags=re.DOTALL)

        # Remove newlines containing only blanks
        text = re.sub(r"^$\n", "", text, flags=re.MULTILINE)

        # Remove more than two newlines in a row
        text = re.sub(r"\n\s+", "\n\n", text, flags=re.MULTILINE)

        return text

    def collect_data_from_confluence(self, space: str, insert: bool = True) -> List:

        # Get pages from Confluence space
        pages = self.get_confluence_pages(space)
        logger.info(str(len(pages)) + " pages collected from space " + space)
        return pages

    def process_parent_page(self, space: str, page_id: str):
        confluence = self.connect_to_confluence()
        keep_going = True
        start = 0
        limit = 100

        pages = []

        while keep_going:
            print(
                f"Fetching page {start} to {start+limit} space {space} page {page_id}"
            )
            results = confluence.get_page_child_by_type(
                page_id=page_id,
                start=start,
                limit=100,
                expand="body.storage",
                type="page",
            )

            pages.extend(results)

            logger.info(f"Fetched {len(pages)} pages from Confluence")

            self.process_new_pages(space, results)

            if len(results) < limit:
                keep_going = False
            else:
                start = start + limit

        for page in pages:
            if page_id not in self.parent_and_children:
                self.parent_and_children[page_id] = []
            self.parent_and_children[page_id].append(page["id"])

            self.cache_id_name[page["id"]] = page["title"].replace("/", "-")
            self.process_parent_page(space, page["id"])

        return pages

    # ------------------- Main ------------------- #
    def run(
        self, confluence_spaces: list = [], parent_pages: List[str] = []
    ) -> pd.DataFrame:
        for space in confluence_spaces:
            # Collect and transform data from confluence
            confluence_pages = self.collect_data_from_confluence(space)
            logger.info(
                str(len(confluence_pages)) + " pages collected from space " + space
            )

    def run_from_parent_page(self, space: str, parent_pages: List[str]):
        for page in parent_pages:
            self.process_parent_page(space, page)

    def get_title(title: str) -> str:
        return title.replace("/", "-")

    def build_index_recursive(self, parent, markdown):
        if (
            parent not in self.parent_and_children
            or len(self.parent_and_children[parent]) == 0
        ):
            return markdown

        if parent not in self.cache_id_name:
            markdown += f"\n*[{parent}]*\n"
        else:
            title = self.cache_id_name[parent].replace(" ", "\ ")
            markdown += f"\n*[{title}]*\n"

        children = self.parent_and_children.get(parent, [])
        for child in children:
            title = self.cache_id_name[child].replace(" ", "&#32;")
            markdown += f"  - [{title}](./{title}.pdf)\n"
            markdown = self.build_index_recursive(child, markdown)

        self.parent_and_children[parent] = ""
        return markdown

    def build_index(self) -> str:
        markdown = ""
        for parent in self.parent_and_children.keys():
            markdown = self.build_index_recursive(parent, markdown)
        return markdown


if __name__ == "__main__":
    config = {
        "folder": "./tmp/financial",
        "space": "FT",
        "page": "",
    }
    source_collector = SourceCollector(root_folder=config["folder"], limit=0)
    # source_collector.run(["~712020b2523477db2449d488573ca22cf8cf0e"])
    if config["page"] == "":
        source_collector.run([config["space"]])
    else:
        source_collector.run_from_parent_page(
            space=config["space"], parent_pages=[config["page"]]
        )
    with open(f"{config['folder']}/index.md", "w") as file:
        file.write(source_collector.build_index())
    print("Done")
