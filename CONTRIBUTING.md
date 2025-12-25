# Contribution guidelines

Contributing to this project should be as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## Github is used for everything

Github is used to host code, to track issues and feature requests, as well as accept pull requests.

Pull requests are the best way to propose changes to the codebase.

1. Fork the repo and create your branch from `main`.
2. If you've changed something, update the documentation.
3. Make sure your code lints (using `scripts/lint`).
4. Test you contribution.
5. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Development

The easiest way to get started with development is to use Visual Studio Code with [devcontainers](https://code.visualstudio.com/docs/devcontainers/containers). This approach creates a preconfigured development environment with the necessary tools

You can follow the [official Home Assistant guide](https://developers.home-assistant.io/docs/setup_devcontainer_environment/) for the initial setup.

Below is a single, consolidated version of the two text fragments, with consistent structure, corrected numbering, and the repository URL set to `https://github.com/ping-localhost/panda-status`.

### Getting ready

1. Clone the repository to a local directory on your computer:
   ```shell
   cd $HOME
   git clone https://github.com/ping-localhost/panda-status
   ```
3. Change into the directory of your fork and start Visual Studio Code from there:

   ```shell
   cd panda-status
   code .
   ```
4. Visual Studio Code will automatically detect the devcontainer and prompt you to **Reopen in Container** (bottom-right corner). Click this option.
   <p class='img'>
     <img src='https://developers.home-assistant.io/img/en/development/reopen_in_container.png' />
   </p>
5. Confirm that the project is opened inside the devcontainer.
6. Run the setup script:
   ```shell
   ./scripts/setup
   ```

   This step will:

   * Install `uv` if it is not already installed,
   * Create a virtual environment if needed,
   * Activate the environment, and
   * Install all required dependencies.
7. Start the development environment by running:
   ```shell
   ./scripts/develop
   ```
8. Home Assistant will then be available with this custom component at: `http://localhost:8123/`.
