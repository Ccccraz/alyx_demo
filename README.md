## Alyx demo

A simple example of the Alyx workflow

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
```

Finally, check out the `get_data.ipynb` file. This file shows how to retrieve experiments from Alyx and download the associated datasets.