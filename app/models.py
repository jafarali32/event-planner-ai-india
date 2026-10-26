from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class ColorSwatch(BaseModel):
    name: str
    hex: str

class EventIdeas(BaseModel):
    themeTitle: str
    themeConcept: str
    colorPalette: List[ColorSwatch] = []
    signatureFoodAndDrinks: List[str] = []
    activitiesAndEntertainment: List[str] = []
    decorAndAtmosphere: List[str] = []
    surpriseElements: List[str] = []
    moodboardPrompt: str

class BudgetItem(BaseModel):
    id: str
    category: str
    item: str
    estimatedCost: float
    actualCost: float = 0.0
    paidAmount: float = 0.0
    status: Literal['planned', 'booked', 'paid'] = 'planned'
    notes: Optional[str] = ""

class TimelineMilestone(BaseModel):
    id: str
    phase: str  # e.g., '12 Months Out', '6 Months Out', '1 Month Out', 'Week Of', 'Day-Of'
    title: str
    description: str
    dueDate: Optional[str] = ""
    completed: bool = False
    category: str

class ScheduleItem(BaseModel):
    id: str
    time: str
    activity: str
    location: Optional[str] = ""
    coordinator: Optional[str] = ""
    notes: Optional[str] = ""
    status: Literal['upcoming', 'ongoing', 'done'] = 'upcoming'

class ChecklistTask(BaseModel):
    id: str
    task: str
    completed: bool = False

class VendorItem(BaseModel):
    id: str
    category: str
    vendorName: str
    contact: Optional[str] = ""
    estimatedCost: float = 0.0
    contractedCost: float = 0.0
    status: Literal['researching', 'contacted', 'quoted', 'booked', 'completed'] = 'researching'
    checklist: List[ChecklistTask] = []
    notes: Optional[str] = ""

class EventPlan(BaseModel):
    id: str
    title: str
    eventType: Literal['wedding', 'birthday', 'community', 'other']
    date: Optional[str] = ""
    location: Optional[str] = ""
    guestCount: int = 50
    currency: str = "USD"
    totalBudget: float = 5000.0
    vibeAndStyle: str = ""
    specialRequests: Optional[str] = ""
    ideas: EventIdeas
    budgetBreakdown: List[BudgetItem] = []
    timeline: List[TimelineMilestone] = []
    dayOfSchedule: List[ScheduleItem] = []
    vendorChecklist: List[VendorItem] = []

class GeneratePlanRequest(BaseModel):
    eventType: Literal['wedding', 'birthday', 'community', 'other']
    title: Optional[str] = ""
    guestCount: int = 75
    totalBudget: float = 10000.0
    currency: str = "USD"
    date: Optional[str] = ""
    location: Optional[str] = ""
    vibeAndStyle: str = "Chic, memorable, relaxed yet organized"
    specialRequests: Optional[str] = ""
    apiKey: Optional[str] = None

class ChatMessage(BaseModel):
    role: Literal['user', 'assistant']
    content: str

class ChatRequest(BaseModel):
    message: str
    eventContext: Optional[dict] = None
    chatHistory: List[ChatMessage] = []
    apiKey: Optional[str] = None

class BudgetOptimizeRequest(BaseModel):
    eventPlan: EventPlan
    targetBudget: float
    apiKey: Optional[str] = None
