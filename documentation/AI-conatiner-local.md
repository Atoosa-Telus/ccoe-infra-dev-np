# How to use Jupyter on a Google Cloud VM

How to run Notebook instance locally, from [here](https://towardsdatascience.com/how-to-use-jupyter-on-a-google-cloud-vm-5ba1b473f4c2)

If you want to develop using the Deep Learning VM container image on your local machine, you can do that using Docker:
```
IMAGE_NAME="gcr.io/deeplearning-platform-release/tf-latest-cpu"
docker pull "${IMAGE_NAME}"
docker run -p 127.0.0.1:8080:8080/tcp -v "${HOME}:/home" \
            "${IMAGE_NAME}"
```
If you have a GPU on your local machine, change the image name from tf-latest-cpu to tf-latest-cu100.

## Papermill
[Papermill](https://cloud.google.com/blog/products/ai-machine-learning/let-deep-learning-vms-and-jupyter-notebooks-to-burn-the-midnight-oil-for-you-robust-and-automated-training-with-papermill)is a library for parametrizing, executing, and analyzing Jupyter Notebooks. It lets you spawn multiple notebooks with different parameter sets and execute them concurrently. Papermill can also help collect and summarize metrics from a collection of notebooks.