# PA6, CS124, Stanford, Winter 2019
# v.1.0.3
# Original Python code by Ignacio Cases (@cases)
######################################################################
import util

import numpy as np
import re


# noinspection PyMethodMayBeStatic
class Chatbot:
    """Simple class to implement the chatbot for PA 6."""

    def __init__(self, creative=False):
        # The chatbot's default name is `moviebot`.
        # TODO: Give your chatbot a new name.
        self.name = 'moviebot'

        self.creative = creative

        # This matrix has the following shape: num_movies x num_users
        # The values stored in each row i and column j is the rating for
        # movie i by user j
        self.titles, ratings = util.load_ratings('data/ratings.txt')
        self.sentiment = util.load_sentiment_dictionary('data/sentiment.txt')
        self.negations = self.load_negations('deps/negations.txt')
        self.minWordLength = 3
        ########################################################################
        # TODO: Binarize the movie ratings matrix.                             #
        ########################################################################

        # Binarize the movie ratings before storing the binarized matrix.
        #self.ratings = ratings
        self.ratings = self.binarize(ratings)
        ########################################################################
        #                             END OF YOUR CODE                         #
        ########################################################################

    ############################################################################
    # 1. WARM UP REPL                                                          #
    ############################################################################

    def load_negations(self, src_filename: str):
        results = set()
        with open(src_filename, 'r') as f:
            for line in f:
                results.add(line.strip())
        return results

    def greeting(self):
        """Return a message that the chatbot uses to greet the user."""
        ########################################################################
        # TODO: Write a short greeting message                                 #
        ########################################################################

        greeting_message = "How can I help you?"

        ########################################################################
        #                             END OF YOUR CODE                         #
        ########################################################################
        return greeting_message

    def goodbye(self):
        """
        Return a message that the chatbot uses to bid farewell to the user.
        """
        ########################################################################
        # TODO: Write a short farewell message                                 #
        ########################################################################

        goodbye_message = "Have a nice day!"

        ########################################################################
        #                          END OF YOUR CODE                            #
        ########################################################################
        return goodbye_message

    ############################################################################
    # 2. Modules 2 and 3: extraction and transformation                        #
    ############################################################################

    def process(self, line):
        """Process a line of input from the REPL and generate a response.

        This is the method that is called by the REPL loop directly with user
        input.

        You should delegate most of the work of processing the user's input to
        the helper functions you write later in this class.

        Takes the input string from the REPL and call delegated functions that
          1) extract the relevant information, and
          2) transform the information into a response to the user.

        Example:
          resp = chatbot.process('I loved "The Notebook" so much!!')
          print(resp) // prints 'So you loved "The Notebook", huh?'

        :param line: a user-supplied line of text
        :returns: a string containing the chatbot's response to the user input
        """
        ########################################################################
        # TODO: Implement the extraction and transformation in this method,    #
        # possibly calling other functions. Although your code is not graded   #
        # directly based on how modular it is, we highly recommended writing   #
        # code in a modular fashion to make it easier to improve and debug.    #
        ########################################################################
        if self.creative:
            response = "I processed {} in creative mode!!".format(line)


        else:  # STARTER MODE:
            # if not self.started:
            #     response += self.greeting()

            response = "I'm sorry, I'm not sure I understood that. If you are describing a movie, \
                        it'd be great if you could put it in quotes ("") so I make sure I understand \
                        what you mean! Let's discuss movies, one at a time :)"

            yes = ["Yes", "yes", "Yeah", "yeah", "Yep", "yep", "Yup", "yup"]
            no = ["No", "no", "Nah", "nah", "Nope", "nope", "Negative", "negative"]

            if len(self.movies_rated) < 5 and self.num_reccs == 0: 
                ask = ["Can you tell me how you felt about another movie?",
                        "Tell me what you thought of another movie.",
                        "What about another movie?",
                        "What are your thoughts on another movie?",
                        "Besides that, can you tell me what you thought of another movie?",
                        "What's another movie you have thoughts on?",
                        "Can you tell me your reaction to another movie?"]
                rand_ask = ask[random.randint(0,len(ask)-1)]

                titles = self.extract_titles(line)
                if len(titles) == 1:
                    title = titles[0]
                    movie_indices = self.find_movies_by_title(title)

                    if len(movie_indices) == 1: 

                        sentiment = self.extract_sentiment(line)
                        if sentiment <= -1:
                            neg_acknowledgement = ["I see", "Okay", "Hmm", "Got it", "Alright"]
                            rand_neg_acknowledge = neg_acknowledgement[random.randint(0,len(neg_acknowledgement)-1)]

                            dislike = ["didn't like", "weren't a fan of", "disliked", "didn't enjoy", "weren't fond of"]
                            rand_dislike = dislike[random.randint(0,len(dislike)-1)]

                            response = rand_neg_acknowledge + ", you " + rand_dislike + " \"{}\". ".format(title) 
                            
                            if movie_indices[0] not in self.movies_rated:
                                self.movies_rated[movie_indices[0]] = -1

                        elif sentiment >= 1:
                            pos_acknowledgement = ["I see", "Cool", "Awesome", "Got it", "Okay"]
                            rand_pos_acknowledge = pos_acknowledgement[random.randint(0,len(pos_acknowledgement)-1)]

                            like = ["liked", "were a fan of", "liked watching", "enjoyed", "thought well of", "enjoyed watching"]
                            rand_like = like[random.randint(0,len(like)-1)]

                            response = rand_pos_acknowledge + ", you " + rand_like + " \"{}\"! ".format(title) 

                            if movie_indices[0] not in self.movies_rated:
                                self.movies_rated[movie_indices[0]] = 1

                        elif sentiment == 0:
                            neutral_acknowledgement = ["Hmm", "I'm sorry", "Sorry"]
                            rand_neutral_acknowledge = neutral_acknowledgement[random.randint(0,len(neutral_acknowledgement)-1)]

                            unsure = ["unsure whether", "not sure if", "not clear on whether", "not sure whether", "unsure if"]
                            rand_unsure = unsure[random.randint(0,len(unsure)-1)]

                            clarify = ["What did you think of it?", "Tell me more about it.", "What were your thoughts on it?"]
                            rand_clarify = clarify[random.randint(0,len(clarify)-1)]

                            response = rand_neutral_acknowledge + ", I'm " + rand_unsure + " you liked \"{}\". ".format(title) + rand_clarify
                
                        if len(self.movies_rated) < 5 and sentiment != 0:
                            response += rand_ask

                    # else: #TODO: if a movie is provided in quotes, but not in our dataset

                elif len(titles) > 1: #if more than 1 movie was mentioned
                    response = "I'm sorry, since I'm in Starter mode, I only have the capacity to understand one " \
                                "movie at a time, unfortunately. I'd really appreciate if you could list the " \
                                "movies you mentioned with one movie per line. Thank you!"

            #start giving recommendations -- TODO: BUGGY, fix!
            if len(self.movies_rated) >= 5:
                user_ratings = []  # list: gets all indices of users ratings that != 0, and fills with 0s for non-rated
                for i in range(len(self.ratings)):
                    if i in self.movies_rated:
                        user_ratings.append(self.movies_rated[i])
                    else:
                        user_ratings.append(0)

                recc_idx = self.recommend(user_ratings, self.ratings, self.total_reccs_poss, False)
                recc = self.titles[recc_idx[self.num_reccs]][0]
                if self.num_reccs == 0: # give the first movie recommendation
                    response += "\nThanks for your inputs! Given what you told me, I think you would like \"" + recc + "\"!"
                    response += "\nWould you like more recommendations?"
                    self.num_reccs += 1

                elif self.num_reccs < self.total_reccs_poss:
                    if any(item in yes for item in line) and any(item in no for item in line): 
                        response = "I'm sorry, I didn't quite understand. Would you like more recommendations?"
                    elif any(item in yes for item in line):
                        response = "Sure! I would also recommend " + recc + "\"!"
                        response += "\nWould you like more recommendations?"
                        self.num_reccs += 1
                    elif any(item in no for item in line): 
                        response = self.goodbye()
                        
                elif self.num_reccs == self.total_reccs_poss:
                    response = "Actually, I've given you {} movie recommendations above, ".format(self.total_reccs_poss)
                    response += '''I'm sure there must be at least one new movie to try! I don't have more recommendations for now, but 
                                    feel free to come back soon with new reviews! Thanks for chatting with me today!'''
            

        ########################################################################
        #                          END OF YOUR CODE                            #
        ########################################################################
        return response

    @staticmethod
    def preprocess(text):
        """Do any general-purpose pre-processing before extracting information
        from a line of text.

        Given an input line of text, this method should do any general
        pre-processing and return the pre-processed string. The outputs of this
        method will be used as inputs (instead of the original raw text) for the
        extract_titles, extract_sentiment, and extract_sentiment_for_movies
        methods.

        Note that this method is intentially made static, as you shouldn't need
        to use any attributes of Chatbot in this method.

        :param text: a user-supplied line of text
        :returns: original text
        dictionary with at most two entries whose keys are the 
        movies in the text and the values are a list of 'before' strings and
        'after' strings. 'before' strings are words that come before the movie
        and 'after' strings come after.
        """
        ########################################################################
        # TODO: Preprocess the text into a desired format.                     #
        # NOTE: This method is completely OPTIONAL. If it is not helpful to    #
        # your implementation to do any generic preprocessing, feel free to    #
        # leave this method unmodified.                                        #
        ########################################################################

        ########################################################################
        #                             END OF YOUR CODE                         #
        ########################################################################
        
        return text

    def extract_titles(self, preprocessed_input):
        """Extract potential movie titles from a line of pre-processed text.

        Given an input text which has been pre-processed with preprocess(),
        this method should return a list of movie titles that are potentially
        in the text.

        - If there are no movie titles in the text, return an empty list.
        - If there is exactly one movie title in the text, return a list
        containing just that one movie title.
        - If there are multiple movie titles in the text, return a list
        of all movie titles you've extracted from the text.

        Example:
          potential_titles = chatbot.extract_titles(chatbot.preprocess(
                                            'I liked "The Notebook" a lot.'))
          print(potential_titles) // prints ["The Notebook"]

        :param preprocessed_input: a user-supplied line of text that has been
        pre-processed with preprocess()
        :returns: list of movie titles that are potentially in the text
        """
        to_ret = []
        str1 = preprocessed_input
        temp = str1
        while(True):
            str1 = temp
            a = str1.find('"')
            if (a == -1):
                break
            for i in range(a+1, len(str1)):
                if (str1[i] == '"'):
                    b = i 
                    break
            to_ret.append(str1[a+1:b])
            temp = str1[b+1:]
        return to_ret

    def find_movies_by_title(self, title):
        """ Given a movie title, return a list of indices of matching movies.

        - If no movies are found that match the given title, return an empty
        list.
        - If multiple movies are found that match the given title, return a list
        containing all of the indices of these matching movies.
        - If exactly one movie is found that matches the given title, return a
        list
        that contains the index of that matching movie.

        Example:
          ids = chatbot.find_movies_by_title('Titanic')
          print(ids) // prints [1359, 2716]

        :param title: a string containing a movie title
        :returns: a list of indices of matching movies
        """
        matches = []
        year_pattern = '\s\([0-9]{4}\)$' # check if title contains year at the end. Ex: (2009)
        year_index = re.search(year_pattern, title)

        title_pattern = f"\\b{title}\\b"

        # check if year starts with The, A, or An

        if year_index: # if the title contains a year
            if title.startswith("The "): 
                title = title[4:-7] + ', The' + title[-7]
            elif title.startswith("A "): 
                title = title[2:-7] + ', A' + title[-7:]
            elif title.startswith("An "): 
                title = title[3:-7] + ', An' + title[-7:]
            for i in range(len(self.titles)):
                if title == self.titles[i][0]: 
                    matches.append(i)
                    break # for title with a year, there's only 1 match
        else:
            if title.startswith("The "): 
                title = title[4:] + ', The' 
            elif title.startswith("A "): 
                title = title[2:] + ', A' 
            elif title.startswith("An "): 
                title = title[3:] + ', An' 
            for i in range(len(self.titles)):
                if title == self.titles[i][0][:-7] or re.search(title_pattern, self.titles[i][0], re.IGNORECASE):
                    matches.append(i)

        return matches

    def extract_edit_distance_words(self, word):
        for i in range(len(word), self.minWordLength, -1):
            sub_str = word[0: i]
            if sub_str in self.sentiment:
                return sub_str
        return ""

    def apply_negation(self, sentiment, sentiments):
        quote = False
        for word in sentiments:
            if '"' in word or quote:
                quote = False if quote else True
                continue
            if word in self.negations:
                return -1 if sentiment == 1 or sentiment == 0 else 1
        return sentiment

    def extract_sentiment(self, preprocessed_input):
        """Extract a sentiment rating from a line of pre-processed text.

        You should return -1 if the sentiment of the text is negative, 0 if the
        sentiment of the text is neutral (no sentiment detected), or +1 if the
        sentiment of the text is positive.

        As an optional creative extension, return -2 if the sentiment of the
        text is super negative and +2 if the sentiment of the text is super
        positive.

        Example:
          sentiment = chatbot.extract_sentiment(chatbot.preprocess(
                                                    'I liked "The Titanic"'))
          print(sentiment) // prints 1

        :param preprocessed_input: a user-supplied line of text that has been
        pre-processed with preprocess()
        :returns: a numerical value for the sentiment of the text
        """
        words = preprocessed_input.split()
        num_pos = 0
        num_neg = 0
        quote = False
        for word in words:
            if '"' in word or quote:
                quote = False if quote else True
                continue
            if word in self.sentiment:
                if self.sentiment[word] == "pos":
                    num_pos += 1
                else:
                    num_neg += 1
            else:
                p_word = self.extract_edit_distance_words(word)
                if p_word == "": 
                    continue
                if self.sentiment[p_word] == "pos":
                    num_pos += 1
                else:
                    num_neg += 1
        
        sentiment = -1 if num_neg >= 1 else 1
        sentiment = 0 if num_neg == num_pos == 0 else sentiment

        return self.apply_negation(sentiment, words)
        
    def extract_sentiment_for_movies(self, preprocessed_input):
        """Creative Feature: Extracts the sentiments from a line of
        pre-processed text that may contain multiple movies. Note that the
        sentiments toward the movies may be different.

        You should use the same sentiment values as extract_sentiment, described

        above.
        Hint: feel free to call previously defined functions to implement this.

        Example:
          sentiments = chatbot.extract_sentiment_for_text(
                           chatbot.preprocess(
                           'I liked both "Titanic (1997)" and "Ex Machina".'))
          print(sentiments) // prints [("Titanic (1997)", 1), ("Ex Machina", 1)]

        :param preprocessed_input: a user-supplied line of text that has been
        pre-processed with preprocess()
        :returns: a list of tuples, where the first item in the tuple is a movie
        title, and the second is the sentiment in the text toward that movie
        """
        pass
    
    
    
    def get_str_units(self, str):
        '''
        Gets a list of string "units", which would be individual characters of the
        string or a year at the end (eg. (2009)) if applicable.
        :param str: a string, assume is already lowercase
        :returns: a list of string "units", either a character or a year 
        '''
        units = []

        year_pattern = '\s\([0-9]{4}\)$' # check if title contains year at the end. Ex: (2009)
        year_index = re.search(year_pattern, str)
        if year_index:
            year_index = year_index.start()

        str_len = len(str)
        str_idx = 0
        while str_idx < str_len:
            if str_idx == year_index:
                # print(year_index)
                # print(str_idx)
                str_idx += 7
                break
            units.append(str[str_idx])
            str_idx += 1

        return units


    def find_edit_dist(self, source, target):
        source_units = self.get_str_units(source)
        target_units = self.get_str_units(target)

        source_length = len(source_units) 
        target_length = len(target_units)

        dist_matrix = np.zeros((source_length+1, target_length+1))

        for i in range(source_length):
            dist_matrix[i+1][0] = dist_matrix[i][0] + 1 #add deletion cost

        for j in range(target_length):
            dist_matrix[0][j+1] = dist_matrix[0][j] + 1 #add insertion cost

        for i in range(source_length):
            for j in range(target_length):
                if source[i] != target[j]:
                    dist_matrix[i+1][j+1] = min(dist_matrix[i][j+1] + 1,
                                                dist_matrix[i+1][j] + 1,
                                                dist_matrix[i][j] + 2)
                else: 
                    dist_matrix[i+1][j+1] = min(dist_matrix[i][j+1] + 1,
                                                dist_matrix[i+1][j] + 1,
                                                dist_matrix[i][j])

        return dist_matrix[source_length][target_length]
    

    def find_movies_closest_to_title(self, title, max_distance=3):
        """Creative Feature: Given a potentially misspelled movie title,
        return a list of the movies in the dataset whose titles have the least
        edit distance from the provided title, and with edit distance at most
        max_distance.

        - If no movies have titles within max_distance of the provided title,
        return an empty list.
        - Otherwise, if there's a movie closer in edit distance to the given
        title than all other movies, return a 1-element list containing its
        index.
        - If there is a tie for closest movie, return a list with the indices
        of all movies tying for minimum edit distance to the given movie.

        Example:
          # should return [1656]
          chatbot.find_movies_closest_to_title("Sleeping Beaty")

        :param title: a potentially misspelled title
        :param max_distance: the maximum edit distance to search for
        :returns: a list of movie indices with titles closest to the given title
        and within edit distance max_distance
        """

        title_size = len(title)
        title_lowercase = title.lower()

        indices = []
        map_title_idx = {} # map from movie title (key) --> movie index (value)
        map_title_dist = {} # map from movie title (key) --> edit distance (value)

        # for all movie titles in dataset, add their edit distance from title
        for i, source in enumerate((self.titles)):
            source_lowercase = source[0].lower()
            source_size = len(source[0])

            edit_dist = self.find_edit_dist(source_lowercase, title_lowercase)

            if edit_dist <= max_distance:
                map_title_dist[source[0]] = edit_dist
                map_title_idx[source[0]] = i

        # sort dictionary of title->dist by ascending distance
        sorted_map = dict(sorted(map_title_dist.items(), key=lambda item: item[1]))
        titles = list(sorted_map.keys())

        if titles: #if titles list is not empty
            min_dist = map_title_dist[titles[0]]
            idx_increment = 0
            while idx_increment <= len(titles)-1:
                # add any indices that correspond with the least edit distance from title
                dist = map_title_dist[titles[idx_increment]]

                if dist == min_dist: 
                    indices.append(map_title_idx[titles[idx_increment]])
                else:
                    break
                idx_increment += 1

        return indices
    
    

    def disambiguate(self, clarification, candidates):
        """Creative Feature: Given a list of movies that the user could be
        talking about (represented as indices), and a string given by the user
        as clarification (eg. in response to your bot saying "Which movie did
        you mean: Titanic (1953) or Titanic (1997)?"), use the clarification to
        narrow down the list and return a smaller list of candidates (hopefully
        just 1!)

        - If the clarification uniquely identifies one of the movies, this
        should return a 1-element list with the index of that movie.
        - If it's unclear which movie the user means by the clarification, it
        should return a list with the indices it could be referring to (to
        continue the disambiguation dialogue).

        Example:
          chatbot.disambiguate("1997", [1359, 2716]) should return [1359]

        :param clarification: user input intended to disambiguate between the
        given movies
        :param candidates: a list of movie indices
        :returns: a list of indices corresponding to the movies identified by
        the clarification
        """
        identified_indices = []
        year_pattern = '\s\([0-9]{4}\)$' # check if title contains year at the end. Ex: (2009)
        
        ##### For disambiguate part 2: #####
        
        for i in range(len(candidates)):
            candidate_idx = candidates[i]
            candidate_title = self.titles[candidate_idx][0]
            year_found = re.search(year_pattern, candidate_title)
            title_no_year = candidate_title
            if year_found:
                year_index = year_found.start()
                title_no_year = title_no_year[0:year_index]

            clarification_found = re.search(clarification, title_no_year)
            if clarification_found:
                clarification_idx = clarification_found.start()
                identified_indices.append(candidate_idx)


        if not identified_indices and clarification.isnumeric() and len(clarification) == 4:
            for i in range(len(candidates)):
                candidate_idx = candidates[i]
                candidate_title = self.titles[candidate_idx][0]
                clarification_found_yr = re.search(clarification, candidate_title)
                if clarification_found_yr:
                    clarification_idx = clarification_found_yr.start()
                    identified_indices.append(candidate_idx)

        ##### For disambiguate part 3: #####

        if not identified_indices and clarification.isnumeric():
            if int(clarification) <= len(candidates):
                identified_indices.append(candidates[int(clarification)-1])


        if not identified_indices and clarification == "most recent":
            movies_with_years = []
            for i in range(len(candidates)):
                candidate_idx = candidates[i]
                candidate_title = self.titles[candidate_idx][0]
                year_found = re.search(year_pattern, candidate_title)
                if year_found:
                    year_index = year_found.start()
                    movies_with_years.append(candidate_idx)

            if movies_with_years:
                first_movie_idx = movies_with_years[0]
                first_movie_title = self.titles[first_movie_idx][0]
                recent_year = first_movie_title[len(first_movie_title)-8:len(first_movie_title)-1]
                recent_idx = []
                for i, movie_idx in enumerate(movies_with_years):
                    movie_title = self.titles[movie_idx][0]
                    movie_year = movie_title[len(movie_title)-8 : len(movie_title)-1]

                    if movie_year == recent_year:
                        recent_idx.append(movie_idx)
                    elif movie_year > recent_year:
                        recent_idx = []
                        recent_idx.append(movie_idx)

                for i in range(len(recent_idx)):
                    identified_indices.append(recent_idx[i])


        the_one_pattern = '^[tT]he\s(\w+\s)+one$'
        the_one_found = re.search(the_one_pattern, clarification)
        if not identified_indices and the_one_found:
            target = clarification[4:len(clarification)-4]

            for i in range(len(candidates)):
                candidate_idx = candidates[i]
                candidate_title = self.titles[candidate_idx][0]
                clarification_found = re.search(target, candidate_title)
                if clarification_found:
                    clarification_idx = clarification_found.start()
                    identified_indices.append(candidate_idx)

            if not identified_indices and target == "first" and len(candidates) >= 1:
                identified_indices.append(candidates[0])
            elif not identified_indices and target == "second" and len(candidates) >= 2:
                identified_indices.append(candidates[1])
            elif not identified_indices and target == "third" and len(candidates) >= 3:
                identified_indices.append(candidates[2])
            elif not identified_indices and target == "fourth" and len(candidates) >= 4:
                identified_indices.append(candidates[3])
            elif not identified_indices and target == "fifth" and len(candidates) >= 5:
                identified_indices.append(candidates[4])
            elif not identified_indices and target == "sixth" and len(candidates) >= 6:
                identified_indices.append(candidates[5])
            elif not identified_indices and target == "seventh" and len(candidates) >= 7:
                identified_indices.append(candidates[6])
            elif not identified_indices and target == "eighth" and len(candidates) >= 8:
                identified_indices.append(candidates[7])
            elif not identified_indices and target == "ninth" and len(candidates) >= 9:
                identified_indices.append(candidates[8])
            elif not identified_indices and target == "tenth" and len(candidates) >= 10:
                identified_indices.append(candidates[9])


        if not identified_indices: #if there are no matches for the given clarification
            identified_indices = candidates

        return identified_indices
    

    ############################################################################
    # 3. Movie Recommendation helper functions                                 #
    ############################################################################

    @staticmethod
    def binarize(ratings, threshold=2.5):
        """Return a binarized version of the given matrix.

        To binarize a matrix, replace all entries above the threshold with 1.
        and replace all entries at or below the threshold with a -1.

        Entries whose values are 0 represent null values and should remain at 0.

        Note that this method is intentionally made static, as you shouldn't use
        any attributes of Chatbot like self.ratings in this method.

        :param ratings: a (num_movies x num_users) matrix of user ratings, from
         0.5 to 5.0
        :param threshold: Numerical rating above which ratings are considered
        positive

        :returns: a binarized version of the movie-rating matrix
        """
        ########################################################################
        # TODO: Binarize the supplied ratings matrix.                          #
        #                                                                      #
        # WARNING: Do not use self.ratings directly in this function.          #
        ########################################################################

        # The starter code returns a new matrix shaped like ratings but full of
        # zeros.
        binarized_ratings = np.zeros_like(ratings)
        for row_idx, row in enumerate(ratings):
            for col_idx, item in enumerate(row):
                if ratings[row_idx][col_idx] == 0:
                    binarized_ratings[row_idx][col_idx] = 0
                elif ratings[row_idx][col_idx] > threshold:
                    binarized_ratings[row_idx][col_idx] = 1
                else:
                    binarized_ratings[row_idx][col_idx] = -1

        ########################################################################
        #                        END OF YOUR CODE                              #
        ########################################################################
        return binarized_ratings

    def similarity(self, u, v):
        """Calculate the cosine similarity between two vectors.

        You may assume that the two arguments have the same shape.

        :param u: one vector, as a 1D numpy array
        :param v: another vector, as a 1D numpy array

        :returns: the cosine similarity between the two vectors
        """
        ########################################################################
        # TODO: Compute cosine similarity between the two vectors.             #
        ########################################################################
        similarity = np.dot(u,v) / (np.linalg.norm(u) * np.linalg.norm(v))
        ########################################################################
        #                          END OF YOUR CODE                            #
        ########################################################################
        return similarity

    def recommend(self, user_ratings, ratings_matrix, k=10, creative=False):
        """Generate a list of indices of movies to recommend using collaborative
         filtering.

        You should return a collection of `k` indices of movies recommendations.

        As a precondition, user_ratings and ratings_matrix are both binarized.

        Remember to exclude movies the user has already rated!

        Please do not use self.ratings directly in this method.

        :param user_ratings: a binarized 1D numpy array of the user's movie
            ratings
        :param ratings_matrix: a binarized 2D numpy matrix of all ratings, where
          `ratings_matrix[i, j]` is the rating for movie i by user j
        :param k: the number of recommendations to generate
        :param creative: whether the chatbot is in creative mode

        :returns: a list of k movie indices corresponding to movies in
        ratings_matrix, in descending order of recommendation.
        """

        ########################################################################
        # TODO: Implement a recommendation function that takes a vector        #
        # user_ratings and matrix ratings_matrix and outputs a list of movies  #
        # recommended by the chatbot.                                          #
        #                                                                      #
        # WARNING: Do not use the self.ratings matrix directly in this         #
        # function.                                                            #
        #                                                                      #
        # For starter mode, you should use item-item collaborative filtering   #
        # with cosine similarity, no mean-centering, and no normalization of   #
        # scores.                                                              #
        ########################################################################

        # Populate this list with k movie indices to recommend to the user.
        recommendations = []
        
        movie_idx_ratings = {}  #map from key:movie index --> value:rating

        user_rated_indexes = []  # list: gets all indices of users ratings that != 0
        for idx in range(len(user_ratings)):
            if user_ratings[idx] != 0:
                user_rated_indexes.append(idx)

        num_movies = np.asarray(ratings_matrix).shape[0]
        for i in range(num_movies): #for each movie i in the dataset
            summed_rating = 0
            for j, j_idx in enumerate(user_rated_indexes): #loop through list of non-0 indices
                
                cosine_sim = 0
                if (np.linalg.norm(ratings_matrix[i]) * np.linalg.norm(ratings_matrix[j_idx])) != 0:
                    cosine_sim = self.similarity(ratings_matrix[i], ratings_matrix[j_idx])
                else: #denominator for cosine similarity would otherwise be 0
                    cosine_sim = 0

                summed_rating += cosine_sim * user_ratings[j_idx]

            movie_idx_ratings[i] = summed_rating


        # sort movie ratings in reverse descending order; lambda -- sort dictionary by values
        sorted_movie_ratings = dict(sorted(movie_idx_ratings.items(), key=lambda item: item[1], reverse=True))
        movie_indexes = list(sorted_movie_ratings.keys())
        
        user_not_rated_indexes = []
        for idx in range(len(user_ratings)):
            if user_ratings[idx] == 0:
                user_not_rated_indexes.append(idx)

        n = 0
        movie_idx_increment = 0
        while n != k:
            movie_idx = movie_indexes[movie_idx_increment]
            if movie_idx in user_not_rated_indexes: # if in user_not_rated list
                recommendations.append(movie_idx)
                n += 1
            movie_idx_increment += 1

        ########################################################################
        #                        END OF YOUR CODE                              #
        ########################################################################
        return recommendations

    ############################################################################
    # 4. Debug info                                                            #
    ############################################################################

    def debug(self, line):
        """
        Return debug information as a string for the line string from the REPL

        NOTE: Pass the debug information that you may think is important for
        your evaluators.
        """
        debug_info = 'debug info'
        return debug_info

    ############################################################################
    # 5. Write a description for your chatbot here!                            #
    ############################################################################
    def intro(self):
        """Return a string to use as your chatbot's description for the user.

        Consider adding to this description any information about what your
        chatbot can do and how the user can interact with it.
        """
        return """
        Your task is to implement the chatbot as detailed in the PA6
        instructions.
        Remember: in the starter mode, movie names will come in quotation marks
        and expressions of sentiment will be simple!
        TODO: Write here the description for your own chatbot!
        """


if __name__ == '__main__':
    print('To run your chatbot in an interactive loop from the command line, '
          'run:')
    print('    python3 repl.py')
