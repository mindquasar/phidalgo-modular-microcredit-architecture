
# Modular Microcredit Architecture

This repository contains the functional prototype of a modular architecture for intelligent microloans using Open Finance, Artificial Intelligence (AI), and Blockchain technologies. The system is designed to promote financial inclusion by offering automated, personalized, and transparent microcredits to underserved populations.

> This project was developed as part of the article:  
> **"Diseño de una Arquitectura Modular Basada en IA y Blockchain para Microcréditos Personalizados sobre Open Finance"**,  
> submitted to *IJACSA - International Journal of Advanced Computer Science and Applications* (2025).

## Key Features

- Modular microservices-based architecture.
- AI-driven credit scoring (LightGBM).
- Smart contract generation with Solidity.
- Interaction with blockchain via MetaMask on Ethereum Sepolia testnet.
- API development using FastAPI (Python).
- Frontend implementation using HTML and JavaScript.
- PostgreSQL database for traceability and transaction history.

## Project Structure

```
/app/                  # Main FastAPI application (backend and scoring)
    /api/              # REST endpoints
    /models/           # Trained ML models
    /schemas/          # Pydantic models
    /services/         # Business logic and scoring pipeline

/frontend/             # HTML + JavaScript form for loan applications

/contracts/            # Solidity smart contracts and deployment scripts

/tests/                # Unit tests for key components

requirements.txt       # Python dependencies
```

## Technologies Used

- **Python 3.9+**, FastAPI, Scikit-learn, XGBoost
- **Solidity**, Remix IDE, MetaMask
- **PostgreSQL**
- **Ethereum Sepolia Testnet**
- **Docker** (planned for deployment, not yet used)

## How to Run the Prototype

1. **Clone the repository**

```bash
git clone https://github.com/your-username/modular-microcredit-architecture.git
cd modular-microcredit-architecture
```

2. **Create a virtual environment and install dependencies**

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. **Run the FastAPI backend**

```bash
uvicorn app.main:app --reload
```

4. **Open the frontend**

Launch the HTML form in your browser and interact with the backend. Ensure MetaMask is configured for the Sepolia testnet to sign transactions.

5. **Train the scoring model (optional)**

The `credit_scoring.py` file includes a basic LightGBM model trained on public data (Kaggle). You can retrain or replace it with a new model using alternate datasets.

## Data Source

The prototype uses a public dataset for model simulation:

- https://www.kaggle.com/code/satyaprakashshukl/loan-approval-prediction/input

## License

This repository is distributed under the **Creative Commons Zero (CC0 1.0 Universal)** license. All content is in the public domain and can be reused freely.

## Contact

For questions or collaboration, please contact:

**Pedro Hidalgo**  
Faculty of Systems Engineering, UNMSM  
`[replace_with_email_or_linkedin]`
