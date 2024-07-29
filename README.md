# VulcanBox

VulcanBox is a powerful and user-friendly command-line interface (CLI) tool designed to help you
manage your test containers easily.

## Features

With VulcanBox, you can...

- Create Docker images
- Create Virtualbox VMs
- List available images and VMs

## Development Setup

### Preqrequisites

Before getting started on development for this project, install the following on your local machine:

- [Python 3.10](https://www.python.org/downloads/) or above
- [Docker](https://docs.docker.com/engine/install/)

Additional installs; optional, for developer convenience

- [Just](https://github.com/casey/just) command runner
- [Direnv](https://direnv.net/docs/installation.html)

VulcanBox can be installed using Poetry. Ensure you have Poetry installed on your system.

1. Clone the repository

   ```shell
   git clone https://github.com/jgfranco17/vulcanbox.git
   cd vulcanbox
   ```

2. Install dependencies

   ```shell
   poetry install
   ```

There is also a Docker implementation available.

```shell
docker build -t vulcanbox .
docker run --rm vulcanbox --version
```

## Usage

You can use VulcanBox directly through the command line.

```shell
vulcanbox --help
```
