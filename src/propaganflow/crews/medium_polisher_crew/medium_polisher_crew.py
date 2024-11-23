from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from medium_polisher_crew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class MediumPolisherCrew():
	"""MediumPolisherCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def medium_optimization_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['medium_optimization_specialist'],
			verbose=True
		)

	@agent
	def tag_optimization_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['tag_optimization_specialist'],
			verbose=True
		)

	@agent
	def image_placement_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['image_placement_expert'],
			verbose=True
		)

	@agent
	def final_tweaks_reviewer(self) -> Agent:
		return Agent(
			config=self.agents_config['final_tweaks_reviewer'],
			verbose=True
		)

	@task
	def medium_blog_post_optimization(self) -> Task:
		return Task(
			config=self.tasks_config['medium_blog_post_optimization']
		)

	@task
	def tagging_and_monetization_enhancement(self) -> Task:
		return Task(
			config=self.tasks_config['tagging_and_monetization_enhancement']
		)

	@task
	def image_placement_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_placement_task']
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the MediumPolisherCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			memory=True
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
