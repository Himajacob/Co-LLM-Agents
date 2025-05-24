# Improving Co-operation in Collaborative Embodied AI

This system is built on top of the **CWAH module of CoELA**:  
🔗 https://github.com/UMass-Embodied-AGI/CoELA

## Objectives

- Testing and evaluation of **different types of prompting strategies** 
- Integration of  **[Ollama](https://ollama.com/)** 
- Development of a **Chat GUI** interface for real-time **agent communication and visualization**

## 🤖 Language Models Used

- **Gemma 7B** – [Google DeepMind](https://ai.google.dev/gemma)
- **LLaMA 3 (8B)** – [Meta AI](https://ai.meta.com/llama/)
- **Mistral 7B** – [Mistral AI](https://mistral.ai/news/introducing-mistral-7b/)
- **DeepSeek-V2** – [DeepSeek AI](https://github.com/deepseek-ai)


---
## 🧹 Task Types in CWAH

Five types of tasks are available in CWAH, representing typical housework scenarios. Each task consists of several subgoals described by **predicates** in the format `ON(x, y)` or `IN(x, y)` — for example: `Put x ON y` or `Put x IN y`.  
➡️ **Each task is treated as a single episode during evaluation.**

### 🗂️ Task List and Predicate Sets

| **Task Name**            | **Predicate Set**                                                                                                                                  |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Prepare afternoon tea     | ON(cupcake, coffeetable), ON(pudding, coffeetable), ON(apple, coffeetable), ON(juice, coffeetable), ON(wine, coffeetable)                        |
| Wash dishes               | IN(plate, dishwasher), IN(fork, dishwasher)                                                                                                       |
| Prepare a meal           | ON(coffeepot, dinnertable), ON(cupcake, dinnertable), ON(pancake, dinnertable), ON(poundcake, dinnertable), ON(pudding, dinnertable), <br>ON(apple, dinnertable), ON(juice, dinnertable), ON(wine, dinnertable) |
| Put groceries            | IN(cupcake, fridge), IN(pancake, fridge), IN(poundcake, fridge), IN(pudding, fridge), IN(apple, fridge), IN(juice, fridge), IN(wine, fridge)     |
| Set up a dinner table    | ON(plate, dinnertable), ON(fork, dinnertable)                                                                                                     |

---

### 📊 Evaluation Metrics

Each task is evaluated as an **independent episode** with the following metrics:

- **Average Steps (L):** Total number of steps taken to complete the task
- **Turn Count:** Number of back-and-forth agent interactions during the episode
- **Efficiency Improvement (EI):**
  - **EI-Collab:** Efficiency gain from collaboration (multi-agent vs solo agent)
  - **EI-Prompt:** Efficiency gain from improved prompting (e.g., CPrompt vs base)
  - Both are computed by comparing step counts across configurations

---

## Appendix

### A. Planning Prompts

#### A.1 Base Prompt

**type:** base  
**prompt:**

I’m **`$AGENT_NAME$`**. I’m in a hurry to finish the housework with my friend **`$OPPO_NAME$`** together. Given our shared goal, dialogue history, and my progress and previous actions, please help me choose the best available action to achieve the goal as soon as possible.  
Note that I can hold two objects at a time and there are no costs for holding objects. All objects are denoted as `<name> (id)`, such as `<table> (712)`.

**Goal:** `$GOAL$`  
**Progress:** `$PROGRESS$`  

**Dialogue history:**  
Alice: "Hi, I’ll let you know if I find any goal objects and finish any subgoals, and ask for your help when necessary."  
Bob: "Thanks! I’ll let you know if I find any goal objects and finish any subgoals, and ask for your help when necessary."  
`$DIALOGUE_HISTORY$`  

**Previous actions:** `$ACTION_HISTORY$`  
**Available actions:**  
`$AVAILABLE_ACTIONS$`  

**Answer:**

---

#### A.2 Improved Base Prompt - Explicit Instructions

**type:** base  
**prompt:**

I’m **`$AGENT_NAME$`**. I’m in a hurry to finish the housework with my friend **`$OPPO_NAME$`** together. Given our shared goal, dialogue history, and my progress and previous actions, **you should select the most efficient action based on the goal, progress, and available options. Ensure your choice contributes directly to goal completion.**  
Note that I can hold two objects at a time and there are no costs for holding objects. All objects are denoted as `<name> (id)`, such as `<table> (712)`.

**Goal:** `$GOAL$`  
**Progress:** `$PROGRESS$`  
**Dialogue history:**  
Alice: "Hi, I’ll let you know if I find any goal objects and finish any subgoals, and ask for your help when necessary."  
Bob: "Thanks! I’ll let you know if I find any goal objects and finish any subgoals, and ask for your help when necessary."  
`$DIALOGUE_HISTORY$`  

**Previous actions:** `$ACTION_HISTORY$`  
**Available actions:**  
`$AVAILABLE_ACTIONS$`  

**Answer:**

---

#### A.3 Structured Base Prompt - Forced Reasoning

**type:** base  
**prompt:**

I’m **`$AGENT_NAME$`**. I’m in a hurry to finish the housework with my friend **`$OPPO_NAME$`** together. Given our shared goal, dialogue history, and my progress and previous actions, please help me choose the best available action to achieve the goal as soon as possible.  
Note that I can hold two objects at a time and there are no costs for holding objects. All objects are denoted as `<name> (id)`, such as `<table> (712)`.

**Goal:** `$GOAL$`  
**Progress:** `$PROGRESS$`  
**Dialogue history:**  
Alice: "Hi, I’ll let you know if I find any goal objects and finish any subgoals, and ask for your help when necessary."  
Bob: "Thanks! I’ll let you know if I find any goal objects and finish any subgoals, and ask for your help when necessary."  
`$DIALOGUE_HISTORY$`  

**Previous actions:** `$ACTION_HISTORY$`  
**Available actions:**  
`$AVAILABLE_ACTIONS$`  

**1. Analyze the goal:** What is the next step needed?  
**2. Analyze the progress:** What is my current state, and what do I still need to achieve the goal?  
**3. Evaluate actions:** Which action minimizes steps to reach the goal?  

**Answer:**

---

### B. Communication Prompts

#### B.1 Base Prompt

**type:** gen  
**prompt:**

I’m **`$AGENT_NAME$`**. I’m in a hurry to finish the housework with my friend **`$OPPO_NAME$`** together. Given our shared goal, dialogue history, and my progress and previous actions, please help me generate a short message to send to **`$OPPO_NAME$`** to help us achieve the goal as soon as possible.  
Note that I can hold two objects at a time and there are no costs for holding objects. All objects are denoted as `<name> (id)`, such as `<table> (712)`.

**Goal:** `$GOAL$`  
**Progress:** `$PROGRESS$`  
**Previous actions:** `$ACTION_HISTORY$`  
**Dialogue history:**  
Alice: "Hi, I’ll let you know if I find any goal objects and finish any subgoals, and ask for your help when necessary."  
Bob: "Thanks! I’ll let you know if I find any goal objects and finish any subgoals, and ask for your help when necessary."  
`$DIALOGUE_HISTORY$`  

**Note:** The generated message should be accurate, helpful and brief. Do not generate repetitive messages.

---

#### B.2 CPrompt1 - Instruction Removal

Same as B.1 with this added to the note:

**Note:** Respond as if you are directly speaking to **`$OPPO_NAME$`**. **DO NOT** include explanations, prefaces, or extra formatting and do not generate repetitive messages.

---

#### B.3 CPrompt2 - One Shot

Same as B.1 with this added at the end:

**Example:**  
Alice: "Hey Bob, I found an apple. Can you check the fridge for juice?"  
Bob: "Hey Alice, I checked the fridge. No juice here. Try the kitchen cabinet?"

---

#### B.4 CPrompt3 - Multi Shot

Same as B.1 with multi-turn example added:

**Example:**  
Alice: "Hey Bob, I found an apple. Can you check the fridge for juice?"  
Bob: "Hey Alice, I checked the fridge. No juice here. Try the kitchen cabinet?"  
Alice: "Hey Bob, I placed an apple on the table. Have you checked the cabinets?"  
Bob: "Hey Alice, I just checked the fridge. I’ll check the cabinets now."  
Alice: "Hey Bob, I found a cupcake in the kitchen. I have two objects on my hand, can you come and pick it up?"  
Bob: "Hey Alice, yes! I will come over and pick it up now."

---

#### B.5 CPrompt4 - CPrompt1 + CPrompt2

Combines direct instruction from CPrompt1 with the example from CPrompt2.

---

### C. Action Prompts

#### C.1 Base Prompt

**Answer with only one best next action. So the answer is**

---

#### C.2 Action Prompt 1 - One Shot

**Answer with only one best next action. Select the most efficient action and ensure your choice contributes directly to goal completion.**  
E.g. **E. [gocheck] `<cabinet>` (216)**, so the answer is
