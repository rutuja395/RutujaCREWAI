from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, WebsiteSearchTool, FileReadTool, PDFSearchTool
from pydantic import BaseModel, Field

import docx  # Import the docx module
# import PyPDF2  # Import the PyPDF2 module
import re
from collections import Counter
from typing import List
# Check our tools documentations for more information on how to use them


web_search_tool = WebsiteSearchTool()
seper_dev_tool = SerperDevTool()
file_read_tool = FileReadTool()
pdf_read_tool = PDFSearchTool()

file_read_tool = FileReadTool(file_path='C:\\Users\\Rutuja Shah\\Downloads\\RutujaCREWAI\\JdandResume\\src\\job-posting\\data\\jd.md')

# pdf_reader = PDFSearchTool(file_path='C:\\Users\\Rutuja Shah\\Downloads\\RutujaCREWAI\\JdandResume\\src\\job-posting\\data\\resume1.pdf')
# pdf_read_tool = PDFSearchTool(file_path='C:\\Users\\Rutuja Shah\\Downloads\\RutujaCREWAI\\JdandResume\\src\\job-posting\\data\\resume3.pdf')

print("pdf_read_tool", pdf_read_tool)

class ResearchRoleRequirements(BaseModel):
    """Research role requirements model"""
    skills: List[str] = Field(..., description="List of recommended skills for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")
    experience: List[str] = Field(..., description="List of recommended experience for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")
    qualities: List[str] = Field(..., description="List of recommended qualities for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")


@CrewBase
class JobPostingCrew:
    # verbose: bool
    """JobPosting crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

   
    @agent
    def job_description_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['job_description_research_agent'],
            tools=[file_read_tool],
            verbose=True
        )
    
    @agent
    def resume_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_research_agent'],
            tools=[pdf_read_tool],
            verbose=True
        )

    @agent
    def screening_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['screening_agent'],
            tools=[web_search_tool,seper_dev_tool],
            verbose=True
        )
    
    @agent
    def screening_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['screening_writer_agent'],
            tools=[web_search_tool,seper_dev_tool],
            verbose=True
        )
    
    @agent
    def screening_review_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['screening_review_agent'],
            tools=[web_search_tool,seper_dev_tool],
            verbose=True
        )
    
    @task
    def analyse_and_research_jd_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyse_and_research_jd_task'],
            agent=self.job_description_research_agent()
        )
    
    @task
    def analyse_and_research_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyse_and_research_resume_task'],
            agent=self.resume_research_agent()
        )
    
    @task
    def research_screening_questions_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_screening_questions_task'],
            agent=self.screening_agent()
        )
    
    @task
    def search_screening_questions_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_screening_questions_task'],
            agent=self.screening_writer_agent()
        )
    
    @task
    def review_and_edit_screening_questions_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_and_edit_screening_questions_task'],
            agent=self.screening_review_agent()
        )


    @crew
    def crew(self) -> Crew:
        """Creates the JobPostingCrew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose= True,
        )