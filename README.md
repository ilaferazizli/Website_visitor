# TMS Alert BOT v2

![images](https://github.com/ilaferazizli/Website_visitor/assets/106245401/8304e497-ff0e-446b-8b6c-2a1d3a874200)

- [Docker Image](https://hub.docker.com/repository/docker/zynthasius/beutmsbot/general)

## Hi, I am an alert bot who notifies nerdy students about their exam results! This bot is designed for **Baku Engineering University** by ilaferazizli, dockerized by zynt.

Powered by Selenium Chrome

## Docker environmental variables:

| Name | Description | E.g |
| ---- | ----------- | --- |
|  `BEU_USERNAME` | TMS UserID to login as | `220XXXXXX` |
| `BEU_PASSWORD` | TMS Password | `S3CR3TP4SS` |
| `WEBHOOK_URL` | Discord webhook url to get notified | `https://discord.com/......` |
|  `MENTION_ID` | Role/User id to get a ping | `XXXXXXXXXXXX` |

`docker pull zynthasius/beutmsbot:latest` /
`podman pull docker.io/zynthasius/beutmsbot:latest`

## Use it with care... Enjoy!