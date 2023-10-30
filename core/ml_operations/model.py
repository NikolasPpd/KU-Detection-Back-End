from core.utils.code_preprocessing import *

class Model:
    def __init__(self, vectorizer, selector, model, name, filetype):
        self.vectorizer = vectorizer
        self.selector = selector
        self.model = model
        self.name = name
        self.filetype = filetype

    def __str__(self):
        return self.name

    def predict(self, code):
        prediction = None

        code = "\n".join(code)
        code = remove_blank_lines(code)
        code = replace_strings_and_chars(code)
        code = replace_numbers(code)
        code = replace_booleans(code)
        code_tokens_list = tokenize_code(code)

        code_vec = self.__ngram_vectorize_text(
            texts=[word_list_to_string(code_tokens_list)],
        )

        # Use the trained model to make a prediction on the preprocessed text
        if self.filetype == "pkl":
            prediction = self.model.predict(code_vec)
            prediction = prediction[0]
        elif self.filetype == "h5":
            code_vec = code_vec.toarray()
            prediction = self.model(code_vec)
            prediction = prediction[0][0]
            if prediction > 0.5:
                prediction = 1
            else:
                prediction = 0

        return prediction

    def __ngram_vectorize_text(self, texts):
        # Vectorize new texts using the same vectorizer that was used during training.
        x = self.vectorizer.transform(texts)

        # Select top 'k' features using the same selector that was used during training.
        x = self.selector.transform(x).astype("float32")

        return x
