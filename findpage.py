import streamlit as st
import pandas as pd
from gensim.models.wrappers.ldamallet import malletmodel2ldamodel
from gensim.models import LdaModel
import template

name = 'Find TV program'

file_tv_programs_and_episodes = 'data/tv_programs_and_episodes.csv'
file_lda_model = 'models/_lda_model_70'
file_topic_distribution = 'data/recommendations_topics_70.csv'


def app():
    # load npo data
    df_tvnz = pd.read_csv(file_tv_programs_and_episodes)

    # show example when user opens the interface for the first time so he/she gets to see some examples
    example_keys = ' '.join(['food', 'cook', 'baker'])

    # only render input field when user chooses ALL, so not when user selects a TV program button
    entered_keys = st.text_input('Describe a content in keywords', '', placeholder='Example ' + example_keys)

    found = None

    if len(entered_keys) > 0: # when chosen ALL and entered key inputs
        found = similar_content(entered_keys.split(' '), df_tvnz)
    else: # when ALL but not entered key inputs yet then show examples
        found = similar_content(example_keys.split(' '), df_tvnz)

    st.caption('')

    # Render result as a grid layout
    template.recommendations_content(found.iloc[:5])
    template.recommendations_content(found.iloc[5:])


def similar_content(entered_keys, df_tvnz):
    # load pre-trained LDA Mallet model
    lda = LdaModel.load(file_lda_model)
    # Transform LDA Mallet to LDA model to get the id2word
    lda_model = malletmodel2ldamodel(lda)

    common_dictionary = lda_model.id2word
    unseen_doc = common_dictionary.doc2bow(entered_keys)

    # get predicted vector
    vector = lda_model[unseen_doc]
    # get the highest probability topic
    best_topic = pd.DataFrame(vector, columns=['topic', 'proba']).sort_values(by='proba', ascending=False).iloc[0, 0]

    # load contents X topic csv
    topic_distributions = pd.read_csv(file_topic_distribution)

    # get top 10 contents
    docs = topic_distributions.iloc[:, [0, 1, best_topic+2]].sort_values(by=f'{best_topic}', ascending=False)[:10]

    # display what the algorithm things by rendering the top 10 words within the topic
    words = [word[0] for word in lda.show_topic(best_topic, topn=10)]
    st.caption(f'The algorithm thinks: {words}')

    # get the contents from NPO to display
    found = df_tvnz.iloc[docs.iloc[:, 0]]

    return found