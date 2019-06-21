# Nicotine: _apply some patches™_

![nicotine_smiles_and_cries](/images/nicotine_smiles_and_cries.png)

## What is nicotine?

Nicotine is an automated patching tool.

## Why nicotine?

Shitty, monolithic servers are susceptible to hacker cancer. But you care about their health and want to see them become the dockerized and immutable microservices that you know they can be. In the interim: put them on the patch: _the Nicotine Patch™_.

## How does nicotine work?

Nicotine is a glorified script that takes an AWS profile string and an `AWS EC2 instance id` and then uses `AWS SSM` to `sudo yum update -y && sudo shutdown -r now`. And then it runs whatever system tests you want. 
