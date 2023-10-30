import os
from joblib import load
import tensorflow as tf
from .model import Model

def load_models_from_directory(directory, models_to_load=None):
    models = []

    # iterate over all subdirectories
    for subdir in os.listdir(directory):
        if not os.path.isdir(os.path.join(directory, subdir)):
            continue

        # confirm it matches the "K#" pattern
        if models_to_load is not None and subdir not in models_to_load:
            continue

        vectorizer = None
        selector = None
        model = None
        filetype = None

        # Find and Load vectorizer
        vectorizer_path = None
        for file in os.listdir(os.path.join(directory, subdir)):
            if file.startswith(f"{subdir}_vectorizer") and file.endswith(".pkl"):
                vectorizer_path = os.path.join(directory, subdir, file)
                vectorizer = load(vectorizer_path)
                break
        if not vectorizer_path:
            print(f"Vectorizer not found for {subdir}. Skipping...")
            continue

        # Find and Load selector
        selector_path = None
        for file in os.listdir(os.path.join(directory, subdir)):
            if file.startswith(f"{subdir}_selector") and file.endswith(".pkl"):
                selector_path = os.path.join(directory, subdir, file)
                selector = load(selector_path)
                break
        if not selector_path:
            print(f"Selector not found for {subdir}. Skipping...")
            continue

        # Load model, either .pkl or .h5
        model_path = None
        for file in os.listdir(os.path.join(directory, subdir)):
            if file.endswith("model.pkl"):
                model_path = os.path.join(directory, subdir, file)
                model = load(model_path)
                filetype = "pkl"
                break
            elif file.endswith("model.h5"):
                model_path = os.path.join(directory, subdir, file)
                model = tf.keras.models.load_model(model_path)
                filetype = "h5"
                break

        if not model_path:
            print(f"No suitable model found for {subdir}. Skipping...")
            continue

        if vectorizer and selector and model:
            print(f"Loaded {subdir} model")
            # append the loaded Model instance to models list
            models.append(Model(vectorizer, selector, model, subdir, filetype))

    return models
