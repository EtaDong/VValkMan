# Basic questions
> What the process of training neural network is like 

> What is say a trained test split

# Materials
> Lamini

> Deeplearning

# Top questions   
> Why Finetuning?

> Training Process

> Where finetuning fits in

> Evaliation and Iteration

> Instruction finetuning

> Considerations on getting started now

> Data preparation

> Conclusion

# Answers
## **Why finetuning?**
<details>
<summary> What is Finetuning?</summary>

- lets you put more data into the model than what fits into the prompt. 

- get the model to learn the data, rather than just get access to it.

- dermatology data

in addition to steering the model to more consistent outputs or behavior, fine-tuning can help the model reduce   
</details>

---     

<details>
<summary> Prompt VS Finetuning </summary>

Pros of Prompts
- No data to get started
- Smaller upfront cost
- no techical knowledge needed
- Connect data through retrieval(RAG) - Retrieval-Augmented Generation

Cons of Prompts
- Much less data fits
- Forgets data
- Hallucination
- RAG misses, or gets incorrect data 

Conclusion 
- Generic, side projects, prototypes


Pros of Finetuning
- Nearly unlimited data fits
- Learn new information
- Correct incorrect information
- Less cost afterwards if smaller model
- Use RAG too

Cons of Finetuning
- More high-quality data
- Upfront compute cost
- Need some technical knowledge, esp, data

Conclusion
- Domain-specific, enterprice, production usage, ... privacy
</details>

---

<details>
<summary>Benefits of finetuning your own LLM</summary>

Performance
- stop hallucinations
- increase consistency
- reduce unwanted info

Privacy
- on-prem or VPC
- prevent leakage
- no breaches

Cost
- lower cost per request
- increased transparency
- greater control

Reliability
- control   
- lower latency
- moderation
</details>

---

<details>
<summary>Fine tune example</summary>

Technologies to fine tune (python library)
- Pytorch(Meta)
    - lowest level interface
- Huggingface
    - Much higher level 
    - import data sets and train models very easily
- Llama library(Lamini)
    - Even higher level interface where you can train models with just three lines of code 

```python
# Lab for why finetuning: 
# compare finetuned vs non-finetuned open-source model
from llama import BasicModelRunner
non_finetuned = BasicModelRunner("meta-llama/Liama-2-7b-hf")
non_finetuned_output = non_finetuned("Tell me how to train my dog to sit")
print(non_finetuned_output)
print(non_finetuned("What do you think of Mars?")) 
print(non_finetuned("what is taylor swift`s best friend"))
print(non_finetuned("""
Agent: I`m here to help you with your Amazon deliver online
Customer: I did`t get my item
Agent: I`m sorry to hear that. Which item was it?
Customer: the blanket
Agent:
"""))

finetuned_model = BasicModelRunner("meta-llama/Llama-2-7b-chat-hf")
finetuned_output = non_finetuned("Tell me how to train my dog to sit")
print(finetuned_output)
print(finetuned_model("[INST]Tell me how to train your dog to sit[/INST]"))
print(non_finetuned_model("[INST]Tell me how to train your dog to sit[/INST]"))
```
</details>

---

<details>
<summary> Where finetuning fits in ? </summary>

Pretraining
- Model at the start:
    - Zero knowledge about the world
    - Can`t form English words
- Next token prediction
- Giant corpus of text data
- Often scraped from the internet: "unlabeled"
- Self-supervised learning
- After Training
    - Learns language
    - Learns knowledge

What is "data scraped from the internet"?
- Often not publicized how to pretrain
- Open-source pretraining data: " The Pile"
- Expensive & time-consuming to train

Limitations of pretrained base models
Finetuning after pretraining
Pre-training -> Base Model -> Finetuning -> Finetuned Model
- Finetuning usually refers to training further
    - Can also be self-supervised unlabeled data
    - Can be "labeled" data you curated
    - Much less data needed
    - Tool in your toolbox
- Finetuning for generative tasks is not well-defined
    - Updates entire model, not just part of it
    - Same training objective: next token prediction
    - More advanced ways reduce how much to update(more later!)

What is finetuning doing for you?
- Behavior change
    - Learning to respond more consistently
    - Learning to focus, e.g. moderation
    - Teasing out capability, e.g. better at conversation
- Gain knowledge
    - Increasing knowledge of new specific concepts
    - Correcting old incorrect information
- Both

Tasks to finetune
- Just text-in, text-out:
    - Extraction: text in, less text out
        - "Reading"
        - Keywords, topics, routing, agents(planning, reasoning, self-critic, tool use), etc.
    - Expansion: text in, more text out
        - "Writing"
        - Chat, write emails, write code
- Task clarity is key indicator of success
- Clarity means knowing what`s bad vs. good vs. better

First time finetuning
1. Identify tasks by prompt-engineering a large LLM
2. Find tasks that you see an LLM doing ~ok at
3. Pick one task
4. Get ~1000 inputs and outputs for the task, Better than the ~Ok from LLM
5. Finetune a small LLM on this data

Lab2: Where finetuning fits in 
```python
import jsonlines
import itertools
import pandas as pd
from pprint import pprint
import datasets # from huggingface
from datasets import load_dataset

pretrained_dataset = load_dataset("EleutherAI/pile", split="train", streaming=True)

n = 5
print("Pretrained dataset:")
top_n = itertools.islice(pretrained_dataset, n)
for i in top_n:
    print(i)

filename = "lamini_docs.jsonl"
instruction_dataset_df = df.read_json(filename, lines=True)
instruction_df

examples = instruction_dataset_df.to_dict()
text = examples["questions"][0] + examples["answer"][0]
text

if "question" in examples and "answer" in examples:
    text = examples["questions"][0] + examples["answer"][0]
elif "instruction" in examples and "responsible" in examples":
    text = examples["instructions"][0] + examples["responsible"][0]
elif "input" in examples and "output" in examples:
    text = examples["inpit"][0] + examples["output"][0]
else:
    text = examples["text"][0]
    
prompt_template_qa = """### Question:
{question}    

### Answer:
{answer}"""

question = example["question"][0]
answer = examples["answer"][0]

text_with_prompt_template = prompt_template_qa.format(question=question, answer=answer)
text_with_prompt_template

prompt_template_q = """### Question:
{question}    

### Answer:"""

num_examples = len(examples["question"])
finetuning_dataset_text_only = []
finetuning_dataset_question_answer = []
for i in range(num_examples):
    question = examples["question"][i]
    answer = examples["answer"][i]

    text_with_prompt_template_qa = prompt_template_qa.formate(question=question, answer=answer)
    finetuning_dataset_text_only.append({"text": text_with_prompt_template_qa})

    text_with_prompt_template_q = prompt_template_q.formate(question=question)
    finetuning_dataset_question_answer.append({"question": text_with_prompt_template_q})

pprint(finetuning_dataset_text_only[0])
pprint(finetuning_dataset_question_answer[0])

with jsonlines.open(f'lamini_docs_processed.jsonl', 'w') as writer:
    writer.write_all(finetuning_dataset_question_answer)

finetuning_dataset_name = "lamini/lamini_docs"
finetuning_dataset = load_dataset(finetuning_dataset_name)
print(finetuning_dataset)
```
</details>

---

<details>
<summary> Instuction Finetuning </summary>
Finetuning
(e.g. reasoning, routing, copilot, chat, agents)

Instruction Finetuning
- AKA "instruction-tuned" or "instruction-following" LLMs
- Teaches model to behave more like a chatbot
- Better user interface for model interaction
    - Turned GPT-3 into ChatGPT
    - Increase AI adoption, from thousands of researchers to millions of people

Instruction-following datasets
Some existing data is ready as-is, online:
- FAQs
- Customer support conversations
- Slack messages

LLM Data Generation
Non-Q&A data can also be converted to Q&A
- Using a prompt template
- Using another LLM

- ChatGPT("Alpaca")
- Open-source models

Instruction Finetuning Generalization
- Can access model`s pre-existing knowledge
- Generalize following instructions to other data, not in finetuning dataset

Overview of Finetuning
Data prep -> Training -> Evaluation

Lab 3: Instruction tuning lab
```python
import itertools
import jsonlines

from datasets import load_dataset
from pprint import pprint

from llama import BasicModelRunner
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

instruction_tuned_dataset = load_dataset("tatsu=lab/alpaca", split ="train", streaming=True)

m = 5
print("Instruction-tuned dataset:")
top_m = list(itertools.islice(instruction_tuned_dataset, m))
for j in top_m:
    print(j)

prompt_template_with_input = """Below is an instruction that describes a task

### Instruction:
{instruction}

### Input:
{input}

### Response:"""

prompt_template_without_input = """Below is an instruction that describes a task

### Instruction:
{instruction}

### Response:"""

processed_data = []
for j in top_m:
    if not j["input"]:
        processed_prompt = prompt_template_without_input.format(instruction=j["instruction"])
    else:
        processed_prompt = prompt_template_with_input.format(instruction=j["instruction"], input=j["input"])

    processed_data.append({"input": processed_prompt, "output": j["output"]})

pprint(processed_data[0])

with jsonlines.open(f'alpaca_processed.jsonl', 'w') as writer:
    writer.write_all(processed_data)

dataset_path_hf = "lamini/alpaca"
dataset_hf = load_dataset(dataset_path_hf)
print(dataset_hf)

non_instruct_model = BasicModelRunner("meta-llama/Llama-2-7b-hf")
non_instruct_output = non_instruct_model("Tell me how to train my dog to sit")
print("Not instruction-tuned output (Llama 2 Base):", non_instruc_output)

instruct_model = BasicModelRunner("meta-llama/Llama-2-7b-chat-hf")
instruct_output = instruct_model("Tell me how to train my dog to sit")
print("Instruction-tuned output (Llama 2):", instruct_output)

chatgpt = BasicModelRunner("chat-gpt")
instruct_output_chatgpt = chatgpt("Tell me how to train my dog to sit")
print("Instruction-tuned output (ChatGPT):", instruct_output_chatgpt)

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-70m")

def inference(text, model, tokenizer, max_input_tokens=1000, max_output_tokens=1000):
    # Tokenize
    input_ids = tokenizer.encode(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=max_input_tokens
    )

    # Generate
    device = model.device
    generated_tokens_with_prompt = model.generate(
        input_ids=input_ids.to(device),
        max_length=max_output_tokens
    )

    # Decode
    generated_text_with_prompt = tokenizer.batch_decode(generated_tokens_with_prompt)

    # Strip the prompt
    generated_text_answer = generated_text_with_prompt[0][len(text):]

    return generated_text_answer

finetuning_dataset_path = "lamini/lamini_docs"
finetuning_dataset = load_dataset(finetuning_dataset_path)
print(finetuning_dataset)
 

```





</details>












---










  


