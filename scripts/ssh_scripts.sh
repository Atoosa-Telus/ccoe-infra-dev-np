#!/bin/bash

gcloud compute ssh  --project "atoosa-wb-v2-pr-656b47" \
 --zone "northamerica-northeast1-a" \
 "test-ssh-vs" --tunnel-through-iap \
-- -L 8080:localhost:8080