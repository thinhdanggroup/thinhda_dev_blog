from pydantic import BaseModel


class SourceDocument(BaseModel):
    content: str
    url: str


class ConfluencePage(BaseModel):
    id: int = 0
    space: str = ""
    title: str
    page_content: str
    link: str
    num_tokens: int
