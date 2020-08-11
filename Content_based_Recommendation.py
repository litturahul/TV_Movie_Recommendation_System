import pandas as pd
import gensim
from gensim import models
from gensim.similarities import MatrixSimilarity

def break_to_tokens(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(token)
    return result


class Recommendation:
    def __init__(self):
        self.movie_data = "data/movie_data.csv"
        self.processed_data = "data/Content_based_recommendation/processed_data.csv"
        self.corpus_dictionary = "data/Content_based_recommendation/content_based_corpus_dictionoary.dict"
        self.tfidf_model = "data/Content_based_recommendation/tfidf_model.model"
        self.matrix_similarity = "data/Content_based_recommendation/similarity.mm"

    def testingpath(self):
        data=pd.read_csv(self.movie_data)
        print(data.columns)
        return "done"

    def pre_process_data(self):
        """
        Reads movie dataset which is created by Data Generation object. Performs data cleaning and returns a data frame
        :return: dataframe
        """
        data = pd.read_csv(self.movie_data)
        data = data[['original_title', 'overview', 'tagline', 'Crew_Cast', 'keywords', 'genres']]
        data = data.fillna(" ")
        data['description'] = data['overview'] + data['tagline']
        del data['overview']
        del data['tagline']
        data['description'] = data['description'].str.replace(
            r"(\.|,|\?|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|;|:|~|`|\d+|\[|\]|{|}|\xA9|\\|\/)", " ")
        data['genres'] = data['genres'].apply(lambda x: x.replace("|", " "))
        data['doc'] = data['description'] + data['genres'] + data['keywords'] + data['Crew_Cast']
        data = data.drop(data.columns[[1, 2, 3, 4]], axis=1)
        try:
            data.to_csv(self.processed_data)
            return "Pre Processing Successful"
        except:
            return "Pre Processing Failed"

    def train_model(self):
        """
        Read the preprocessed data and generate corpus dictionary, tfidf model and matrix(Cosine) similarity
        :return: status of training
        """
        try:
            data = pd.read_csv(self.processed_data)
            del data['Unnamed: 0']
            # creating tokens for the doc column
            corpus = data['doc'].map(break_to_tokens)
            # creating dictionary of words in the movie dataset
            dictionary = gensim.corpora.Dictionary(corpus)
            dictionary.save(self.corpus_dictionary)
            # creating vector with bag of words for the corpus
            vector = [dictionary.doc2bow(d) for d in corpus]
            # creating tfidf values for the vector
            tfidf = models.TfidfModel(vector)
            tfidf.save(self.tfidf_model)
            corpus_tfidf = tfidf[vector]
            # Compute Similarities
            similarity = MatrixSimilarity(corpus_tfidf,num_features=len(dictionary))
            similarity.save(self.matrix_similarity)
            return "Model Trained Successfully"
        except:
            return "Error While Training Model"

    def get_recommendation(self,movie_title:str):
        """
        Accepts Movie Name and fetches the list of recommended movie names using matrix(cosine) similarity
        :param movie_title:
        :return: array of movie names
        """
        print("movie : ",movie_title)
        dictionary = gensim.corpora.Dictionary.load(self.corpus_dictionary)
        tfidf_model = gensim.models.TfidfModel.load(self.tfidf_model)
        similarity = MatrixSimilarity.load(self.matrix_similarity)
        data = pd.read_csv(self.processed_data)

        del data['Unnamed: 0']
        data["original_title"]=data["original_title"].str.lower()
        movie = data.loc[data.original_title == movie_title]
        print(movie)
        if movie.shape[0]==0:
            status = ["Failed to Recommend Movies with existing movie data."]
            return status
        else:
            movie_doc_bow = dictionary.doc2bow(movie['doc'].map(break_to_tokens)[0])
            movie_tfidf = tfidf_model[movie_doc_bow]
            movie_recommendations = pd.DataFrame({'Cosine_sim_values':similarity[movie_tfidf],'title':data.original_title.values}).sort_values(by="Cosine_sim_values",ascending=False)
            top_recommendations = movie_recommendations['title'].head(11)
            return top_recommendations.to_numpy()

