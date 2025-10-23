"""
===========================================================
  CPU-FRIENDLY GENERATIVE AI DEMO — TEXT ONLY (Safe)
  Author: Training Program
  Requirements: Python 3.9+
===========================================================
"""

# ---------------------------------------------------------
# 1️⃣ INSTALL REQUIRED LIBRARIES
# ---------------------------------------------------------
# pip install torch --upgrade
# pip install transformers

# ---------------------------------------------------------
# 2️⃣ IMPORT LIBRARIES
# ---------------------------------------------------------
from transformers import pipeline

# ---------------------------------------------------------
# 3️⃣ TEXT GENERATION DEMO (TINY MODEL)
# ---------------------------------------------------------
def text_generation_demo():
    print("\n🧠 TEXT GENERATION DEMO (Tiny Model)\n")
    
    # Use small model for low memory usage
    generator = pipeline("text-generation", model="sshleifer/tiny-gpt2")
    
    prompt = "In a futuristic city, AI technology changed the world by"
    result = generator(prompt, max_length=30, num_return_sequences=1)
    
    print("Prompt:", prompt)
    print("\n✨ Generated Text:\n", result[0]['generated_text'])

# ---------------------------------------------------------
# 4️⃣ MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    print("="*50)
    print(" 🚀 CPU-FRIENDLY GENERATIVE AI DEMO — TEXT ONLY ")
    print("="*50)

    # Run text generation
    text_generation_demo()
