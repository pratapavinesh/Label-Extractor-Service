import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_label_name_from_text(text):
    doc = nlp(text)
    # Iterate over the recognized entities
    for ent in doc.ents:
        if ent.label_ == 'PRODUCT':
            return ent.text  # Return the first product name found
    return "can not recognised name"  # Return None if no product name is found