# Cloudera Operation Database - 2023
COD Hands on Lab for the 2023 Technical Kick Off
## Project overview
Project covers the basics and more advances features of the Cloudera Operational Databases in CDP Public Cloud Operation Database Data Services.
Data 

**Make sure you replace ** with your name from the code snippets**

## Understanding/Installing the environment
### 1 - Installing an environment with the CLI
First check if you're on the latest base version with the command below.
```
pip3 install cdpcli-beta --upgrade --user
```
![pip_install](images/pip_install.png)

```
cdp --version
```
0.9.77 (BETA)

#### 1.1 - Understanding the CLI
We'll start with a fake command to make the options appearing
```
cdp opdb test
```
![fake_command](images/fake_command.png)
#### 1.2 - Using the CLI to deploy an environment
Create a small COD instance with the minimum (3) workers
```
cdp opdb create-database --environment-name lje-env --database-name **-cod --auto-scaling-parameters
```
