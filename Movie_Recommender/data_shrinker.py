import pickle
import numpy as np

similarity = pickle.load(open('similarity.pkl', 'rb'))
similarity = similarity.astype(np.float16)
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Model successfully shrunk ! ready for GitHub.")