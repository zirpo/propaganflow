from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool,SerperDevTool

# Uncomment the following line to use an example of a custom tool
# from bloq_writing_crew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class BloqWritingCrew():
	"""BloqWritingCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self):
		self.output_filename = None

	@agent
	def persuasive_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['persuasive_writer'],
			tools=[SerperDevTool(),ScrapeWebsiteTool()],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def logic_driven_editor(self) -> Agent:
		return Agent(
			config=self.agents_config['logic_driven_editor'],
			verbose=True
		)
	
	@agent
	def content_humanizer(self) -> Agent:
		return Agent(
			config=self.agents_config['content_humanizer'],
			verbose=True
		)
	
	@agent
	def medium_optimization_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['medium_optimization_specialist'],
			verbose=True
		)

	@task
	def blog_planner_task(self) -> Task:
		return Task(
			config=self.tasks_config['blog_planner_task'],
		)

	@task
	def writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['writing_task'],
			
		)
	@task
	def editing_task(self) -> Task:
		return Task(
			config=self.tasks_config['editing_task'],
			
		)
	
	@task
	def humanizing_task(self) -> Task:
		return Task(
			config=self.tasks_config['humanizing_task'],
			
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the BloqWritingCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			memory=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

	def kickoff(self, inputs=None):
		"""Override kickoff to handle output_filename from inputs"""
		if inputs and 'output_filename' in inputs:
			self.output_filename = inputs['output_filename']
		return super().kickoff(inputs=inputs)
