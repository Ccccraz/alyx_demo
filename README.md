## Alyx demo

A simple example of the Alyx workflow

## Get start
```bash
git clone https://github.com/Ccccraz/alyx_demo.git

cd alyx_demo

conda env create -n alyx_demo python=3.9

conda activate alyx_demo

pip install .
```

or with uv:
```bash
git clone https://github.com/Ccccraz/alyx_demo.git

cd alyx_demo

uv sync
```

## Workflow
First, check out the `setup_alyx.ipynb` file. If you are using Alyx for the first time, this step will complete the global settings of Alyx.

Then, check out the `gen_data.ipynb` file. This file shows the full workflow of connecting to Alyx, creating a session, generating mock data, and uploading it to our samba server and establishing a connection with Alyx.

- Typically, the workflow is as follows:
```mermaid
sequenceDiagram
  actor User as User
  participant Alyx as Alyx
  participant File Server as File Server
  User ->>+ Alyx: Create Session
  Alyx -->>- User: Ok
  User ->> User: Trial loop
  Note right of User: After the experiment is over
  User ->> User: Package Datasets
  User ->>+ File Server: Upload raw data
  File Server -->>- User: Ok
  User ->>+ Alyx: Register Dataset to Session
  Alyx -->>- User: Ok
  File Server ->> CI/CD Server: Trigger CI/CD
  CI/CD Server ->> File Server: request Dataset by predefined query rule
  File Server ->> CI/CD Server: Send datasets
  CI/CD Server ->> CI/CD Server: run analysis
  CI/CD Server ->> User: send analysis result to User by email
```

Finally, check out the `get_data.ipynb` file. This file shows how to retrieve experiments from Alyx and download the associated datasets.

- A typical data consumption workflow:
```mermaid
sequenceDiagram
  actor User as User
  participant Alyx as Alyx
  participant File Server as File Server
  User ->>+ Alyx: Query Session by Suject like 'COGP-003'
  Alyx ->>- User: All Sessions related to COGP-003
  User ->> User: Query Session by Date like '2022-01-01' to '2022-01-31'
  Note right of User: After the query is over
  User ->>+ Alyx: Query Dataset by Session
  Alyx ->>- User: url of Dataset
  User ->>+ File Server: Download Dataset by url from file server
  File Server ->>- User: Dataset
  User ->> User: Analysis Dataset that downloaded
```