# Mental Health Support Chatbot: Semantic Intent Matching

A retrieval-based NLP chatbot that matches a user's message to the closest known intent using sentence embeddings, then replies with a varied, supportive response. It includes a tuned confidence threshold, a crisis-safety layer, and an evaluation against a TF-IDF baseline.

> **Disclaimer:** This is a student project. It is not a medical tool and is not a substitute for a mental health professional. If you or someone you know is in crisis, contact local emergency services or a mental health hotline.

## Results

| Model | LOO accuracy | LOO macro-F1 | Paraphrase accuracy |
|---|---|---|---|
| TF-IDF baseline | 56.3% | 53.9% | 60.0% |
| **MiniLM embeddings** | **69.8%** | **65.5%** | **86.7%** |

- **Leave-one-out (LOO):** each example pattern is used as a query against all the others. Only intents with 2+ patterns are evaluated.
- **Paraphrase accuracy:** 30 hand-written sentences that are not in the dataset, each labelled with its expected intent.
- **Confidence threshold (0.38):** answers 97% of in-scope inputs at 71% accuracy, and rejects 9 of 10 out-of-scope inputs with a fallback reply.

The embedding model beats the baseline by about 27 points on paraphrases, because it matches on meaning rather than shared words.

## How it works
1. **Clean the data:** fix broken characters in `intents.json`, remove an empty pattern, replace a placeholder reply, and remove a foreign phone number and locale-specific statistic.
2. **Retrieve:** encode all example patterns, then pick the most similar one for each message using cosine similarity.
   - Baseline: TF-IDF with character n-grams
   - Main model: Sentence-Transformers `paraphrase-MiniLM-L6-v2`
3. **Threshold and fallback:** below the tuned similarity threshold, the bot asks the user to say more instead of guessing. The threshold maximises correct answers accepted plus out-of-scope inputs rejected.
4. **Crisis-safety layer:** self-harm language triggers a fixed support message with local resources *before* retrieval runs, so it can't be missed by a low similarity score.
5. **Response selection:** a random reply within the matched intent, never the same reply twice in a row.

## Project structure
```
.
├── Mental_Health_Chatbot.ipynb   # full pipeline: cleaning, models, evaluation, chatbot
├── intents.json                  # intents, example patterns, and responses
├── requirements.txt
└── README.md
```

## Run it

**Locally**
```bash
pip install -r requirements.txt
jupyter notebook Mental_Health_Chatbot.ipynb   # Run All
```

**Google Colab:** upload the notebook and `intents.json`, uncomment the `!pip install` line in the first code cell, and run all cells. A GPU isn't needed.

For a live command-line chat, set `RUN_INTERACTIVE = True` in section 9 and run that cell. Type `quit` to stop.

## Limitations
- Replies are pre-written, not generated, so the bot can't handle situations outside its intents.
- Many intents have only 1 to 3 example patterns, and some are close in meaning (for example sad, depressed, worthless), which limits leave-one-out accuracy.
- The test set is small (30 sentences), and the threshold is tuned on the same data it is evaluated on, so the coverage figure is optimistic.
- A few nonsense inputs can still slip past the threshold and get a generic intent reply.
- Crisis detection is keyword-based and will miss indirect phrasing.
- The crisis helpline numbers should be verified before any real deployment.

## Next steps
- Fine-tune a classifier on a public emotion dataset (for example GoEmotions) and compare it with this baseline by macro-F1.
- Build a larger, independent test set.
- Add a Streamlit interface.

## Author
Zeyad ElMorshedi, Computer Engineering student, Alexandria University
[LinkedIn](https://www.linkedin.com/) · [GitHub](https://github.com/Zeyad-005)
