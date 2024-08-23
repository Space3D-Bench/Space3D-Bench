import json
import re
from pathlib import Path
from typing import Any, Dict
from tqdm import tqdm
from dotenv import dotenv_values

from core.abstract_llm import AbstractVisionLLM, AbstractTextLLM
from core.example_llm import ExampleVisionLLM, ExampleTextLLM  # replace with your code
from core.scene import Scene
from core.prompts import (
    SYSTEM_PROMPT_IMAGE,
    SYSTEM_PROMPT_TEXT,
    PROMPT_IMAGE,
    PROMPT_TEXT,
)


def load(file_path: Path) -> Dict[str, Any]:
    return json.load(file_path.open("r"))


if __name__ == "__main__":

    ############### Replace this example with your own implementation ###############
    config = dotenv_values(".env")

    vision_llm: AbstractVisionLLM = ExampleVisionLLM(
        endpoint=config["ENDPOINT"],
        api_version=config["API_VERSION"],
        deployment=config["VISION_DEPLOYMENT"],
    )
    text_llm: AbstractTextLLM = ExampleTextLLM(
        endpoint=config["ENDPOINT"],
        api_version=config["API_VERSION"],
        deployment=config["TEXT_DEPLOYMENT"],
    )
    #################################################################################

    for scene in Scene:
        scene_path = Path("data") / scene.value

        if scene_path.exists() is False:
            print(f"Data for scene {scene.value} not found.")
            continue

        ground_truth = load(scene_path / "ground_truth.json")
        questions = load(scene_path / "questions.json")
        answers = load(scene_path / "answers.json")
        result_path = scene_path / "result.json"

        result = load(result_path) if result_path.exists() else {}

        for nr, question in tqdm(questions.items()):
            if nr in result:
                continue

            if nr not in answers:
                result[nr] = {"result": "0", "justification": "No answer available."}
                print(f"Question nr {nr} not in answers.")
                continue

            ans = answers[nr]
            question_prompt = ground_truth[nr]["prompt"]
            if isinstance(ground_truth[nr]["answer"], str):
                context = ground_truth[nr]["answer"]
                prompt = PROMPT_TEXT.format(question, context, ans, question_prompt)
                response = text_llm.get_response(
                    prompt=prompt, system_prompt=SYSTEM_PROMPT_TEXT
                )
            else:
                context = ground_truth[nr]["answer"]["example_answer"]
                img_path = Path(ground_truth[nr]["answer"]["image_path"])
                prompt = PROMPT_IMAGE.format(question, context, ans, question_prompt)
                response = vision_llm.get_response(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_IMAGE,
                    image_path=img_path,
                )

            match = re.search(r"\{.*\}", response)
            if match:
                json_content = match.group(0)
                try:
                    response_dict = json.loads(json_content)
                except json.JSONDecodeError:
                    response_dict = {"error": response}
                    print(f"Error: could not parse the LLM response in Q{nr}")
            else:
                response_dict = {"error": response}
                print(f"Error: no JSON format in LLM response Q{nr}")

            result[nr] = response_dict
            result[nr].update({
                "question": question,
                "answer": ans,
                "ground_truth": context
            })

            with result_path.open("w") as result_file:
                json.dump(result, result_file, indent=4)
