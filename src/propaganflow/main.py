#!/usr/bin/env python
import json
import yaml
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel, Field

from crewai.flow.flow import Flow, listen, start

from .crews.research_paper_crew.research_paper_crew import ResearchPaperCrewCrew
from .crews.bloq_writing_crew.bloq_writing_crew import BloqWritingCrew


class ResearchState(BaseModel):
    """
    Pydantic model representing the state of research flow.
    """
    topic: str = Field(
        default="",
        description="The main research topic to investigate"
    )
    research_areas: Optional[str] = Field(
        default="",
        description="Optional specific areas to focus the research on"
    )
    research_result: str = Field(
        default="",
        description="The compiled research results and findings"
    )
    bloq_result: str = Field(
        default="",
        description="The result from the bloq writing process"
    )

    class Config:
        """Pydantic model configuration"""
        validate_assignment = True


class ResearchFlow(Flow[ResearchState]):

    def __init__(self, config_path: Optional[str] = None):
        super().__init__()
        self.config_path = config_path
        self.input_dir = Path(__file__).parent / "crews" / "research_paper_crew" / "research_input"
        self.loaded_config = {}

    def get_available_configs(self) -> List[Path]:
        """Get list of available config files in the research_input directory"""
        return sorted(
            list(self.input_dir.glob("*.yaml")) +
            list(self.input_dir.glob("*.yml")) +
            list(self.input_dir.glob("*.json"))
        )

    def select_config_file(self) -> Optional[Path]:
        """Interactive selection of config file"""
        configs = self.get_available_configs()
        
        if not configs:
            print("No configuration files found in research_input directory")
            return None
            
        print("\nAvailable configuration files:")
        for i, config in enumerate(configs, 1):
            print(f"{i}. {config.name}")
            
        while True:
            try:
                choice = input("\nSelect a configuration file (number) or press Enter for manual input: ")
                if not choice:
                    return None
                    
                index = int(choice) - 1
                if 0 <= index < len(configs):
                    return configs[index]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def load_config(self) -> dict:
        """Load configuration from file if provided"""
        if self.loaded_config:  # Return cached config if already loaded
            return self.loaded_config

        config_path = self.config_path

        # If no config path provided, allow selection from research_input directory
        if not config_path:
            selected_path = self.select_config_file()
            if selected_path:
                config_path = str(selected_path)
            else:
                return {}

        path = Path(config_path)
        if not path.exists():
            print(f"Warning: Config file {config_path} not found")
            return {}

        try:
            if path.suffix.lower() == '.json':
                with open(path) as f:
                    self.loaded_config = json.load(f)
            elif path.suffix.lower() in ['.yaml', '.yml']:
                with open(path) as f:
                    self.loaded_config = yaml.safe_load(f)
            else:
                print(f"Warning: Unsupported file format {path.suffix}")
                self.loaded_config = {}
            return self.loaded_config
        except Exception as e:
            print(f"Error loading config: {e}")
            self.loaded_config = {}
            return {}

    @start()
    def get_topic(self):
        config = self.load_config()
        
        if config.get('topic'):
            self.state.topic = config['topic']
            print(f"Using topic from config: {self.state.topic}")
        else:
            print("Getting research topic")
            self.state.topic = input("Please enter a research topic: ")

    @listen(get_topic)
    def get_research_areas(self):
        if self.loaded_config.get('research_areas'):
            # Convert list of research areas to a semicolon-separated string if it's a list
            research_areas = self.loaded_config['research_areas']
            if isinstance(research_areas, list):
                research_areas = "; ".join(research_areas)
            self.state.research_areas = research_areas
            print(f"Using research areas from config: {self.state.research_areas}")
        else:
            print("Getting research areas")
            self.state.research_areas = input("Please enter specific research areas (optional, press Enter to skip): ")

    @listen(get_research_areas)
    def conduct_research(self):
        print("Conducting research")
        inputs = {"topic": self.state.topic}
        if self.state.research_areas:
            inputs["research_areas"] = self.state.research_areas
            
        result = (
            ResearchPaperCrewCrew()
            .crew()
            .kickoff(inputs=inputs)
        )

        print("Research completed", result.raw)
        self.state.research_result = result.raw

    @listen(conduct_research)
    def save_research(self):
        print("Saving research")
        with open("researchpaper.md", "w") as f:
            f.write(self.state.research_result)
        print("Research paper saved to researchpaper.md")

    @listen(save_research)
    def write_bloq(self):
        print("Starting bloq writing process")
        research_file = Path("researchpaper.md")
        
        inputs = {
            "file_path": str(research_file.absolute()),
            "topic": self.state.topic
        }
        
        result = (
            BloqWritingCrew()
            .crew()
            .kickoff(inputs=inputs)
        )

        print("Bloq writing completed", result.raw)
        self.state.bloq_result = result.raw
        
        # The bloq writing crew already saves to bloq1.md in its review_and_polish task
        print("Bloq content saved to bloq1.md")


def kickoff(config_path: Optional[str] = None):
    research_flow = ResearchFlow(config_path)
    research_flow.kickoff()


def plot():
    research_flow = ResearchFlow()
    research_flow.plot()


if __name__ == "__main__":
    import sys
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    kickoff(config_path)
