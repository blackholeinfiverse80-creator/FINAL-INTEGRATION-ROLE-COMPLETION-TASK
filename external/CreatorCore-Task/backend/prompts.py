try:
    from langchain_core.prompts import PromptTemplate
except Exception:
    # Minimal fallback PromptTemplate for environments without langchain_core
    class PromptTemplate:
        def __init__(self, input_variables=None, template=""):
            self.input_variables = input_variables or []
            self.template = template

# Prompt template for Story Generation
story_prompt = PromptTemplate(
    input_variables=["topic", "goal"],
    template="""
You are a creative storyteller. Generate a compelling story based on the following topic and goal.

Topic: {topic}
Goal: {goal}

Please provide the story in a structured format:
- Title: [Story Title]
- Introduction: [Brief intro]
- Body: [Main story content]
- Conclusion: [Ending]

Ensure the story is engaging, coherent, and aligns with the goal.
"""
)

# Prompt template for Ad/Script Generation
ad_script_prompt = PromptTemplate(
    input_variables=["topic", "goal"],
    template="""
You are an advertising copywriter. Create an effective ad script for the following topic and goal.

Topic: {topic}
Goal: {goal}

Provide the ad script in this format:
- Hook: [Attention-grabbing opening]
- Body: [Main message and benefits]
- Call to Action: [What the audience should do next]

Make it persuasive, concise, and targeted.
"""
)

# Prompt template for Podcast Script Generation
podcast_script_prompt = PromptTemplate(
    input_variables=["topic", "goal"],
    template="""
You are a podcast scriptwriter. Develop a podcast episode script based on the topic and goal.

Topic: {topic}
Goal: {goal}

Structure the script as follows:
- Introduction: [Host intro and topic overview]
- Main Content: [Discussion points, interviews, or segments]
- Conclusion: [Wrap-up and key takeaways]

Keep it conversational, informative, and engaging for listeners.
"""
)