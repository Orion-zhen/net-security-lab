import base64
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA


n = b"This is a test string"
h = SHA.new()
h.update(n)
print(f"Hash: {h.hexdigest()} length: {len(h.hexdigest())*4}")

sign_txt = "sign.txt"

with open("master-private.pem") as f:
    key = f.read()
    private_key = RSA.importKey(key)
    hash_obj = SHA.new(n)
    signer = Signature_pkcs1_v1_5.new(private_key)
    d = base64.b64encode(signer.sign(hash_obj))

f = open(sign_txt, "wb")
f.write(d)
f.close()

with open("master-private.pem") as f:
    key = f.read()
    public_key = RSA.importKey(key)
    sign_file = open(sign_txt, "r")
    sign = base64.b64decode(sign_file.read())
    h = SHA.new(n)
    verifier = Signature_pkcs1_v1_5.new(public_key)
    print(f"result: {verifier.verify(h,sign)}")
