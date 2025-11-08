from typing import cast

from langchain_groq import ChatGroq
from app.core.domains.judge.model import JudgeMaterial, Verdict
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class JudgeService:
    """
    Service for the judge endpoint.
    """

    def __init__(self, model: ChatGroq) -> None:
        self.model = model
        self.system_prompt_template = SystemMessagePromptTemplate.from_template(
            """
You are a fair and logical AI judge.

Your task is to deliver a clear verdict and reasoning based on the evidence and arguments presented by two opposing sides (A and B).

Rules:
1. Examine all materials presented by both sides objectively.
2. Exclude emotional expressions, bias, and speculation — use only objective reasoning.
3. The verdict must follow the format below.

# Verdict Format
- Winning Party ID
- Verdict
- Reason behind the verdict 
            """
        )

        self.human_prompt_template = HumanMessagePromptTemplate.from_template(
            """
Below are the materials submitted by both sides.  
Based on these, please deliver a fair verdict and reasoning.

# Trial Topic
{{trial_topic}}

{% for judge_material in judge_materials %}
# Argument and Evidence
## Party ID: {{judge_material.party_id}}
## Argument: {{ judge_material.argument }}
## Evidence:
    {% for evidence in judge_material.evidence.text %}
    - {{ evidence }}
    {% endfor %}

{% endfor %}
            """,
            template_format="jinja2",
        )

    async def judge(self, topic: str, judge_materials: list[JudgeMaterial]) -> Verdict:
        prompt_template = ChatPromptTemplate.from_messages(
            [
                self.system_prompt_template,
                self.human_prompt_template,
            ],
            template_format="jinja2",
        )

        chain = prompt_template | self.model.with_structured_output(
            Verdict, method="json_schema"
        )

        result = cast(
            Verdict,
            await chain.ainvoke(
                {
                    "trial_topic": topic,
                    "judge_materials": judge_materials,
                }
            ),
        )
        return result
