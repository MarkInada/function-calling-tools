import os
import requests
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

REDMINE_URL = os.environ["REDMINE_URL"]
REDMINE_PROJECT = os.environ["REDMINE_PROJECT"]
REDMINE_API_KEY = os.environ["REDMINE_API_KEY"]


def create_redmine_issue(issue_category, issue_title, due_date, issue_description):
    url = REDMINE_URL + "issues.json"
    headers = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": REDMINE_API_KEY
    }

    data = {
        "issue": {
            "project_id": REDMINE_PROJECT,
            "subject": "【" + issue_category + "】" + issue_title,
            "description": issue_description,
            # "tracker_id": tracker_id,
            "priority_id": 2,
            "due_date": due_date
            # "assigned_to_id": assigned_to_id
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    # find created issue url
    issue_id = response_data["issue"]["id"]
    created_issue_url = REDMINE_URL + "issues/" + str(issue_id)

    return response_data, created_issue_url


class RedmineIssueInput(BaseModel):
    issue_category: str = Field(description="issue category")
    issue_title: str = Field(description="issue title")
    due_date: str = Field(description="issue due date(YYYY-MM-DD)")
    issue_description: str = Field(description="issue description(markdown format)")


class RedmineInfo(BaseTool):
    name = 'create_redmine_issue'
    description = "Enter Redmine Issue information, including four arguments (category, title, due date (YYYY-MM-DD), and a summary description in Markdown format)."
    args_schema: Type[BaseModel] = RedmineIssueInput

    def _run(self, issue_category: str, issue_title: str, due_date: str, issue_description: str):
        return create_redmine_issue(issue_category, issue_title, due_date, issue_description)

    def _arun(self, ticker: str):
        raise NotImplementedError("get_stock_performance does not support async")
