
# An InstructLab Taxonomy for Konflux

## Fine tuning, RAG, etc

InstructLab is a specific approach to model fine tuning. There's a lot
of general knowledge on the internet about fine tuning vs RAG, and
which to use depends on the use case, the dataset, the deployment
environment. There are plenty of valid cases where both fine tuning
and RAG may be used together.

General use cases appropriate for fine tuning:
- Given a model a broad base of domain-specific information that it
  can draw from when generating responses.
- Altering the tone or style of the model's responses.
- Resource-constrained environments where a smaller model and/or fewer
  moving parts is preferred compared to a generalized model plus RAG.


A good read: https://helixml.substack.com/p/how-we-got-fine-tuning-mistral-7b

## First, the official public taxonomy

The official InstructLab taxonomy at
https://github.com/instructlab/taxonomy is where you contribute to add
knowledge or skills to the IBM-produced InstructLab models that get
uploaded to https://huggingface.co/instructlab and made available for
the general public to use.

A taxonomy is a set of carefully curated data that is the basis for
what you want your model to learn. The example questions and answers
in your taxonomy, along with any supporting knowledge documents, get
used to generate much larger numbers of synthetic question and answer
pairs that are ultimately used to fine tune a model.

We won't walk through contributing to the official InstructLab
taxonomy here, but follow the guides in its GitHub repository if
you're interested in that.

## Now, a Konflux specific taxonomy and model

[Konflux](https://konflux-ci.dev/) is an open source Kubernetes-native
security-first software factory based on Tekton.  This README.md walks
through creating a Konflux-specific taxonomy that we'll use to
fine tune a Konflux-specific large language model.

This isn't an exhaustive guide, nor does it generate a model suitable
for any production use. Instead, its purpose is to show how someone
can get started using InstructLab to fine tune their own models for
their own purposes.

## Generating Markdown from the Konflux website

This crawls the Konflux documentation website using
https://github.com/paulpierre/markdown-crawler to convert the content
to Markdown, which we use to train InstructLab.

```
pip install beautifulsoup4 requests markdownify markdown-crawler
python crawl.py
```

That's what generated all the markdown files under `markdown/`. You
don't need to re-run this unless you want to pull in new changes from
the website.


## Create Example Questions and Answers

See `qna.yaml`.


## Generate Synthetic Data

InstructLab takes our example question/answer pairs and generates a
lot of synthetic data from them. It's this synthetic data that is then
used to actually train the model. The more knowledge content we're
trying to teach the model, the more generated instructions we need so
that as it randomly picks parts of our knowledge we cover the entire
corpus.

Assuming you've cloned this repository and have a working `ilab` CLI:

```
ilab download
ilab generate --taxonomy-path qna.yaml --num-instructions 20
```

It takes more than 20 instructions to teach the model about the entire
Konflux website, but for simple testing purposes 20 is enough to see
how the process works. The more instructions you generate, the longer
it takes. Generating 300 instructions takes about 30 minutes on a
Fedora 39 machine with Intel i9-13900KF, 32GB RAM, and Nvidia RTX 4080
GPU with InstructLab properly setup for GPU acceleration. Your mileage
may vary.

### Existing Generated Data

The `pre-generated/` folder contains some sample generated data if you'd like to test with a larger number of instructions than 20.

- `pre-generated/train_*.jsonl` is the actual data that will be used to
  train the model
- `pre-generated/test_*.jsonl` is the question and answer pairs from
  qna.yaml that will be used by the training process when testing
  inference on the fine tuned model.

Explore the generated samples with jq:

```
jq -s '.' pre-generated/train_*.jsonl
```


## Train the model

Assuming you have GPU acceleration working from a Linux machine:

```
ilab train --device cuda --input-dir generated --num-epochs 2
```

If you'd prefer to use the pre-generated data, substitute `generated`
for `pre-generated` in the command above.

Training takes about 4 minutes on a Fedora 39 machine with Intel
i9-13900KF, 32GB RAM, and Nvidia RTX 4080 GPU with InstructLab
properly setup for GPU acceleration. Your mileage may vary.


## Chat with the model

In one terminal, start serving your newly trained model:

```
ilab serve --model-path models/ggml-model-f16.gguf
```

In another terminal, chat with the model:

```
ilab chat
```

Some example questions to ask, along with example responses:


```
You are a helpful AI assistant that answers questions about the
Konflux open source project. If you do not know an answer, say you do
not know instead of making up an answer. Keep your answers under 100
words. What is the Konflux project?

The Konflux project is an open-source initiative that aims to simplify
and automate the process of building, testing, and deploying
applications in a Kubernetes environment. By using Konflux, developers
can create reusable, modular, and maintainable code, which can be
easily integrated into various environments, such as on-premises,
cloud, or hybrid systems. Konflux provides a user-friendly interface,
which allows developers to manage their applications' lifecycle more
efficiently, reducing the time and effort required for manual
tasks. Overall, Konflux is a valuable tool for organizations looking
to streamline their DevOps processes, improve collaboration, and
ensure consistent application delivery across different environments.
```


```
You are a helpful AI assistant that answers questions about the
Konflux open source project. If you do not know an answer, say you do
not know instead of making up an answer. Keep your answers under 100
words. How do I get started with Konflux?

To get started with Konflux, first, ensure that your development
environment meets the project's requirements, which include a
supported version of Kubernetes, Helm, and other necessary
tools. Next, follow the installation guide in the Konflux
documentation, which provides step-by-step instructions on how to
install and configure the platform. After installation, create your
first application using Konflux's user-friendly interface, which
guides you through the process of defining, building, testing, and
deploying your application in a Kubernetes environment. Finally,
explore the project's features, such as automated builds, testing, and
deployments, to further streamline your development workflow. By
following these steps, you can quickly get started with Konflux and
leverage its benefits for your development projects.
```


```
You are a helpful AI assistant that answers questions about the
Konflux open source project. If you do not know an answer, say you do
not know instead of making up an answer. Keep your answers under 100
words. What are Konflux environments?

...
```

This last one hallucinated a lot...
