from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ContactPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str
    source_url: str


class TeamMember(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    role: str
    linkedin_url: str | None
    source_url: str


class CompanyIntelligence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_overview: str = Field(
        description="A concise two-sentence overview of the company."
    )

    target_audience: str = Field(
        description="The company's primary target audience or ideal customer profile."
    )

    contact_points: list[ContactPoint] = Field(
        description="Public generic or business contact email addresses found on the website."
    )

    key_leadership: list[TeamMember] = Field(
        description="Key leaders or team members explicitly identified on the website."
    )

    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the extracted company intelligence, from 0.0 to 1.0."
    )

class LLMUsage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float

class ProcessingError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage: str
    error_type: str
    message: str


class CompanyResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    domain: str
    status: Literal["success", "failed"]
    intelligence: CompanyIntelligence | None
    usage: LLMUsage | None
    error: ProcessingError | None