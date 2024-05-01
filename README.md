
# An InstructLab Taxonomy for Konflux

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

Assuming you've cloned this repository into `~/src/instructlab/konflux-taxonomy`:

```
ilab generate --taxonomy-path ~/src/instructlab/konflux-taxonomy/qna.yaml --num-instructions 300
```

Generating 300 instructions takes about 30 minutes on a Fedora 39
machine with Intel i9-13900KF, 32GB RAM, and Nvidia RTX 4080 GPU with
InstructLab properly setup for GPU acceleration. Your mileage may
vary.

### Existing Generated Data

The `generated/` folder contains some sample generated data.

- `generated/train_merlinite-7b-lab-Q4_K_M.jsonl` is the actual data
  that will be used to train the model
- `generated/test_merlinite-7b-lab-Q4_K_M.jsonl` is the question and
  answer pairs from qna.yaml that will be used by the training process
  when testing inference on the fine-tuned model.

Explore the generated samples with jq:

```
jq -s '.' train_merlinite-7b-lab-Q4_K_M.jsonl
```


## Train the model

Assuming you've cloned this repository into
`~/src/instructlab/konflux-taxonomy` and have GPU acceleration working
from a Linux machine:

```
ilab train --device cuda --input-dir ~/src/instructlab/konflux-taxonomy/generated --num-epochs 2
```

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
You are a helpful AI assistant that answers questions about the Konflux open source project. If you do not know an answer, say you do not know instead of making up an answer. Keep your answers under 100 words. What is the Konflux project?

The Konflux project is an open-source initiative that aims to simplify and automate the process of building, testing, and deploying applications in a Kubernetes environment. By using Konflux, developers can create reusable, modular, and maintainable code, which can be easily integrated into various environments, such as on-premises, cloud, or hybrid systems. Konflux provides a user-friendly interface, which allows developers to manage their applications' lifecycle more efficiently, reducing the time and effort required for manual tasks. Overall, Konflux is a valuable tool for organizations looking to streamline their DevOps processes, improve collaboration, and ensure consistent application delivery across different environments.
```


```
You are a helpful AI assistant that answers questions about the Konflux open source project. If you do not know an answer, say you do not know instead of making up an answer. Keep your answers under 100 words. How do I get started with Konflux?

To get started with Konflux, first, ensure that your development environment meets the project's requirements, which include a supported version of Kubernetes, Helm, and other necessary tools. Next, follow the installation guide in the Konflux documentation, which provides step-by-step instructions on how to install and configure the platform. After installation, create your first application using Konflux's user-friendly interface, which guides you through the process of defining, building, testing, and deploying your application in a Kubernetes environment. Finally, explore the project's features, such as automated builds, testing, and deployments, to further streamline your development workflow. By following these steps, you can quickly get started with Konflux and leverage its benefits for your development projects.
```


```
You are a helpful AI assistant that answers questions about the Konflux open source project. If you do not know an answer, say you do not know instead of making up an answer. Keep your answers under 100 words. What are Konflux environments?

...
```

This last one hallucinated a lot...
