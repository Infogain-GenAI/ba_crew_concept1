
# from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, task, crew, before_kickoff

# from CustomVectorDBSource import CustomVectorDBSource
# from crewai import Knowledge

# # If you want to run a snippet of code before or after the crew starts,
# # you can use the @before_kickoff and @after_kickoff decorators
# # https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# @CrewBase
# class BaCrewConcept1():
# 	"""BaCrewConcept1 crew"""

# 	# Learn more about YAML configuration files here:
# 	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
# 	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
# 	agents_config = 'config/agents.yaml'
# 	tasks_config = 'config/tasks.yaml'
# 	knowledge = Knowledge()

# 	@agent
# 	def business_analyst(self) -> Agent:
# 		return Agent(
# 			config=self.agents_config['business_analyst'],
# 			verbose=True
# 		)

# 	# To learn more about structured task outputs,
# 	# task dependencies, and task callbacks, check out the documentation:
# 	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
# 	@task
# 	def research_task(self) -> Task:
# 		return Task(
# 			config=self.tasks_config['user_story_creation_task'],
# 			#action=lambda inputs: query_faiss(inputs["query"], index, chunks)
# 		)

# 	# @task
# 	# def reporting_task(self) -> Task:
# 	# 	return Task(
# 	# 		config=self.tasks_config['reporting_task'],
# 	# 		output_file='report.md'
# 	# 	)

# 	@before_kickoff
# 	def prepare_inputs(self, inputs):
# 		#extract the file path and file type from the inputs
# 		file_path = inputs.get("file_path")
# 		file_type = inputs.get("file_type")
# 		#initialize the custom source before the crew starts
# 		custom_source = CustomVectorDBSource(file_path, file_type)
# 		self.custom_source.add(file_path, file_type)
# 		knowledge = Knowledge( collection_name="vector_db_knowledge", sources=[custom_source] )

# 	@crew
# 	def crew(self) -> Crew:
# 		"""Creates the BaCrewConcept1 crew"""
# 		# To learn how to add knowledge sources to your crew, check out the documentation:
# 		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

# 		return Crew(
# 			agents=self.agents, # Automatically created by the @agent decorator
# 			tasks=self.tasks, # Automatically created by the @task decorator
# 			process=Process.sequential,
# 			verbose=True,
# 			knowledge_sources=self.knowledge,
# 			memory=True
# 			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
# 		)
import os
import openai
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from dotenv import load_dotenv

@CrewBase
class BaCrewConcept1():
	# Create a PDF knowledge source
	pdf_source = PDFKnowledgeSource(
		file_paths=["SurfaceAnalyzer_Description.pdf"]
	)
	load_dotenv()

	openai.api_key = os.getenv("OPENAI_API_KEY")
	#openai.api_key = "sk-proj-fIiwrQwmmSoQKYR2DvhKT3BlbkFJ91eyB8pmpaEJ0LGiwV8O"

	# LLM with a temperature of 0 to ensure deterministic outputs
	llm = LLM(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0.8)

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# Create an agent with the knowledge store
	@agent
	def business_analyst(self) -> Agent:
		return Agent(
		config=self.agents_config['business_analyst'],
		verbose=True,
		allow_delegation=False,
		llm=self.llm,
	)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['user_story_creation_task']
	)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			verbose=True,
			process=Process.sequential,
			memory=True,
			manager_llm=self.llm,
			knowledge_sources=[self.pdf_source]
	)

