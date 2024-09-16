from fastapi.responses import JSONResponse
from blockchain import Blockchain
from pydantic import BaseModel
from fastapi import FastAPI
from uuid import uuid4
import uvicorn

app = FastAPI()
blockchain = Blockchain()
node_identifier = str(uuid4()).replace("-", "")


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: int


class Nodes(BaseModel):
    nodes: list


@app.post("/transactions/new")
async def new_transaction(transaction: Transaction):
    # Check that the required fields are in the POST'ed data
    required = ["sender", "recipient", "amount"]
    if not all(k in transaction for k in required):
        return JSONResponse(status_code=400, content={"error": "Missing fields"})

    # Create a new Transaction
    index = blockchain.new_transaction(
        transaction["sender"], transaction["recipient"], transaction["amount"]
    )

    response = {"message": f"Transaction will be added to Block {index}"}
    return response


@app.get("/mine")
async def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block["proof"]
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    return response


@app.get("/chain")
async def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return response


@app.post("/nodes/register")
async def regester_nodes(value: Nodes):
    try:
        nodes = value["nodes"]
    except:
        return JSONResponse(status_code=400, content={"error": "No nodes supplied"})

    for node in nodes:
        blockchain.register_node(node)
        response = {
            "message": "New nodes are added",
            "total_nodes": list(blockchain.nodes),
        }
    return response


@app.get("/nodes/resolve")
async def resolve_conflict():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            "message": "This chain is corrected to a new one",
            "new_chain": blockchain.chain,
        }
    else:
        response = {"message": "This chain works well", "chain": blockchain.chain}
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
