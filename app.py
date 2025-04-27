from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)  # <-- ESTA LINHA aqui libera o CORS!!

nlp = spacy.load('pt_core_news_sm')

traducao_pos = {
    'PRON': 'Pronome',
    'VERB': 'Verbo',
    'NOUN': 'Substantivo',
    'ADJ': 'Adjetivo',
    'ADV': 'Advérbio',
    'DET': 'Determinante',
    'ADP': 'Preposição',
    'CCONJ': 'Conjunção',
    'SCONJ': 'Conjunção Subordinativa',
    'INTJ': 'Interjeição',
    'NUM': 'Numeral',
    'PUNCT': 'Pontuação',
    'PROPN': 'Nome Próprio',
    'X': 'Outro/Desconhecido'
}

@app.route('/analisar', methods=['POST'])
def analisar():
    data = request.get_json()
    texto = data.get('texto', '')
    doc = nlp(texto)

    resultado = []

    for sent in doc.sents:
        sent_resultado = []
        for token in sent:
            if not token.is_punct:
                sent_resultado.append({
                    'palavra': token.text,
                    'classe': token.pos_,
                    'classe_pt': traducao_pos.get(token.pos_, 'Desconhecido')
                })
        resultado.append({
            'frase': sent.text,
            'tokens': sent_resultado
        })

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
