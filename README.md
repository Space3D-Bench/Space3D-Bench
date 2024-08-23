<p align="center">
<h1 align="center"><strong>Space3D-Bench: Spatial 3D Question Answering Benchmark</strong></h1>
  <p align="center">
    <a href="https://emilia-szymanska.gitlab.io/cv/" target="_blank">Emilia Szymanska</a>&emsp;
    <a href="https://dusmanu.com/" target="_blank">Mihai Dusmanu</a>&emsp;
    <a href="https://jwbuurlage.github.io/" target="_blank">Jan-Willem Buurlage</a>&emsp;
    <a href="https://radmahdi.github.io/" target="_blank">Mahdi Rad</a>&emsp;
    <a href="https://people.inf.ethz.ch/pomarc/" target="_blank">Marc Pollefeys</a>&emsp;
    <br>
    ETH Zurich&emsp;Microsoft Spatial AI Lab, Zurich
    <br>
    <strong>ECCV 2024 Workshop</strong>
  </p>
</p>


<p align="center">
  <a href="http://arxiv.org/abs/TBD" target='_**blank**' disabled>
    <img src="https://img.shields.io/badge/arXiv-TBD-red?">
  </a> 
  <a href="https://arxiv.org/pdf/TBD" target='_blank' disabled>
    <img src="https://img.shields.io/badge/Paper-📖-red?">
  </a> 
  <a href="https://space3d-bench.github.io/" target='_blank'>
    <img src="https://img.shields.io/badge/Project-&#x1F680-green">
  </a>
</p>


<div style="text-align: center;">
    <img src="assets/space3d-bench.jpg" alt="teaser" width=100% >
</div>


<p align="justify"> We present <b>Space3D-Bench</b> - a collection of 1000 general spatial questions and answers related to scenes of the Replica dataset which offers a variety of data modalities: point clouds, posed RGB-D images, navigation meshes and 3D object detections. To ensure that the questions cover a wide range of 3D objectives, we propose an indoor spatial questions taxonomy inspired by geographic information systems and use it to balance the dataset accordingly. Moreover, we provide an assessment system that grades natural language responses based on predefined ground-truth answers by leveraging a Vision Language Model's comprehension of both text and images to compare the responses with ground-truth textual information or relevant visual data. </p>

## 📋 Content

### Released dataset format
TODO
In the release, you 
```
├── core
    ├── abstract_llm.py 
    ├── example_llm.py
    ├── prompts.py
    ├── scene.py 
├── eval.py
```

### Scripts

In terms of scripts - used for evaluation of the answering system responses - the repository contains the following files: 
- `core/abstract_llm.py`: LLM-related interfaces, used for answer evaluation with the to-be-implemented methods;
-  `core/example_llm.py`: an example of the implementation of the LLM interfaces, with calls to Azure OpenAI services and Azure Identity authentication;
- `core/prompts.py`: prompts used when calling LLMs;
- `core/scene.py`: enum class, containing scene names and their corresponding folder names as values;
- `eval.py`: script used to evaluate the answers from a spatial QA system with respect to the scene context.


## 🚀 Getting Started

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

### LLM calls

Depending on the way you receive responses from an LLM that would be used for answers evaluation, you may need to adjust the scripts. Implement two classes, inheriting from `AbstractTextLLM` and `AbstractVisionLLM` classes in `core/abstract_llm.py`, for text-focused and vision-related Large Language Models respectively. We provide example implementations in `core/example_llm.py`, where we use API calls to Azure OpenAI services with Azure Identity authentication to get responses from the models. Then, move to `eval.py` and update the object creation accordingly in lines 26-37. In our case, we create our example objects with the settings from `.env` file having the following format:
```
ENDPOINT="..."
API_VERSION="..."
VISION_DEPLOYMENT="..."
TEXT_DEPLOYMENT="..."
```

We used `2024-02-15-preview` version, `gpt-4-0613` as a text LLM and `gpt-4-vision-preview` for image-related tasks. 

## 🔍 Evaluation

### Automatic assessment explanation

<p align="justify"> The goal of the automatic assessment is to evaluate the responses from an answering system with respect to the actual state of the corresponding scene in the dataset. We divided the assessment into two cases: Ground Truth Check - when the ground truth is indisputable (e.g. number of objects in the room), Answer Cross-check - when the definition of the ground truth would either need to exceed context length or would unnecessarily limit the answering system's creativity (e.g. finding similarities between rooms). In both scenarios, an LLM is provided with the question, the system's answer, and the acceptance criterion, which varies based on the question type. In the case of the Ground Truth Check, the message to the LLM is extended with information on the actual state of the scene with respect to the given question. Answer Cross-check, however, provides an image presenting the corresponding scene(s) in question, accompanied by an example answer. This way, a VLM can decide whether the actual system's answer matches the reality, and not necessarily matching the example, reducing the bias of the assessment system. </p>


<div style="text-align: center;">
    <img src="assets/assessment.png" alt="teaser" width=90% >
</div>

### Running

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


## 🔗 Citation
If you find our paper and project useful, please consider citing:
```bibtex
@inproceedings{szymanska2024space3dbench,
  title={{Space3D-Bench: Spatial 3D Question Answering Benchmark}},
  author={Szymanska, Emilia and Dusmanu, Mihai and Buurlage, Jan-Willem and Rad, Mahdi and Pollefeys, Marc},
  booktitle={European Conference on Computer Vision (ECCV) Workshops},
  year={2024}
}
```