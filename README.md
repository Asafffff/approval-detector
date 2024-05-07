# ERC-20 Approval Events Fetcher

## Description

This tool retrieves all ERC-20 token approval events for a given Ethereum address using the Infura API. It can be run as a standalone script from the command line or included as part of a FastAPI application to provide an API endpoint for fetching approvals.

## Prerequisites

- Python 3.6+
- An active Infura account with a Project ID
- Internet access to connect to the Ethereum network

### .env File properties:

```.env
PROJECT_NAME=approval-detection
DOMAIN=localhost
ENVIRONMENT=local
LOG_LEVEL=INFO

WEB3_PROVIDER=infura
INFURA_API_URL=https://mainnet.infura.io/v3
INFURA_API_KEY=<YOUR_API_KEY_HERE>
```

## Installation

Clone the repository and navigate to the project directory
Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

# Usage

## Standalone Script

To run the script from the command line and fetch approval events, navigate to the src directory and run:

```bash
python3 src/my_approvals.py --address 0x005e20fCf757B55D6E27dEA9BA4f90C0B03ef852
```

## As Part of FastAPI

To use the script as part of a FastAPI application, you can start the server with Uvicorn. Ensure you are in the root directory of your project, and then run:

```bash
uvicorn src.api.main:app
```

This will serve the FastAPI application where you can access the API endpoint to fetch approval events.

# API Endpoint

Once the FastAPI application is running, you can make a GET request to the following endpoint:

```
http://localhost:8000/approvals?address=0xYourEthereumAddress
```
