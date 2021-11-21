## Initializing Cloud SDK 

This [page](https://cloud.google.com/sdk/docs/initializing) shows you how to initialize the Cloud SDK.

After you install Cloud SDK, perform initial setup tasks by running [`gcloud init`](https://cloud.google.com/sdk/gcloud/reference/init). You can also run `gcloud init` to change your settings or create a new configuration.

## Authorizing Cloud SDK tools

In order to access Google Cloud, you will usually have to [authorize](https://cloud.google.com/sdk/docs/authorizing) Cloud SDK tools.

`gcloud auth login`: Authorize with a user account without setting up a configuration.

`gcloud auth activate-service-account`: Authorize with a service account instead of a user account. Useful for authorizing non-interactively and without a web browser.

`gcloud config [COMMAND]`

`gcloud config configurations [COMMAND]`: Create and manage Cloud SDK configurations and properties.

## Managing Cloud SDK configurations 

A [configuration](https://cloud.google.com/sdk/docs/configurations) is a named set of Cloud SDK properties. These properties are key-value pairs, organized in sections, that govern the behavior of the gcloud tool and other Cloud SDK tools.

```
gcloud config configurations create [NAME]
gcloud config configurations activate [NAME]
gcloud config configurations list
gcloud config set project [PROJECT]
gcloud config unset project
gcloud config configurations describe [NAME]
gcloud config configurations delete [NAME]

```
