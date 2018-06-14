import sys, os, django, random, psycopg2, json, sqlite3, abc
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERTICAL = 'V'
HORIZONTAL = 'H'
VERTICAL_NUMBER = 0
HORIZONTAL_NUMBER = 1
BLOCKED_POSITION = 'XXXX'
DBENGINE_POSTGRE = 'POSTGRE'
DBENGINE_SQLITE = 'SQLITE'

SQL_BASE_POSTGRE = \
'''
select text 
  from "Word"
where length(text) < %s
'''


CONFIG = {
    "db_engine" : DBENGINE_SQLITE,
    "db_config" : {"NAME": "mylanguage", "USER":"mylanguage", "HOST": "46.101.27.52", "PASSWORD":"ufoVarginhaOvini"},
    "db_sqlite_path": os.path.join(BASE_DIR, 'db.sqlite3')
}


'''
  To choose the direction aleatory(vertically or horizontally)
  Get an aleatory number less than 6 for be the horizontal position
  Get an aleatory number less than 6 for be the vertical position
  Get an word with length less than 12 minus the aleatory number chosen for the direction 
'''


class DataBaseInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_connection_string(self):
        pass
    
    @abc.abstractmethod
    def initalize_db(self):
        pass

    @abc.abstractclassmethod
    def exec_sql(self, sql):
        pass
    
    @abc.abstractclassmethod
    def get_base_sql(self):
        pass
    
class BaseConcreteDb(object):
    cursor = None
    def exec_sql(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(sql)
            raise Exception(e)
        
class PostgreCommand(BaseConcreteDb, DataBaseInterface):
    def __init__(self):
        self.__cursor = None
        self.initalize_db()
    
    def get_connection_string(self):
        dbconf = CONFIG["db_config"]                
        return "dbname='%s' user='%s' host='%s' password='%s'" % (dbconf["NAME"], dbconf["USER"],
            dbconf["HOST"], dbconf["PASSWORD"]) 
    
    def initalize_db(self):
        conn = psycopg2.connect(self.get_connection_string())
        self.cursor = conn.cursor()
    
    def get_base_sql(self):
        return SQL_BASE_POSTGRE


class SqliteCommand(BaseConcreteDb, DataBaseInterface):
    def __init__(self):
        self.initalize_db()

    def get_connection_string(self):
        return CONFIG["db_sqlite_path"]
        
    def initalize_db(self):
        conn = sqlite3.connect(self.get_connection_string())
        self.cursor = conn.cursor()
    
    def get_base_sql(self):
        return SQL_BASE_POSTGRE


class DbCommandFactory(object):

    def __get_postgre_command(self):
        return PostgreCommand()

    def __get_sqlite_command(self):
        return SqliteCommand()
    
    @classmethod
    def get_command(cls):
        if CONFIG["db_engine"] == DBENGINE_POSTGRE:
            return cls.__get_postgre_command(cls)
        elif CONFIG["db_engine"] == DBENGINE_SQLITE:
            return cls.__get_sqlite_command(cls)
        else:
            return None

class CrossWords(object):
    def __init__(self, horizontal_cells_count, vertical_cells_count, db_command):
        if not isinstance(db_command, DataBaseInterface) : raise Exception('db_command must be an DatabaseInterface instance.')
        
        self.horizontal_cells_count = horizontal_cells_count
        self.vertical_cells_count = vertical_cells_count                
        self.__db_command = db_command
        self.reset_game_parameters()

    @property
    def words_matrix(self):
        return self.__words_matrix
    
    def reset_game_parameters(self):
        self.__words_on_game = []
        self.__coordinates = []
        self.__words_matrix = []
        self.__failures = 0
        self.__min_failures = 5000
        self.__max_failures = 6000
        self.__last_direction_number = None
        self.__occupied_positions_already_reused = []
        self.__empty_positions_already_reused = []
        self.__last_two_directions = []
        self.__last_word_positions = []
        self.__all_words_possitions = {}
        self.__force_use_last_word = False
        self.__try_last_time = False    
        self.construct_matrix()

    def get_words_on_db(self, max_size, tuple_tuple_letter_position = ()):
        sql = self.get_sql(max_size, tuple_tuple_letter_position)
        try:
            return self.__db_command.exec_sql(sql)
        except:
            return []

    def get_not_in_sql(self):
        if len(self.__words_on_game) == 1 :
            return " and text not in ('" + str(self.__words_on_game[0]) + "')"
        elif  len(self.__words_on_game) > 1:
            return " and text not in " + str(tuple(self.__words_on_game))
        else:
            return ""

    def get_sql(self, max_size, tuple_tuple_letter_position = ()):
        sql = self.__db_command.get_base_sql() % (max_size) 
        LETTER_POSITION_INDEX = 1
        LETTER_INDEX = 0        

        for filter in tuple_tuple_letter_position:
            if filter:
                sql += ' and (substr(text, %s, 1) = \'%s\'  or  %s > %s ) ' % (str(filter[LETTER_POSITION_INDEX]),  
                    filter[LETTER_INDEX], str(filter[LETTER_POSITION_INDEX]), str(max_size))
        
        sql += self.get_not_in_sql()
        return sql
    
    
    def construct_matrix(self):
        self.__words_matrix = []
        for a in range(0, self.horizontal_cells_count):
            for b in range(0, self.vertical_cells_count):
                self.__words_matrix.append([])
                self.__words_matrix[a].append(None)


    def get_direction(self):
        if not self.__last_direction_number:
            direction_number = random.randrange(0,2)
        else:
            if self.__last_direction_number == 0:
                direction_number = 1
            else:
                direction_number = 0
        if direction_number == VERTICAL_NUMBER:
            return VERTICAL
        elif direction_number == HORIZONTAL_NUMBER:
            return HORIZONTAL
    
    def __appendDirection(self, direction):
        
        if len(self.__last_two_directions) < 2:
            self.__last_two_directions.append(direction)
        else:
            self.__last_two_directions = [direction]
    
    def direction_is_acceptable_now(self, direction):
        if len(self.__last_two_directions) < 2:
            return True
        else:
            if self.__last_two_directions[0] == direction and self.__last_two_directions[1] == direction:
                return False
            else:
                return True

    def get_position(self, empty):
        for a in range(0, self.horizontal_cells_count):
            for b in range(0, self.vertical_cells_count):
                position = self.__words_matrix[a][b]
                if empty:
                    if not position and not ([a,b] in self.__empty_positions_already_reused):    
                        return [a+1, b+1]
                else:
                    if (position) and (position !=BLOCKED_POSITION) and not ([a,b] in self.__occupied_positions_already_reused):
                        return [a+1, b+1]
        return None

    def get_empty_position(self):
        pos = self.get_position(empty=True)        
        self.__empty_positions_already_reused.append(pos)
        return pos
        
    def get_occupied_position(self):
        pos =  self.get_position(empty=False)
        self.__occupied_positions_already_reused.append(pos)
        return pos
        
    def get_positions_based_on_last_word(self):
        limit = len(self.__last_word_positions)
        index = random.randrange(0, limit)
        return list(self.__last_word_positions[index])
    
    def get_positions_based_in_some_used_word(self):
        limit = len(self.__coordinates)
        index = random.randrange(0, limit)
        coordinate = self.__coordinates[index]
        self.put_word_on_positions(coordinate["x"], coordinate["y"], coordinate["word"], coordinate["orientation"])
        return self.get_positions_based_on_last_word()
    
    def get_postion_near_some_word(self):
        pos = self.get_positions_based_in_some_used_word()
        x, y = pos[0], pos[1]
        if self.__last_direction_number == VERTICAL_NUMBER:
            direction = HORIZONTAL
        else:
            direction = VERTICAL
       
        if direction == HORIZONTAL:
            x = random.randrange(0, x+1)
        else:
            y = random.randrange(0,y+1)
        
        return [x, y]
        

    def get_initial_positions(self, force_aleatory=False):
        if force_aleatory:
            return [self.get_initial_position(HORIZONTAL), self.get_initial_position(VERTICAL)]
        else:
            return self.get_positions_based_on_last_word()                    

    def get_initial_position(self, vertical_horizontal):
        limit = 6
        if self.min_failures_reached():
            reductor = 2
        else:
            reductor = 5
        if vertical_horizontal == VERTICAL:
            limit = self.vertical_cells_count - reductor
        elif vertical_horizontal == HORIZONTAL:
            limit = self.horizontal_cells_count - reductor
        
        return random.randrange(1, limit + 1)
    
                
    def get_word(self, max_size, tuple_tuple_letter_position = ()):
        words = self.get_words_on_db(max_size, tuple_tuple_letter_position)
        max_index = len(words) -1
        if max_index > 0 :
            return words[random.randrange(0, max_index)][0]
        else:
            return ""

    def get_word_for_derterminate_position(self, direction, x, y):
        max_length = 0        
        filter = []

        if direction == VERTICAL:
            max_length =  self.vertical_cells_count - x    
            for a in range(0, max_length):
                letter = self.__words_matrix[x + a -1][y-1]
                if letter:
                    if letter == BLOCKED_POSITION:
                        max_length = a
                        break
                    else:
                        filter.append((letter, a +1))
        elif direction == HORIZONTAL:
            max_length = self.horizontal_cells_count - y
            for a in range(0, max_length):
                letter = self.__words_matrix[x-1][y + a-1]
                if letter:
                    if letter == BLOCKED_POSITION:
                        max_length = a
                        break
                    else:
                        filter.append((letter,a + 1))
                          
        word =  self.get_word(max_length, tuple(filter))
        if word in self.__words_on_game:
            return None
        else:
            return word
    
    def position_before_first_letter_is_available(self, direction, x, y):
        if direction == VERTICAL:
            if (x -2) < 0:
                return True
            return self.__words_matrix[x - 2][y-1] in [None, BLOCKED_POSITION]
        elif direction == HORIZONTAL:
            if (y -2) < 0: 
                return True
            return  self.__words_matrix[x -1][y-2] in [None, BLOCKED_POSITION]
    
    def position_after_last_letter_is_available(self, direction, x, y, word_lenth):
        if direction == VERTICAL:
            if x + word_lenth > self.vertical_cells_count:
                return True
            return self.__words_matrix[x + word_lenth-1][y-1] in [None, BLOCKED_POSITION]
        elif direction == HORIZONTAL:
            if y + word_lenth > self.horizontal_cells_count:
                return True
            return self.__words_matrix[x -1][y + word_lenth -1] in [None, BLOCKED_POSITION]
        
    
    def lock_position_before_first_letter(self, direction, x, y):
        if direction == VERTICAL:
            self.__words_matrix[x -2][y-1]  = BLOCKED_POSITION
        elif direction == HORIZONTAL:
            self.__words_matrix[x -1][y-2]  = BLOCKED_POSITION
    
    def is_finalizing(self):
        return False
    
    def word_has_interceptions(self, word):
        positions = self.__all_words_possitions[word]
        for lword in self.__all_words_possitions:
            if lword != word:
                for pos in positions:
                    if pos in self.__all_words_possitions[lword]:
                        return True
        
        return False
            
    def clear_word_positions(self, word):
        positions = self.__all_words_possitions[word]
        for pos in  positions:
            self.set_value_on_position(pos[0], pos[1], None)
    
    def remove_word_from_game(self, word):
        self.clear_word_positions(word)
        self.__words_on_game.remove(word)
        for coordinate in self.__coordinates:
            if coordinate["word"] == word:
                self.__coordinates.remove(coordinate)
                break

    def put_word_on_positions(self, x, y, word, direction):
        if not self.is_finalizing():
            self.__last_word_positions.clear()
        word_letter_positions = []
        if direction == VERTICAL:
            for i in range(0, len(word)):
                self.__words_matrix[x + i-1][y-1] = word[i] 
                word_letter_positions.append((x + i, y))
                if not self.is_finalizing():
                    self.__last_word_positions.append((x + i, y))
        else:
            for i in range(0, len(word)):
                self.__words_matrix[x-1][y + i-1] = word[i] 
                word_letter_positions.append((x, y + i))
                if not self.is_finalizing():
                    self.__last_word_positions.append((x, y + i))
        
        self.__all_words_possitions.update({word:word_letter_positions})

        self.__words_on_game.append(word)

    def set_value_on_position(self, x, y, value):
        self.__words_matrix[x-1][y-1] = value
    
    def block_position(self, x, y):
        self.set_value_on_position(x, y, BLOCKED_POSITION)
    
    def min_failures_reached(self):
        return self.__failures >= self.__min_failures

    
    def __get_position(self, force_aleatory):
        positions =  self.get_initial_positions(force_aleatory)
        if positions:
            x = positions[0]
            y = positions[1]
        else:
            self.__failures = self.__max_failures
            x, y = None, None
        
        return x, y
         
    
    def __inverse_direction(self, direction):
        if direction == VERTICAL:
            direction = HORIZONTAL
        else:
            direction = VERTICAL
        return direction
    
    def include_word_on_game(self, word, x, y, direction, force_aleatory):
        if word:
            if direction == VERTICAL:
                if (x -2) >= 0: 
                    if self.position_before_first_letter_is_available(direction, x, y):
                        self.lock_position_before_first_letter(direction, x, y)
                    else:
                        return None

                if x + len(word) <= self.vertical_cells_count: 
                    if self.position_after_last_letter_is_available(direction, x, y, len(word)):
                        self.block_position(x + len(word), y)
                    else:
                        return None

                self.put_word_on_positions(x, y, word, direction)

            elif direction == HORIZONTAL:
                if (y -2) >= 0: 
                    if self.position_before_first_letter_is_available(direction, x, y):
                        self.lock_position_before_first_letter(direction, x, y)
                    else:
                        return None

                if y + len(word) <= self.horizontal_cells_count: 
                    if self.position_after_last_letter_is_available(direction, x, y, len(word)):
                        self.__words_matrix[x + -1 ][y + len(word)-1] = BLOCKED_POSITION
                    else:
                        return None

                self.put_word_on_positions(x, y, word, direction)

            print(word)

            self.__coordinates.append({"x": x, "y": y, "orientation": direction, "word": word }) 
            self.__appendDirection(direction)   

            self.__force_use_last_word = False    
            
            if direction == HORIZONTAL:
                self.__last_direction_number = HORIZONTAL_NUMBER
            else:
                self.__last_direction_number = VERTICAL_NUMBER
            
            return word
        else:
            if self.min_failures_reached():
                self.block_position(x, y)                    

            self.__failures += 1
            return None


    def get_aleatory_coordinate(self, force_aleatory):
        x, y = self.__get_position(True)
        if not x:
            return None
    
        direction =  self.get_direction()  
        word = self.get_word_for_derterminate_position(direction, x, y)
        if not word:
            direction = self.get_direction()
            word = self.get_word_for_derterminate_position(direction, x, y)            

        first_word = self.include_word_on_game(word, x, y, direction, True)

        #finding a match
        if first_word:
            last_word = None
            word = None
            found  = False
            for i in range(0, 20):
                x, y = self.__get_position(False)
                direction = self.get_direction()                  
                word = self.get_word_for_derterminate_position(direction, x, y)
                if word:
                    last_word = self.include_word_on_game(word, x, y, direction, False)
                    if last_word:
                        found = True
                        break
            
            if not found:
                self.remove_word_from_game(first_word)
    
    def generate(self):
        self.reset_game_parameters()
        how_many_aleatory = 0
        while True:
            self.get_aleatory_coordinate(False)
            if self.__failures >= self.__max_failures:
                if how_many_aleatory < 2 and len(self.__words_on_game) < 21:
                    how_many_aleatory += 1
                    self.__failures = 0
                    self.get_aleatory_coordinate(True)
                else:     
                    self.__try_last_time = True
                    self.get_aleatory_coordinate(False)                   
                    break


        return self.__coordinates 
    
    def generate_many(self, how_many_games):
        games = []
        for i in range(0, how_many_games):            
            games.append(self.generate())
        
        return games

def run():
    begin_time = datetime.now()
    cw = CrossWords(12, 12, DbCommandFactory.get_command())

    for g in range(87, 101):
        game = cw.generate()
        with open(os.path.join(BASE_DIR, 'extra-db-files', 'english', 'crosswords', str(g) + '-crossword.json'), 'w') as f:
            f.write(json.dumps(game, indent=4) )        
    
    end_time = datetime.now()
    print('Lições criadas: Inicio: %s, Fim: %s' % (str(begin_time), str(end_time)))

if __name__ == "__main__":
    run()