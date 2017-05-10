from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics
from sklearn.cross_validation import train_test_split
import sklearn.datasets

class classifier:
	def __init__(self, corpus_path):
		self.corpus_path = corpus_path #path to the dialogue act corpus, e..g SWDA
		self.vectorizer = TfidfVectorizer(binary=True)

	def train(self, path):
	    #just loading and training the model here
	    dataset = sklearn.datasets.load_files(path, shuffle=True)
	    # dataset = sklearn.datasets.load_files(path, shuffle=True)

	    #split into train and test
	    print ('Split data into training and testing')
	    X_train, X_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.25, random_state=33)
	    self.labels = dataset.target_names
	    #classifier.fit(X_train, y_train)
	    X_train_tf = self.vectorizer.fit_transform(X_train)

	    #build full matrix
	    full_matrix_train = X_train_tf.todense()
	    self.model = BernoulliNB().fit(full_matrix_train, y_train)

	    print ('Train done')

	    (score, pred) = self.run_classifier(X_test, y_test)
	    print(score)
	    print(pred)
	    self.evaluate(pred, y_test)

	def run_classifier(self, X_test, y_test):
	    """TODO: Do some kind of machine learning to classify the utterances we care about"""
	    X_test_tf = self.vectorizer.transform(X_test)
	    full_test_matrix = X_test_tf.todense()
	    score = self.model.score(full_test_matrix, y_test)
	    pred = self.model.predict(full_test_matrix)

	    return score, pred

	def evaluate(self, predictions, y_test):
	    print((metrics.classification_report(y_test, predictions, target_names=self.labels)))
	    #return np.mean(predictions==self.test.target)

if __name__ == "__main__":
	cl = classifier('corpus_modified/')
	cl.train('corpus_modified/')
