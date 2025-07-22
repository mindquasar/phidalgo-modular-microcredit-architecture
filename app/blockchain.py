from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (recommended for sensitive data like API keys)
load_dotenv()

# -----------------------------------------------------------------------------
# 1. Connect to the Sepolia testnet using Infura or Alchemy
# -----------------------------------------------------------------------------
# You can create a free Infura/Alchemy account and get an API key.
# The default fallback URL below is just a placeholder.
INFURA_URL = os.getenv("INFURA_URL", "https://sepolia.infura.io/v3/51c8f8410cdd45348e3e13716c5a5042")
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# -----------------------------------------------------------------------------
# 2. Define the smart contract address
# -----------------------------------------------------------------------------
# This contract must be deployed ahead of time (e.g., via Remix, Hardhat).
# We convert the address to checksum format to ensure compatibility.
CONTRACT_ADDRESS = Web3.to_checksum_address(
    os.getenv("CONTRACT_ADDRESS", "0xA1ba981e67d0A587206602ECF48b02a763A12F77")
)

# -----------------------------------------------------------------------------
# 3. Smart contract ABI (Application Binary Interface)
# -----------------------------------------------------------------------------
# This tells Web3 how to encode/decode function calls and parameters.
# Must exactly match the deployed contract's ABI.
contract_abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "_client", "type": "string"},
            {"internalType": "uint256", "name": "_amount", "type": "uint256"},
            {"internalType": "uint8", "name": "_approved", "type": "uint8"},
        ],
        "name": "registerMicrocredit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Create an instance of the contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# -----------------------------------------------------------------------------
# 4. Prepare a transaction for MetaMask to sign (do not send it here)
# -----------------------------------------------------------------------------
def prepare_transaction(client: str, amount: int, approved: bool, sender_address: str) -> dict:
    """
    Prepares a blockchain transaction to register the microcredit.

    Parameters:
    - client (str): Identifier or name of the client
    - amount (int): Amount requested
    - approved (bool): Whether the credit was approved
    - sender_address (str): Wallet address that will sign and send the transaction (from MetaMask)

    Returns:
    - dict: Unsigned transaction dictionary ready for MetaMask to sign
    """

    try:
        # Validate the sender's wallet address using checksum format
        sender = Web3.to_checksum_address(sender_address)

        # -----------------------------
        # Why we set gas and gasPrice:
        # -----------------------------
        # gas: estimates how much computation the transaction will use
        # gasPrice: how much you're willing to pay *per unit of gas*
        #
        # This is essential for MetaMask or any frontend signer to 
        # simulate and present the transaction properly.
        #
        # If omitted, some providers or MetaMask may reject the transaction.
        # We use web3.eth.gas_price for a dynamic value that adapts to network conditions.

        txn = contract.functions.registerMicrocredit(
            client, amount, int(approved)
        ).build_transaction({
            "from": sender,
            "nonce": web3.eth.get_transaction_count(sender),  # Prevents duplicate txs
            "gas": 200000,                                     # Safe upper estimate
            "gasPrice": web3.eth.gas_price                     # Dynamic pricing (recommended)
        })

        # This dictionary can now be sent to MetaMask to sign via frontend
        return txn

    except Exception as e:
        # If anything goes wrong, raise a runtime error with explanation
        raise RuntimeError(f"Failed to prepare transaction: {str(e)}")
