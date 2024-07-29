# VulcanBox

VulcanBox is a powerful and user-friendly command-line interface (CLI) tool designed to help you manage your Github repositories efficiently.

## Features

With VulcanBox, you can...

- Create repositories: Create new GitHub repositories effortlessly.
- List repositories: List all repositories of a specified GitHub user.
- Clone repositories: Clone repositories to your local machine.
- Manage collaborators: Add or remove collaborators from your repositories.

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
   git clone https://github.com/yourusername/vulcanbox.git
   cd vulcanbox
   ```

2. Install dependencies

   ```shell
   poetry install
   ```

3. Set up your environment variables for GitHub API

   ```bash
   export GITHUB_USERNAME="your username"
   export GITHUB_API_TOKEN="my-token"
   ```

There is also a Docker implementation available.

```shell
docker build -t vulcanbox .
docker run --rm -e GITHUB_API_TOKEN="${GITHUB_API_TOKEN}" -e GITHUB_USERNAME="${GITHUB_USERNAME}" vulcanbox --version
```

## Usage

You can use VulcanBox directly through the command line.

```shell
vulcanbox --help
```
