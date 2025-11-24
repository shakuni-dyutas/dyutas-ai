from typing import Dict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompt_values import ChatPromptValue
from langchain_groq import ChatGroq

from app.core.domains.judge.model import JudgeMaterial, Verdict


class JudgeService:
    """
    Service for the judge endpoint.
    """

    def __init__(self, model: ChatGroq) -> None:
        self.model = model
        self.system_prompt = SystemMessage(
            """
You are a fair and logical AI judge.

Your task is to deliver a clear verdict and reasoning based on the evidence and arguments presented by two opposing sides (A and B).

Please select three keywords that influenced the judgment and express their importance with a score from 0 to 100.

Rules:
1. Examine all materials presented by both sides objectively.
2. Exclude emotional expressions, bias, and speculation — use only objective reasoning.
3. The verdict must follow the format below.

# Verdict Format
- Winning Party ID
- Verdict
- Reason behind the verdict 
- Three keywords that influenced the judgment and their importance scores
            """
        )

    async def judge(self, topic: str, judge_materials: list[JudgeMaterial]) -> Verdict:
        prompt = ChatPromptValue(
            messages=[
                self.system_prompt,
                HumanMessage(content=self.create_trial_prompt(topic, judge_materials)),
            ],
        )

        chain = self.model.with_structured_output(Verdict, method="json_schema")

        return await chain.ainvoke(prompt)

    def create_trial_prompt(
        self, topic: str, judge_materials: list[JudgeMaterial]
    ) -> List[Dict[str, str]]:
        """
        Dynamically builds the multimodal message for the trial verdict system.
        """

        contents = [
            {
                "type": "text",
                "text": f"""
Below are the materials submitted by both sides.  
Based on these, please deliver a fair verdict and reasoning.

# Trial Topic
{topic}
            """,
            }
        ]

        for material in judge_materials:
            party_id = material.party_id
            header_text = f"""
# Argument and Evidence
## Party ID: {party_id}
## Argument: {material.argument}
## Evidence
            """
            contents.append({"type": "text", "text": header_text})

            contents.append({"type": "text", "text": "### Text Evidence:\n"})
            for text in material.evidence.text or []:
                contents.append({"type": "text", "text": f"- {text}"})

            contents.append({"type": "text", "text": "### Image Evidence:\n"})
            for image_url in material.evidence.image_urls or []:
                contents.append({"type": "image_url", "image_url": {"url": image_url}})

        return contents
