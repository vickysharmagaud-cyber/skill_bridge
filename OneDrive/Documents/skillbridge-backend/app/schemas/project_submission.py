from pydantic import BaseModel


class ProjectSubmissionCreate(BaseModel):
    project_id: int
    github_url: str | None = None
    submission_text: str | None = None