from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, WebsiteSearchTool, FileReadTool, PDFSearchTool, ScrapeWebsiteTool, FileWriterTool
from pydantic import BaseModel, Field
# Check our tools documentations for more information on how to use them


web_search_tool = WebsiteSearchTool()
seper_dev_tool = SerperDevTool()
api_url ="https://www.upwork.com/api/v3/jobs/search"
api_key = "your_api_key_here"  # Add your API key here
scrape_website_tool = ScrapeWebsiteTool(website_url=api_url, headers={"Authorization": f"Bearer {api_key}"})
# scrape_website_tool = ScrapeWebsiteTool(website_url=api_url)
file_writer_tool = FileWriterTool(file_path='example.csv')

class ResearchRoleRequirements(BaseModel):
    """Research role requirements model"""
    skills: List[str] = Field(..., description="List of recommended skills for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")
    experience: List[str] = Field(..., description="List of recommended experience for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")
    qualities: List[str] = Field(..., description="List of recommended qualities for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")


@CrewBase
class Upworkscrapecrew:
    # verbose: bool
    """Scarping crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

   
    @agent
    def upwork_scraper_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['upwork_scraper_agent'],
            tools=[scrape_website_tool],
            verbose=True
        )
    
    @agent
    def csv_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['csv_writer_agent'],
            tools=[file_writer_tool],
            # result = file_writer_tool._run(,'this is example'),
            verbose=True
        )
    
    @task
    def research_upwork_website_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_upwork_website_task'],
            agent=self.upwork_scraper_agent()
        )
    
    @task
    def write_to_csv_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_to_csv_task'],
            agent=self.csv_writer_agent()
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Scrapingcrew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose= True,
        )

    # @agent
    # def screening_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['screening_agent'],
    #         tools=[web_search_tool,seper_dev_tool],
    #         verbose=True
    #     )
    
    # @agent
    # def screening_writer_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['screening_writer_agent'],
    #         tools=[web_search_tool,seper_dev_tool],
    #         verbose=True
    #     )
    
    # @agent
    # def screening_review_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['screening_review_agent'],
    #         tools=[web_search_tool,seper_dev_tool],
    #         verbose=True
    #     )
    
    # @task
    # def analyse_and_research_jd_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['analyse_and_research_jd_task'],
    #         agent=self.job_description_research_agent()
    #     )
    
    # @task
    # def analyse_and_research_resume_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['analyse_and_research_resume_task'],
    #         agent=self.resume_research_agent()
    #     )
    
    # @task
    # def research_screening_questions_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['research_screening_questions_task'],
    #         agent=self.screening_agent()
    #     )
    
    # @task
    # def search_screening_questions_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['search_screening_questions_task'],
    #         agent=self.screening_writer_agent()
    #     )
    
    # @task
    # def review_and_edit_screening_questions_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['review_and_edit_screening_questions_task'],
    #         agent=self.screening_review_agent()
    #     )


   