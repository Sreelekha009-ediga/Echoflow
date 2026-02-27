import whisper
import fastapi
import uvicorn
import numpy
import pandas
import sklearn
import language_tool_python
from deep_translator import GoogleTranslator

print("All critical imports successful!")
print("Whisper version:", whisper.__version__)
print("scikit-learn version:", sklearn.__version__)