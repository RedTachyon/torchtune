# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from typing import Any, Callable, Dict, Mapping, Optional, TypedDict
from xml.etree import ElementTree as ET

import numpy as np

from datasets import load_dataset
from torch.utils.data import Dataset
from torchtune.data._common import CROSS_ENTROPY_IGNORE_IDX
from torchtune.data._messages import validate_messages
from torchtune.modules.tokenizers import ModelTokenizer
from torchtune.modules.transforms import Transform


BASE_PROMPT = """A conversation between User and Assistant. The user asks a question, and the Assistant solves it. The assistant first thinks about the reasoning process in the mind and then provides the user with the answer. The reasoning process and answer are enclosed within <think></think> and <answer></answer> tags, respectively, i.e., <think>reasoning process here</think> <answer>answer here</answer>. User: %s. Assistant:"""

class ReasoningProblem(TypedDict):
    question: str
    cot: str
    answer: str

class RLDataset(Dataset):

    def __init__(
        self,
        *,
        source: str,
        problem_transform: Transform,
        tokenizer: ModelTokenizer,
        filter_fn: Optional[Callable] = None,
        **load_dataset_kwargs: Dict[str, Any],
    ) -> None:
        self._problem_transform = problem_transform
        self._tokenizer = tokenizer

        self._data = load_dataset(source, **load_dataset_kwargs)
        if filter_fn is not None:
            self._data = self._data.filter(filter_fn)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index: int) -> Dict[str, Any]:
        sample = self._data[index]
        return self._prepare_sample(sample)

    def _prepare_sample(self, sample: Mapping[str, Any]) -> Dict[str, Any]:
        transformed_sample = self._problem_transform(sample)  # keys "question" and "answer"

        question = BASE_PROMPT % transformed_sample["question"]

        q_tokens = self._tokenizer.encode(question, add_eos=False)
        mask = [1 for _ in q_tokens]
        answer = transformed_sample["answer"]


        return {"tokens": q_tokens, "mask": mask, "answer": answer}



def extract_tags(text: str):
    # Add root element to make valid XML
    xml_string = f"<root>{text}</root>"
    root = ET.fromstring(xml_string)

    return {
        'think': [elem.text for elem in root.findall('think')],
        'answer': [elem.text for elem in root.findall('answer')]
    }

def shaped_reward(question: str, answer: str, completion: str) -> float:
    question_chars = len(question)
    only_completion = completion[question_chars:]

    try:
        tags = extract_tags(only_completion)
    except ET.ParseError:
        return -1.0

    reward = 0

    if len(tags['answer']) == 1:
        reward += 0.1

    if len(tags['think']) == 1:
        reward += 0.1

    if tags['answer'][-1] == answer:
        reward += 1.0

    return reward


def correctness_reward(question: str, answer: str, completion: str) -> float:
    question_chars = len(question)
    only_completion = completion[question_chars:]

    try:
        tags = extract_tags(only_completion)
    except ET.ParseError:
        return 0.0

    if tags['answer'][-1] == answer:
        return 1.0
    else:
        return 0.0


