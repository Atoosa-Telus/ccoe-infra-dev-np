
#https://cloud.google.com/sdk/docs/scripting-gcloud

# My startup script
gcloud auth login
gcloud auth list

# My best friend
gcloud config --help

# --format flag
# gcloud topic formats
# https://cloud.google.com/sdk/gcloud/reference/topic/formats
# --format=json|yaml|csv|text|list


# Get information about the currebt project I am owkring on 
gcloud config list
export PROJECT_ID=$(gcloud config get-value project)
echo $PROJECT_ID

# The credentil failure issue:
gcloud auth application-default login

# Update components when failing add-ons
gcloud components update

# How to set projects 
gcloud config set project cio-logging-storage-1b866dc7

# Run legacy queries from command line
bq query --nouse_legacy_sql  < base_queries.sql

bq ls --format=pretty

#setup ssh config
gcloud compute ssh --zone "northamerica-northeast1-a" "python-20210615-154019" --tunnel-through-iap --dry-run
# put all the nfo into confi_file

#https://cloud.google.com/sdk/docs/scripting-gcloud
gcloud init

# but I need key?
gcloud auth activate-service-account --key-file [KEY_FILE]

# working with glcoud comoute instances & notebooks
#gcloud compute instances list

gcloud notebooks instances describe  \
python-20210615-154019 --location=northamerica-northeast1-a

# workspace projects list
gcloud projects list --filter="name=[cio-datahub-ws]* AND lifecycleState:ACTIVE"
gcloud projects list --filter="labels.application:cio-datahub-ws AND lifecycleState:ACTIVE"