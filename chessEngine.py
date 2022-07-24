import chess
import chess.polyglot

class chessEngine:

    def __init__ (self):
        self.board = chess.Board()
        self.board.turn = chess.WHITE
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 999999
        }
        
        self.pawn_table = [
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [5.0, 10.0, 10.0, -20.0, -20.0, 10.0, 10.0,  5.0],
            [5.0, -5.0, -10.0, 0.0,  0.0, -10.0, -5.0,  5.0],
            [0.0,  0.0,  0.0,  20.0,  20.0,  0.0,  0.0,  0.0],
            [5.0,  5.0, 10.0, 25.0, 25.0, 10.0,  5.0,  5.0],
            [10.0, 10.0, 20.0, 30.0, 30.0, 20.0, 10.0, 10.0],
            [50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ]
        self.knight_table = [
            [-50.0, -40.0, -30.0, -30.0, -30.0, -30.0, -40.0, -50.0],
            [-40.0, -20.0, 0.0,  0.0,  0.0,  0.0, -20.0, -40.0],
            [-30.0, 5.0,  10.0, 15.0, 15.0, 10.0, 0.0,  -30.0],
            [-30.0, 0.0,  10.0, 15.0, 15.0, 10.0, 0.0,  -30.0],
            [-30.0, 5.0,  10.0, 15.0, 15.0, 10.0, 0.0,  -30.0],
            [-30.0, 0.0,  10.0, 15.0, 15.0, 10.0, 0.0,  -30.0],
            [-40.0, -20.0, 0.0,  0.0,  0.0,  0.0, -20.0, -40.0],
            [-50.0, -40.0, -30.0, -30.0, -30.0, -30.0, -40.0, -50.0]         
        ]
        self.bishop_table = [
            [-20.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -20.0],
            [-10.0, 5.0,  0.0,  0.0,  0.0,  0.0,  5.0,  -10.0],
            [-10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -10.0],
            [-10.0, 0.0,  10.0, 10.0, 10.0, 10.0, 0.0,  -10.0],
            [-10.0, 5.0,  5.0,  10.0, 10.0, 5.0,  5.0,  -10.0],
            [-10.0, 0.0,  10.0, 10.0, 10.0, 10.0, 0.0,  -10.0],
            [-10.0, 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  -10.0],
            [-20.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -20.0]
            
            
        ]
        self.rook_table = [
            [0.0,  0.0,  0.0,  5.0,  5.0,  0.0,  0.0,  0.0],
            [-5.0, 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  -5.0],
            [-5.0, 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  -5.0],
            [-5.0, 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  -5.0],
            [-5.0, 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  -5.0],
            [-5.0, 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  -5.0],
            [5.0,  10.0,  10.0,  10.0,  10.0,  10.0,  10.0,  5.0],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]

            
        ]
        self.queen_table = [
            [-20.0, -10.0, -10.0, -5.0, -5.0, -10.0, -10.0, -20.0],
            [-10.0, 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  -10.0],
            [-10.0, 5.0,  5.0,  5.0,  5.0,  5.0,  0.0,  -10.0],
            [0.0,  0.0,  5.0,  5.0,  5.0,  5.0,  0.0,  -5.0],
            [-5.0, 0.0,  5.0,  5.0,  5.0,  5.0,  0.0,  -5.0],
            [-10.0, 0.0,  5.0,  5.0,  5.0,  5.0,  0.0,  -10.0],
            [-10.0, 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  -10.0],
            [-20.0, -10.0, -10.0, -5.0, -5.0, -10.0, -10.0, -20.0]

            
        ]
        self.king_table = [
            [20.0, 30.0,  10.0,  0.0,  0.0,  10.0,  30.0,  20.0],
            [20.0, 20.0,  0.0,  0.0,  0.0,  0.0,  20.0,  20.0],
            [-10.0, -20.0, -20.0, -20.0, -20.0, -20.0, -20.0, -10.0],
            [-20.0, -30.0, -30.0, -40.0, -40.0, -30.0, -30.0, -20.0],
            [-30.0, -40.0, -40.0, -50.0, -50.0, -40.0, -40.0, -30.0],
            [-30.0, -40.0, -40.0, -50.0, -50.0, -40.0, -40.0, -30.0],
            [-30.0, -40.0, -40.0, -50.0, -50.0, -40.0, -40.0, -30.0],
            [-30.0, -40.0, -40.0, -50.0, -50.0, -40.0, -40.0, -30.0]

        ]

        self.piece_table = {
            1 : self.pawn_table,
            2 : self.knight_table,
            3 : self.bishop_table,  
            4 : self.rook_table,
            5 : self.queen_table,
            6 : self.king_table
        }
        
        
    
    # The material score is calculated by the summation of all respective piece’s 
    # weights multiplied by the difference between the number of that respective piece 
    # between white and black
    def material_evaluation(self):
        score = 0
        for i in range(1, 7):
            score += len(self.board.pieces(i, chess.WHITE)) * self.piece_values[i]
            score -= len(self.board.pieces(i, chess.BLACK)) * self.piece_values[i]
        return score
    
    # The individual pieces score is the sum of piece-square values of positions where 
    # the respective piece is present at that instance of the game.
    def individual_piece_evaluation(self, ptype):
        score = 0
        score += sum([self.piece_table[ptype][i//8][i%8] for i in self.board.pieces(ptype, chess.WHITE)])
        score += sum([- self.piece_table[ptype][chess.square_mirror(i)//8][chess.square_mirror(i)%8] for i in self.board.pieces(ptype, chess.BLACK)])
      
        return score
    
    # the evaluation function which will return the summation of the material scores and the individual
    #  scores for white and when it comes for black, let’s negate it.
    def evaluation(self):
        score = self.material_evaluation()
        for i in range (1,7):
            for piece in self.board.pieces(i, chess.WHITE):
                score += self.individual_piece_evaluation(i)

        # if the side to move is black, then the score is the negative of the score
        if self.board.turn == chess.BLACK:
            score = -score

        return score

    # check if checkmate
    def isCheckmate(self):
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                return -9999
            else:
                return 9999
        return 0
    
    def isStalemate(self):
        if self.board.is_stalemate():
            return 1
        return 0
        
    
    def isInsufficientMaterial(self):
        if self.board.is_insufficient_material():
            return 1
        return 0

    # Move selection using min max algorithm
    # For the smartness of our engine, we can use the initial moves
    # from a book in which moves will be stored with a lot of opening
    # moves by chess Grandmasters in a bin format.
    # 
    def quiescenceSearch(self, alpha, beta):
        
        evaluation = self.evaluation()
        if evaluation >= beta:
            return beta
        if alpha < evaluation:
            alpha = evaluation
        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move)
                evaluation = -self.quiescenceSearch(-beta, -alpha)
                self.board.pop()
                if evaluation >= beta:
                    return beta
                if alpha < evaluation:
                    alpha = evaluation
        return alpha

    def alphaBeta(self, alpha, beta, depth):
        bestScore = -9999
        # bestMove = None
        if depth == 0:
            # quiescence search:
            # if the depth is 0, then we will only search for the best move so that
            # we can avoid the overhead of the full search algorithm.
            return self.quiescenceSearch(alpha, beta)
        
        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move)
                evaluation = -self.alphaBeta(-beta, -alpha, depth - 1)
                self.board.pop()

                if evaluation >= beta:
                    return evaluation

                if alpha < evaluation:
                    alpha = evaluation

                if evaluation > bestScore:
                    bestScore = evaluation
                    # bestMove = move

        return bestScore




    def minmax(self, depth = 4):
        best_move = chess.Move.null()
        best_score = -9999
        alpha = -100000 # alpha is the best score for the maximizing player
        beta = 100000 # beta is the best score for the minimizing player
        for move in self.board.legal_moves:
            self.board.push(move)
            board_score = -self.alphaBeta(-beta, -alpha, depth - 1)
            if board_score > best_score:
                best_score = board_score
                best_move = move
            if best_score > alpha:
                alpha = best_score
            self.board.pop()
        return best_move 


    def nextMove(self, depth = 4):
        try: 
            move = chess.polyglot.MemoryMappedReader("./books/human.bin").weighted_choice(self.board).move
            print("book move", move)
            return move
        except:
            return self.minmax(depth)

    def makeMove(self):
        mv = self.nextMove()
        self.board.push(mv)
        
    
    def printBoard(self):
        return self.board
    
    def printEvaluation(self):
        print(self.evaluation())
    
    def printMaterialEvaluation(self):
        print(self.material_evaluation())
    
    def printIndividualPieceEvaluation(self, piece):
        print(self.individual_piece_evaluation(piece))


 
