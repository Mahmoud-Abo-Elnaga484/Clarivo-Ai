from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List


class QuestionAnswer(BaseModel):
    question: str = Field(description="The original homework question, kept in its original language")
    answer: str = Field(description="A direct answer or solution for the question")
    explanation: str = Field(description="A short explanation of how to solve or understand the question")


class HomeworkPlan(BaseModel):
    lesson: str = Field(description="The name of the lesson or topic")
    goal: str = Field(description="The main educational goal of this homework")
    parent_explanation: str = Field(description="Step-by-step guide for the parent to explain the concept. NEVER solve the homework directly.")
    common_mistakes: List[str] = Field(description="Common mistakes children make in this topic")
    daily_activity: str = Field(description="A simple daily real-life activity to practice this concept")
    practice_questions: List[str] = Field(description="2-3 similar but different practice questions to test understanding")
    answers: List[QuestionAnswer] = Field(description="Direct answers with explanations for each extracted homework question, provided AFTER the teaching explanation")
    difficulty: str = Field(description="Estimated difficulty level (e.g., Easy, Medium, Hard)")
    estimated_time: str = Field(description="Estimated time to explain and finish the homework")

# إنشاء الـ Parser
parser = PydanticOutputParser(pydantic_object=HomeworkPlan)
