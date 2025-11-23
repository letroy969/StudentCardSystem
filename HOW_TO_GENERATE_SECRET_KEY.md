# How to Generate SECRET_KEY in Render

## Option 1: Use Render's Generate Button (Easiest) ✅

### Where to Find It:

1. **In the Environment Variables section:**
   - When you add a new environment variable
   - Look for a **"Generate"** button or **"Generate random value"** link
   - It's usually next to the value input field

2. **If you don't see Generate button:**
   - Just type any random string (you can generate locally and paste it)
   - Or use Option 2 below

---

## Option 2: Generate Locally (Recommended) ✅

### On Windows (PowerShell):

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### On Mac/Linux:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### What This Does:
- Generates a secure 64-character random key
- Copy the output
- Paste it as the value for `SECRET_KEY`

---

## Option 3: Quick Random Key (Simple)

If you can't generate, use any long random string:

```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

Or use an online generator:
- https://randomkeygen.com/
- Use "CodeIgniter Encryption Keys" - copy one

---

## ✅ Recommended Steps:

1. **Open PowerShell** (Windows) or Terminal (Mac/Linux)
2. **Run**: `python -c "import secrets; print(secrets.token_hex(32))"`
3. **Copy** the output (64 characters)
4. **Paste** into Render's `SECRET_KEY` value field
5. **Save**

---

## Example Output:

```
a7f3b8c9d2e1f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

Just copy and paste this into Render!

---

**Easiest: Generate locally and paste into Render!** 🚀

