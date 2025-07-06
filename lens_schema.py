from pydantic import BaseModel, EmailStr
from typing import List, Optional

class LensRequest(BaseModel):
    name: str
    age: int
    contactNumber: str
    emailID: EmailStr
    usesGlassesOrContacts: str
    consultationFrequency: str
    symptoms: Optional[List[str]]
    sleepHours: float
    hydrationFrequency: str
    screenTime: str
    screenBreakTime: int
    isScreenDarkMode: str
    screenBrightness: str
    readingTime: float
    outdoorTime: float
    diagnosedConditions: Optional[List[str]]
    familyHistory: Optional[List[str]]

class LensResponse(BaseModel):
    lens_name: str
    lens_file_name: str
    coating_file_name: str
    description: str
    benefits: str
    lens_image_url: str
    coating_image_url: str
