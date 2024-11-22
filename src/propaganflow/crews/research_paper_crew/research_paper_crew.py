from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool, ScrapeWebsiteTool, SerperDevTool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@CrewBase
class ResearchPaperCrewCrew():
    """ResearchPaperCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def research_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['research_specialist'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()]
        )

    @agent
    def content_organizer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_organizer'],
            tools=[],
        )

    @agent
    def writing_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['writing_expert'],
            tools=[],
        )

    @task
    def gather_sources_task(self) -> Task:
        return Task(
            config=self.tasks_config['gather_sources_task'],
        )

    @task
    def create_outline_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_outline_task'],
            tools=[],
        )

    @task
    def draft_paper_task(self) -> Task:
        return Task(
            config=self.tasks_config['draft_paper_task'],
            tools=[],
        )

    @task
    def revise_edit_task(self) -> Task:
        return Task(
            config=self.tasks_config['revise_edit_task'],
            tools=[],
            
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ResearchPaperCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True
        )
