import zipfile
import os

root = "backend"
skip = {".env", ".env.example", "Dockerfile", "s.yaml", "__pycache__"}

with zipfile.ZipFile("deploy.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for fname in filenames:
            if fname in skip or fname.endswith(".pyc"):
                continue
            src = os.path.join(dirpath, fname)
            arcname = src.replace(root + os.sep, "").replace("\\", "/")
            z.write(src, arcname)
print("done")
