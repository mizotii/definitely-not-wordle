import { useEffect, useState } from 'react'
import { instance } from './api/axios'
import { WORD_LENGTH } from './constants';
import './App.css'
import MessageBox from './components/MessageBox';
import Grid from './components/Grid';
import GuessButton from './components/GuessButton';
import ResetButton from './components/ResetButton';

function App() {

  const [currentGuess, setCurrentGuess] = useState('');
  const [messageText, setMessageText] = useState('');

  const [currentTurnNumber, setCurrentTurnNumber] = useState(0);
  const [gameStatus, setGameStatus] = useState('in_progress');
  const [guessHistory, setGuessHistory] = useState([]);

  const [currentAnswer, setCurrentAnswer] = useState();

  const startGame = async () => {
    try {
      const res = await instance.post('/api/game/start');
      const data = res.data;

      setCurrentTurnNumber(data.current_turn_number);
      setGameStatus(data.game_status);
      setGuessHistory(data.guess_history);
    } catch (error) {
        setMessageText(error.message);
    }
  }

  const getGameStatus = async () => {
    try {
      const res = await instance.get('/api/game');
      const data = res.data;

      setCurrentTurnNumber(data.current_turn_number);
      setGameStatus(data.game_status);
      setGuessHistory(data.guess_history);
    } catch (error) {
        setMessageText(error.message);
    }
  }

  const handleSubmitGuess = async (guess) => {
    try {
      const res = await instance.post('/api/guess', {guess});
      const data = res.data;

      setCurrentGuess('');
      setMessageText('');
      setCurrentTurnNumber(data.current_turn_number);
      setGameStatus(data.game_status);
      setGuessHistory(data.guess_history);

      if (data.game_status != 'in_progress') {
        setMessageText(`You ${data.game_status}.`);
        setCurrentAnswer(data.current_answer);
      }

    } catch (error) {
        setMessageText(error.message);
    }
  }

  useEffect(() => {
    startGame();
  }, []);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (gameStatus === 'in_progress') {
        if (e.key === 'Enter' && currentGuess.length === WORD_LENGTH) {
          handleSubmitGuess(currentGuess);
        }
        else if (e.key === 'Backspace' && currentGuess.length > 0) {
          setCurrentGuess(currentGuess.slice(0, -1));
        }
        else if (e.key.match(/^[a-z]$/i) && currentGuess.length < WORD_LENGTH) {
          setCurrentGuess(currentGuess + e.key.toUpperCase());
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);

  }, [currentGuess, gameStatus])

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center gap-6">
      <h1 className="text-2xl font-semibold tracking-widest uppercase">Wordle</h1>
      <MessageBox message={messageText}/>
      <Grid
        currentGuess={currentGuess}
        currentTurnNumber={currentTurnNumber}
        gameStatus={gameStatus}
        guessHistory={guessHistory}
      />
      <div className="flex gap-3">
        <GuessButton
          submitGuess={() => handleSubmitGuess(currentGuess)}
          disabled={currentGuess.length != WORD_LENGTH || gameStatus != 'in_progress'}
        />
        <ResetButton
          reset={startGame}
        />
      </div>
    </div>
  )
}

export default App
