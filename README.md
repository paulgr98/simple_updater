# Simple Updater

Simple Updater is a Python application designed to automate the process of checking for and installing software updates based on a user-defined configuration. It currently supports updating applications via `winget`.

## Features

*   **Automated Updates**: Checks for and installs updates for configured applications.
*   **Configurable**: Easily define which applications to manage using a `config.json` file.
*   **Winget Integration**: Leverages `winget` for seamless updates of applications available through the Windows Package Manager.

## How to Use

### Prerequisites

*   Python 3.x
*   Windows Package Manager (`winget`) (for `winget` type applications)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/simple_updater.git
    cd simple_updater
    ```

### Configuration

The `simple_updater` relies on a `config.json` file to know which applications to manage.

1.  **Create `config.json`**: Copy the provided `config.template.json` and rename it to `config.json` in the root directory of the project.
    ```bash
    cp config.template.json config.json
    ```

2.  **Rename `config.template.json`** to `config.json` and define your applications.

    **`config.json` Structure:**

    The `config.json` file should contain a JSON array named `apps`. Each object within this array represents an application to be managed and should have the following properties:

    *   `name` (string): A user-friendly name for the application (e.g., "PowerToys").
    *   `type` (string): The update mechanism to use. Currently, only `"winget"` is supported.
    *   `id` (string): The unique identifier for the application within the specified `type`'s ecosystem. For `winget`, this is the package ID (e.g., "Microsoft.PowerToys").

    **Example `config.json`:**

    ```json
    {
      "apps": [
        {
          "name": "PowerToys",
          "type": "winget",
          "id": "Microsoft.PowerToys"
        },
        {
          "name": "Visual Studio Code",
          "type": "winget",
          "id": "Microsoft.VisualStudioCode"
        }
      ]
    }
    ```

### Running the Updater

Execute the `main.py` script to check for and apply updates:

```bash
python main.py
```

The script will print out the status of updates and which applications are being updated.
