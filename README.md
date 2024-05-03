
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
ilab train --device cuda --input-dir generated
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
How does Konflux use Tekton Chains?

Konflux uses Tekton Chains to define, execute, and manage workflows
for deploying and managing containerized applications. Tekton Chains
allows Konflux to create complex workflows that consist of multiple
tasks, each of which can be executed in a containerized
environment. By using Tekton Chains, Konflux can ensure that each task
in the workflow is executed in the correct order, with the correct
dependencies, and with the correct resources. Additionally, Tekton
Chains provides built-in support for monitoring and logging, allowing
Konflux to track the progress of each workflow and troubleshoot any
issues that may arise. Overall, Tekton Chains provides a powerful and
flexible framework for managing workflows in containerized
environments, allowing Konflux to deploy and manage containerized
applications more efficiently and effectively.
```


```
Can Konflux produce a signed in-toto attestation?

Yes, Konflux can produce a signed in-toto attestation. In-toto is a
framework for building trust in containerized workloads, and it allows
users to attest to the provenance and integrity of container
images. Konflux supports in-toto attestations by generating signed
attestations for container images that are built using
in-toto-compatible build tools, such as Buildpacks or Kaniko. These
attestations can be used to verify the provenance and integrity of the
container images, ensuring that they have not been tampered with or
modified since they were built. By generating signed in-toto
attestations, Konflux can help users build trust in their
containerized workloads and ensure that they are secure and reliable.
```

```
What are Konflux environments?

Konflux environments are a set of tools that allow users to manage and
configure their containerized applications in a more automated and
efficient way. Environments allow users to define the configuration,
dependencies, and resources required to run their applications, and
then deploy those applications to various target environments, such as
development, staging, or production. Environments can be used to
manage the entire lifecycle of an application, from development to
deployment to management, allowing users to ensure that their
applications are always up-to-date, secure, and running on the latest
versions oftheir dependencies. By using Konflux environments, users
can streamline their development and deployment processes, reduce the
risk of errors and inconsistencies, and ensure that their applications
are always available and accessible to their users.
```

```
What is SLSA?

SLSA, or the Supply Chain Levels for Software Artifacts, is an open
framework designed to build trust in the software supply chain by
establishing security best practices and providing a clear,
consistent, and verifiable way to ensure software artifacts'
integrity, provenance, and authenticity. SLSA comprises four levels,
each with increasing levels of security and assurance, to help
organizations implement security measures in their software
development and delivery processes. By following SLSA, developers can
build trust in their software supply chain, reduce the risk of
security vulnerabilities, and ensure the integrity of their software
artifacts.
```

```
What does SLSA have to do with Konflux?

SLSA (Supply Chain Levels for Software Artifacts) is directly related
to Konflux as it is one of the key security frameworks that Konflux
follows to ensure the security and integrity of the software supply
chain. By adhering to SLSA's best practices and guidelines, Konflux
helps developers build trust in their software supply chain, reduce
the risk of security vulnerabilities, and ensure the integrity of
their software artifacts. Konflux's integration with SLSA enables
developers to create secure and reliable software delivery pipelines,
which in turn helps maintain the trust of end-users and stakeholders
in the software.
```


Hallucinations, or product suggestions?

```
How do I retrieve my generated SBOMs with the Konflux CLI?


To retrieve your generated Software Bill of Materials (SBOMs) using
the Konflux Command Line Interface (CLI), follow these steps:

1. Install the Konflux CLI: To use the Konflux CLI, you need to
install it first. Follow the installation instructions provided in the
(https://konfluxproject.github.io/konflux-docs/).

2. Authenticate: Once the Konflux CLI is installed, authenticate it
   using your credentials. Run the following command:
   
konflux login

3. Retrieve your SBOMs: After logging in, you can retrieve your
generated SBOMs using the `konflux sbom get` command. The command has
several options to help you filter and sort the results. For example,
to list all your SBOMs, run:

konflux sbom get --all

4. View your SBOMs: Once you have retrieved your SBOMs, you can view
   them in your terminal or save them to a file for further analysis
   or sharing.
```
