import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
import pickle

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

evaluate_model = tf.keras.models.load_model('model.h5')

def check_sentence(sentence, model, tokenizer):
    # Токенізація та перетворення на послідовність
    sequence = tokenizer.texts_to_sequences([sentence])
    # Паддінг до максимальної довжини
    padded_sequence = pad_sequences(sequence, maxlen=250)
    # Передбачення
    prediction = model.predict(padded_sequence)[0][0]
    # Виведення результату
    if prediction > 0.6:
        #return("positive", prediction)
        return "positive"
    elif prediction < 0.4:
        #return("negative", prediction)
        return "negative"
    else:
        #return("neutral", prediction)
        return "neutral"

if __name__ == "__main__":
    check_sentence(input())
