"""
CelebrateAI - Data Schemas & Validation Models
Includes strict type checking, field constraints, and input sanitization rules.
"""

import html
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator


class ColorSwatch(BaseModel):
    """Represents an aesthetic theme color swatch."""
    name: str = Field(..., min_length=1, max_length=50, description="Descriptive color name")
    hex: str = Field(..., pattern=r"^#[0-9a-fA-F]{6}$", description="Valid 6-digit hex code")


class EventIdeas(BaseModel):
    """Personalized theme, culinary, and atmospheric ideas."""
    themeTitle: str = Field(..., min_length=2, max_length=120)
    themeConcept: str = Field(..., min_length=10, max_length=1500)
    colorPalette: List[ColorSwatch] = Field(default_factory=list, max_length=10)
    signatureFoodAndDrinks: List[str] = Field(default_factory=list, max_length=15)
    activitiesAndEntertainment: List[str] = Field(default_factory=list, max_length=15)
    decorAndAtmosphere: List[str] = Field(default_factory=list, max_length=15)
    surpriseElements: List[str] = Field(default_factory=list, max_length=10)
    moodboardPrompt: str = Field(..., max_length=1000)


class BudgetItem(BaseModel):
    """Individual line-item in the event budget ledger."""
    id: str = Field(..., min_length=1, max_length=50)
    category: str = Field(..., min_length=1, max_length=60)
    item: str = Field(..., min_length=1, max_length=150)
    estimatedCost: float = Field(..., ge=0.0, le=100_000_000.0)
    actualCost: float = Field(default=0.0, ge=0.0, le=100_000_000.0)
    paidAmount: float = Field(default=0.0, ge=0.0, le=100_000_000.0)
    status: Literal['planned', 'booked', 'paid'] = Field(default='planned')
    notes: Optional[str] = Field(default="", max_length=500)


class TimelineMilestone(BaseModel):
    """Milestone checkpoint in the planning countdown roadmap."""
    id: str = Field(..., min_length=1, max_length=50)
    phase: str = Field(..., min_length=1, max_length=60)
    title: str = Field(..., min_length=1, max_length=150)
    description: str = Field(default="", max_length=1000)
    dueDate: Optional[str] = Field(default="", max_length=30)
    completed: bool = Field(default=False)
    category: str = Field(default="General", max_length=50)


class ScheduleItem(BaseModel):
    """Hour-by-hour cue in the day-of run of show."""
    id: str = Field(..., min_length=1, max_length=50)
    time: str = Field(..., min_length=1, max_length=30)
    activity: str = Field(..., min_length=1, max_length=150)
    location: Optional[str] = Field(default="", max_length=100)
    coordinator: Optional[str] = Field(default="", max_length=100)
    notes: Optional[str] = Field(default="", max_length=500)
    status: Literal['upcoming', 'ongoing', 'done'] = Field(default='upcoming')


class ChecklistTask(BaseModel):
    """Specific deliverable task assigned to a vendor."""
    id: str = Field(..., min_length=1, max_length=50)
    task: str = Field(..., min_length=1, max_length=200)
    completed: bool = Field(default=False)


class VendorItem(BaseModel):
    """Vendor record and relationship tracking entry."""
    id: str = Field(..., min_length=1, max_length=50)
    category: str = Field(..., min_length=1, max_length=60)
    vendorName: str = Field(..., min_length=1, max_length=120)
    contact: Optional[str] = Field(default="", max_length=200)
    estimatedCost: float = Field(default=0.0, ge=0.0, le=100_000_000.0)
    contractedCost: float = Field(default=0.0, ge=0.0, le=100_000_000.0)
    status: Literal[
        'researching', 'contacted', 'quoted', 'booked', 'completed'
    ] = Field(default='researching')
    checklist: List[ChecklistTask] = Field(default_factory=list, max_length=30)
    notes: Optional[str] = Field(default="", max_length=1000)


class EventPlan(BaseModel):
    """Comprehensive event blueprint schema."""
    id: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=2, max_length=150)
    eventType: Literal['wedding', 'birthday', 'community', 'other']
    date: Optional[str] = Field(default="", max_length=30)
    location: Optional[str] = Field(default="", max_length=150)
    guestCount: int = Field(default=150, ge=1, le=50000)
    currency: str = Field(default="INR", pattern=r"^[A-Z]{3}$")
    totalBudget: float = Field(default=500000.0, ge=1.0, le=100_000_000.0)
    vibeAndStyle: str = Field(default="", max_length=500)
    specialRequests: Optional[str] = Field(default="", max_length=2000)
    ideas: EventIdeas
    budgetBreakdown: List[BudgetItem] = Field(default_factory=list)
    timeline: List[TimelineMilestone] = Field(default_factory=list)
    dayOfSchedule: List[ScheduleItem] = Field(default_factory=list)
    vendorChecklist: List[VendorItem] = Field(default_factory=list)


class GeneratePlanRequest(BaseModel):
    """Validated request body for AI event plan synthesis."""
    eventType: Literal['wedding', 'birthday', 'community', 'other']
    title: Optional[str] = Field(default="", max_length=150)
    guestCount: int = Field(default=150, ge=1, le=50000)
    totalBudget: float = Field(default=500000.0, ge=1.0, le=100_000_000.0)
    currency: str = Field(default="INR", pattern=r"^[A-Z]{3}$")
    date: Optional[str] = Field(default="", max_length=30)
    location: Optional[str] = Field(default="", max_length=150)
    vibeAndStyle: str = Field(default="Chic, memorable, and well-organized", max_length=500)
    specialRequests: Optional[str] = Field(default="", max_length=2000)
    apiKey: Optional[str] = Field(default=None, max_length=200)

    @field_validator('title', 'location', 'vibeAndStyle', 'specialRequests')
    @classmethod
    def sanitize_strings(cls, v: Optional[str]) -> Optional[str]:
        """Sanitizes user string inputs against XSS and excessive whitespace."""
        if v:
            return html.escape(v.strip())
        return v


class ChatMessage(BaseModel):
    """Chat message schema for conversation history."""
    role: Literal['user', 'assistant']
    content: str = Field(..., min_length=1, max_length=5000)


class ChatRequest(BaseModel):
    """Interactive chat payload for EventGenie AI."""
    message: str = Field(..., min_length=1, max_length=2000)
    eventContext: Optional[dict] = None
    chatHistory: List[ChatMessage] = Field(default_factory=list, max_length=30)
    apiKey: Optional[str] = Field(default=None, max_length=200)

    @field_validator('message')
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        """Sanitizes user chat message against XSS and excessive whitespace."""
        return html.escape(v.strip())
