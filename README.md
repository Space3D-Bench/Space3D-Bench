# Space3D-Bench

TODO

## Repository content

### Repository files

TODO

### Released dataset format

#### General structure
TODO

#### 

## Setup

### Environment

1. Download the repository.
    ```bash
    git clone https://github.com/Space3D-Bench/Space3D-Bench.git
    cd Space3D-Bench
    ```
2. Prepare your python virtual environment (example shown for conda).
    ```bash
    conda create -n your_env_name python=3.10
    conda activate your_env_name
    ```
3. Install the requirements.
    ```bash
    pip install -r requirements.txt
    ```

### Data

1. Download the dataset and place it in the repository:
    ```bash
    wget https://github.com/Space3D-Bench/Space3D-Bench/releases/download/v0.0.1/data.zip
    unzip data.zip -d path/to/the/Space3D-Bench/repository
    rm data.zip
    ```
2. Run the questions from data/SCENE_NAME/questions.json on your Q&A system, using Replica dataset data and our proposed curated detections with navigation meshes (described in the `Repository content` section). Keep saving the responses from your system to a JSON file in the following format:
    ```json
    {
        "1": "Answer to question nr 1.",
        "2": "Answer to question nr 2.",
        ...
    }
    ```
3. Place the responses-containing JSON files in the corresponding `data/SCENE_NAME/` directory, with a file name changed to `answers.json` (you may choose another name, but then update the line 49 in `eval.py` accordingly).

### LLM interaction

Depending on the way you receive responses from an LLM that would be used for answers evaluation, you may need to adjust the scripts. Implement two classes, inheriting from `AbstractTextLLM` and `AbstractVisionLLM` classes in `core/abstract_llm.py`, for text-focused and vision-related Large Language Models respectively. We provide example implementations in `core/example_llm.py`, where we use API calls to Azure OpenAI services with Azure Identity authentication to get responses from the models. Then, move to `eval.py` and update the object creation accordingly in lines 26-37. In our case, we create our example objects with the settings from `.env` file having the following format:
```
ENDPOINT="..."
API_VERSION="..."
VISION_DEPLOYMENT="..."
TEXT_DEPLOYMENT="..."
```

## Evaluation

Once the preparation steps descibed in `Setup` sections are done, simply run the `eval.py` file from within your environment:
```bash
cd path/to/Space3D-Bench/repo
python eval.py
```

The assessment results will be incrementally saved to `data/SCENE_NAME/result.json`. In case the evaluation is interrupted, you can rerun the script and it will skip the questions for which the assessment decision is already present in the result JSON. The script will also skip the scenes for which the `answers.json` file does not exist.

The `result.json` file will have the following structure:
```json
{
    "1": {
        "result": "0",
        "justification": "Justification for result 1.",
        "question": "First question?",
        "answer": "Answer to the first question.",
        "context": "Scene context (ground truth information or an example of an answer)."
    },
    "2": {
        "result": "1",
        "justification": "Justification for result 2.",
        "question": "Second question?",
        "answer": "Answer to the second question.",
        "context": "Scene context (ground truth information or an example of an answer)."
    },
    ...
}
```
In the result field, 1 indicates an answer acceptance, 0 a rejection.