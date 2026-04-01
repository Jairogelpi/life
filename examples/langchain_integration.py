"""
LIFE + LangChain Integration
Example of using LIFE with LangChain agents
"""

from typing import Any, Dict, Optional
from life import LifeAgent, DNA


class LifeLangChainAgent(LifeAgent):
    """
    LIFE-enhanced LangChain agent.
    
    Wraps LangChain agent with biological systems:
    - DNA constrains what tools the agent can use
    - Immune system validates outputs
    - Homeostasis manages long-running chains
    - Context provides portable memory
    """
    
    def __init__(self, langchain_agent: Any, **kwargs):
        super().__init__(**kwargs)
        self.langchain_agent = langchain_agent
        
        # Register LangChain tools in DNA capabilities
        if hasattr(langchain_agent, 'tools'):
            for tool in langchain_agent.tools:
                self.dna.capabilities.append(tool.name)
                # Register validator
                if hasattr(tool, 'validate'):
                    self.nervous.register_tool_validator(tool.name, tool.validate)
    
    def _do_execute(self, task: str, **kwargs) -> Any:
        """Execute via LangChain agent"""
        # Pre-execution: validate task against DNA
        if not self.dna.can_perform(task):
            raise ValueError(f"Task violates DNA constraints: {task}")
        
        # Execute with LangChain
        result = self.langchain_agent.invoke({
            "input": task,
            **kwargs
        })
        
        # Post-execution: validate output
        validation = self.immune.validate_output(result)
        if not validation["valid"]:
            # Attempt auto-correction
            result = self.immune.auto_correct(result, validation["issues"])
        
        return result
    
    @classmethod
    def from_langchain(
        cls,
        llm: Any,
        tools: list,
        dna: Optional[DNA] = None,
        **kwargs
    ) -> "LifeLangChainAgent":
        """Create LIFE agent from LangChain components"""
        from langchain.agents import create_react_agent, AgentExecutor
        from langchain.prompts import PromptTemplate
        
        # Create LangChain agent
        prompt = PromptTemplate.from_template(
            """You are a helpful agent with access to tools.

{tools}

Use the following format:
Thought: your reasoning
Action: tool name
Action Input: tool input
Observation: tool result
... (repeat)
Thought: I know the final answer
Final Answer: your answer

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
        )
        
        agent = create_react_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools)
        
        return cls(executor, dna=dna, **kwargs)


# Example usage
def example_langchain_integration():
    """Example of LIFE + LangChain"""
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain.tools import Tool
        
        # Create tools
        def search_tool(query: str) -> str:
            return f"Search results for: {query}"
        
        tools = [
            Tool(name="search", func=search_tool, description="Search the web")
        ]
        
        # Create LLM
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        
        # Create LIFE-enhanced agent
        agent = LifeLangChainAgent.from_langchain(
            llm=llm,
            tools=tools,
            dna=DNA(
                name="LangChainBot",
                values=["accuracy", "helpfulness"],
                capabilities=["search", "reasoning"],
            ),
        )
        
        # Execute with full LIFE capabilities
        result = agent.execute("What is the capital of Spain?")
        print(f"Result: {result}")
        
        return agent
        
    except ImportError:
        print("LangChain not installed. Run: pip install life-agents[langchain]")
        return None


if __name__ == "__main__":
    example_langchain_integration()
