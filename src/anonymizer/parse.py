import spacy as sp
import stanza as sa
import in_out as in_out

lang = "fr"
path = "./data/test/"


def get_sentences(doc):
    # we are only interested in first and last sentence
    # remove any named entities from first and last sentence
    # spacy
    # unfortunately need to iterate through sents the way the
    # attribute is defined in spacy
    text = []
    for sent in doc.sents:
        text.append(str(sent))
    print("Line 0: {}".format(text[0]))
    print("Line 1: {}".format(text[1]))
    return text


def process_doc(doc):
    # stanza
    for sent in doc.sentences:
        entlist = [ent.text for ent in sent.ents]
        wordlist = [word.text for word in sent.words]
        # now remove all entlist strings from wordlist
        newlist = [i for i in wordlist if i not in entlist]
    return newlist


def init_spacy(lang):
    if lang == "es":
        # model = "es_core_news_sm"
        model = "es_core_news_md"
        # model = "es_core_news_lg"
        # model = "es_dep_news_trf"
    elif lang == "fr":
        # model = "fr_core_news_sm"
        model = "fr_core_news_md"
        # model = "fr_core_news_lg"
        # model = "fr_dep_news_trf"
    else:
        print("model not found, aborting")
        exit()
    # initialize nlp pipeline
    try:
        # disable not needed components
        nlp = sp.load(
            model, exclude=["morphologizer", "attribute_ruler", "lemmatizer", "ner"]
        )
    except OSError:
        raise OSError("Could not find {} in standard directory.".format(model))
    nlp = sp.load(model)
    # find which processors are available in model
    # components = [component[0] for component in nlp.components]
    # print("Loading components {} from {}.".format(components, model))
    return nlp


def init_stanza(lang):
    nlp = sa.Pipeline(
        lang=lang, processors="tokenize,mwt,pos,lemma,ner", tokenize_no_ssplit=True
    )
    return nlp


if __name__ == "__main__":
    nlp_spacy = init_spacy(lang)
    nlp_stanza = init_stanza(lang)
    # process the text
    eml_files = in_out.list_of_files(path)
    for file in eml_files:
        text = in_out.get_text(path + file)
        text = in_out.delete_header(text)
        print(repr(text))
        doc_spacy = nlp_spacy(text)
        text = get_sentences(doc_spacy)
        # start with first line
        doc_stanza = nlp_stanza(text[0])
        # newlist = process_doc(doc_stanza)
        # print("{}: {}".format(file, newlist))
        # in_out.write_file(" ".join(newlist), "./data/out/" + file)
