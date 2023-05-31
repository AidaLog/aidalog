from main.settings import os, BASE_DIR, MEDIA_ROOT,MEDIA_URL
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import numpy as np

import networkx as nx
import matplotlib.pyplot as plt

import random

this_dir = os.path.join(BASE_DIR, 'ner/engine/')
model = load_model(this_dir + 'model/NER.h5')

with open(this_dir + 'tokenizer/word2idx.json', 'r') as fp:
    word2idx = dict(json.load(fp)[0])

with open(this_dir + 'tokenizer/tag2idx.json', 'r') as fp:
    tag2idx= dict(json.load(fp)[0])

with open(this_dir + 'tokenizer/pos2idx.json', 'r') as fp:
    pos2idx = dict(json.load(fp)[0])

with open(this_dir + 'tokenizer/idx2word.json', 'r') as fp:
    idx2word = dict(json.load(fp)[0])

with open(this_dir + 'tokenizer/idx2tag.json', 'r') as fp:
    idx2tag = dict(json.load(fp)[0])

with open(this_dir + 'tokenizer/idx2pos.json', 'r') as fp:
    idx2pos = dict(json.load(fp)[0])

with open(this_dir + 'tokenizer/pos_translation.json', 'r') as fp:
    pos_translation = dict(json.load(fp)[0])

with open(this_dir + 'tokenizer/ner_tags_translation.json', 'r') as fp:
    ner_tags_translation = dict(json.load(fp)[0])


pos_colors = {
    'VBG': '#FFCC00',   # Verbal gerund (Yellow)
    'NNP': '#FF99CC',   # Proper noun, singular (Pink)
    'IN': '#33CCFF',    # Preposition or subordinating conjunction (Light Blue)
    'WDT': '#99FF33',   # Wh-determiner (Green)
    'RB': '#FF6699',    # Adverb (Magenta)
    'DT': '#FFCC99',    # Determiner (Light Orange)
    'LRB': '#66CCFF',   # Left round bracket (Blue)
    'JJR': '#66FFCC',   # Adjective, comparative (Light Green)
    'VBZ': '#99CCFF',   # Verb, 3rd person singular present (Light Blue)
    'VB': '#FFFF66',    # Verb, base form (Yellow)
    'NN': '#FF6666',    # Noun, singular or mass (Red)
    'TO': '#99FF66',    # to (Light Green)
    'JJS': '#FF9966',   # Adjective, superlative (Light Orange)
    'FW': '#FF99FF',    # Foreign word (Purple)
    '.': '#CC66FF',     # Period (Violet)
    'RBR': '#66FF99',   # Adverb, comparative (Light Green)
    'VBD': '#99FF99',   # Verb, past tense (Pale Green)
    'PDT': '#FF9933',   # Predeterminer (Dark Orange)
    'MD': '#FFCC66',    # Modal (Orange)
    'EX': '#CCFF66',    # Existential there (Light Green)
    '$': '#FFFF66',     # Currency symbol (Yellow)
    'WRB': '#FF9933',   # Wh-adverb (Dark Orange)
    'RP': '#FFCC66',    # Particle (Orange)
    'NNPS': '#CC66FF',  # Proper noun, plural (Violet)
    ';': '#66FF99',     # Semicolon (Light Green)
    'JJ': '#99FF99',    # Adjective (Pale Green)
    'POS': '#99FF33',   # Possessive ending (Green)
    'RRB': '#FFCC99',   # Right round bracket (Light Orange)
    'PRP$': '#66CCFF',  # Possessive pronoun (Blue)
    'CC': '#66FFCC',    # Coordinating conjunction (Light Green)
    'VBN': '#99CCFF',   # Verb, past participle (Light Blue)
    'WP': '#FF9966',    # Wh-pronoun (Light Orange)
    ':': '#FFCC00',     # Colon (Yellow)
    'RBS': '#FF99CC',   # Adverb, superlative (Pink)
    'PRP': '#33CCFF',   # Personal pronoun (Light Blue)
    'WP$': '#99FF66',   # Possessive wh-pronoun (Light Green)
    'VBP': '#FF6666',   # Verb, non-3rd person singular present (Red)
    ',': '#FFFF66',     # Comma (Yellow)
    'UH': '#FF9933',    # Interjection (Dark Orange)
    '``': '#FFCC66',    # Opening quotation mark (Orange)
    'CD': '#CCFF66',    # Cardinal number (Light Green)
    'NNS': '#FF99FF',   # Noun, plural (Purple)
}

tag_colors = {
    'B-geo': '#FFCC00',   # Beginning of geographical entity (Yellow)
    'B-gpe': '#FF99CC',   # Beginning of geopolitical entity (Pink)
    'I-art': '#33CCFF',   # Intermediate of artistic entity (Light Blue)
    'B-eve': '#99FF33',   # Beginning of event entity (Green)
    'B-tim': '#FF6699',   # Beginning of time entity (Magenta)
    'I-per': '#FFCC99',   # Intermediate of person entity (Light Orange)
    'I-geo': '#66CCFF',   # Intermediate of geographical entity (Blue)
    'B-org': '#66FFCC',   # Beginning of organization entity (Light Green)
    'O': '#999999',       # No entity tag (Gray)
    'B-art': '#FF9966',   # Beginning of artistic entity (Light Orange)
    'B-per': '#FF6666',   # Beginning of person entity (Red)
    'B-nat': '#99FF66',   # Beginning of natural entity (Pale Green)
    'I-eve': '#FF99FF',   # Intermediate of event entity (Purple)
    'I-gpe': '#CC66FF',   # Intermediate of geopolitical entity (Violet)
    'I-tim': '#66FF99',   # Intermediate of time entity (Light Green)
    'I-nat': '#99FF99',   # Intermediate of natural entity (Pale Green)
    'I-org': '#FF9933',   # Intermediate of organization entity (Dark Orange)
}

pos_meaning = {
    'CC': 'Coordinating conjunction',
    'UH': 'Interjection',
    'VBZ': 'Verb, 3rd person singular present',
    'JJR': 'Adjective, comparative',
    'JJ': 'Adjective',
    '``': 'Opening quotation mark',
    'RBS': 'Adverb, superlative',
    'NN': 'Noun, singular or mass',
    'VBG': 'Verb, gerund or present participle',
    'VBD': 'Verb, past tense',
    'VB': 'Verb, base form',
    'NNP': 'Proper noun, singular',
    'VBN': 'Verb, past participle',
    'NNS': 'Noun, plural',
    'WRB': 'Wh-adverb',
    'EX': 'Existential there',
    'VBP': 'Verb, non-3rd person singular present',
    'FW': 'Foreign word',
    'POS': 'Possessive ending',
    'DT': 'Determiner',
    'RB': 'Adverb',
    'IN': 'Preposition or subordinating conjunction',
    ',': 'Comma',
    'RRB': 'Right round bracket',
    'PRP$': 'Personal pronoun',
    'JJS': 'Adjective, superlative',
    ':': 'Sentence-ending punctuation',
    'NNPS': 'Proper noun, plural',
    'WP': 'Wh-determiner',
    'RBR': 'Adverb, comparative',
    'WP$': 'Possessive wh-pronoun',
    'CD': 'Cardinal number',
    '(': 'Left round bracket'
}

tag_meaning = {
    'B-geo': 'Geographical Entity, Beginning of a Location',
    'B-gpe': 'Geopolitical Entity, Beginning of a Political Entity',
    'I-art': 'Artwork, Inside an Artwork Entity',
    'B-eve': 'Event, Beginning of an Event',
    'B-tim': 'Time Indicator, Beginning of a Time Expression',
    'I-per': 'Person, Inside a Person Entity',
    'I-geo': 'Geographical Entity, Inside a Location',
    'B-org': 'Organization, Beginning of an Organization',
    'O': 'Other, Not Part of Any Entity',
    'B-art': 'Artifact, Beginning of an Artifact Entity',
    'B-per': 'Person, Beginning of a Person Entity',
    'B-nat': 'Nationality, Beginning of a Nationality',
    'I-eve': 'Event, Inside an Event Entity',
    'I-gpe': 'Geopolitical Entity, Inside a Political Entity',
    'I-tim': 'Time Indicator, Inside a Time Expression',
    'I-nat': 'Nationality, Inside a Nationality',
    'I-org': 'Organization, Inside an Organization'
}

def sentence2idx(sentence):
    sentence = sentence.split()
    sentence = [word2idx.get(word, 0) for word in sentence]
    sentence = pad_sequences(maxlen=50, sequences = [sentence], padding='post')
    return sentence


def entity_recognition(sentence, chunk_size):
    target_vocab_size = len(sentence.split())
    predictions = []

    # Chunk the sentence into fixed-size chunks
    chunks = [sentence.split()[i:i+chunk_size] for i in range(0, target_vocab_size, chunk_size)]

    # Generate predictions for each chunk
    for chunk in chunks:
        chunk_sentence = ' '.join(chunk)
        chunk_predictions = generate_chunk_predictions(chunk_sentence)
        predictions.extend(chunk_predictions)

    return predictions


def generate_chunk_predictions(chunk_sentence):
    stc = sentence2idx(chunk_sentence)
    recognitions = model.predict(stc, verbose=0)
    pos_predictions = recognitions[0]
    entity_predictions = recognitions[1]
    word_defn = []

    for i in range(len(chunk_sentence.split())):
        word_dict = {}
        word_dict["Word"] = chunk_sentence.split()[i]
        word_dict["POS"] = idx2pos[str(np.argmax(pos_predictions[0][i]))]
        word_dict["Tag"] = idx2tag[str(np.argmax(entity_predictions[0][i]))]
        word_defn.append(word_dict)

    return word_defn


def preview(prediction_labels, style=1):
    plt.figure(figsize=(28, 28))
    plt.title("Network Graph Extracting knowledge from text")

    # Sample prediction labels
    prediction_labels = prediction_labels[0]
    
    # Create an empty graph
    G = nx.Graph()

    # Add nodes (words) to the graph
    for label in prediction_labels:
        word = label['Word']
        tag = label['Tag']
        pos = label['POS']  
        G.add_node(word, tag=tag, pos=pos)

    # Add edges (connections) based on the same tag
    for i in range(len(prediction_labels) - 1):
        word1 = prediction_labels[i]['Word']
        word2 = prediction_labels[i + 1]['Word']
        tag1 = prediction_labels[i]['Tag']
        tag2 = prediction_labels[i + 1]['Tag']
        G.add_edge(word1, word2, tag=tag1)

    # Draw the network graph
    graph_layout = {
        1 : nx.kamada_kawai_layout(G),
        2 : nx.circular_layout(G),
        3 : nx.spring_layout(G),
        4 : nx.spiral_layout(G) 
    }
    pos = graph_layout[style]
    nx.draw_networkx_nodes(G, pos=pos, node_color=[pos_colors[G.nodes[node]['pos']] for node in G.nodes])
    nx.draw_networkx_labels(G, pos=pos)
    nx.draw_networkx_edges(G, pos=pos, edgelist=[(u, v) for (u, v, attr) in G.edges(data=True) ], edge_color=tag_colors[tag])
    nx.draw_networkx_edges(G, pos=pos, edgelist=[(u, v) for (u, v, attr) in G.edges(data=True) if attr['tag'] == 'O'], edge_color='gray')

    # set legend on top right displaying the different POS  colors and their translations from pos_translation
    legend_handles = []
    legend_labels = []
    for pos, color in pos_colors.items():
        meaning = pos_meaning.get(pos, '')
        label = f'{pos} ({meaning})'
        legend_handles.append(plt.Line2D([], [], marker='o', color=color, label=label))
        legend_labels.append(label)
    
    plt.legend(handles=legend_handles, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # # tag definition
    # # Create legend entries
    # legend_entries = []
    # for tag in tag_colors:
    #     color = tag_colors[tag]
    #     meaning = tag_meaning[tag]
    #     entry = f'{tag} - {meaning}'
    #     legend_entries.append((entry, color))

    # fig, ax = plt.subplots()
    # ax.legend(handles=[plt.Line2D([], [], color=color, marker='o', linestyle='', label=entry) for entry, color in legend_entries])

    plt.axis('off')

    print("**********saving Figure")
    file_tag = random.randint(100, 9999)
    file_name = f'output{file_tag}.png'
    target_location = MEDIA_ROOT + "/" + file_name
    plt.savefig(target_location)
    return MEDIA_URL + file_name
