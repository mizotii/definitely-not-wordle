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

  const handleSubmitGuess = async () => {
    try {
      const res = await instance.post('/api/guess');
      const data = res.data;

      setCurrentTurnNumber(data.current_turn_number);
      setGameStatus(data.game_status);
      setGuessHistory(data.guess_history);

      if (data.game_status != 'in_progress') {
        setCurrentAnswer(data.current_answer);
      }

    } catch (error) {
        setMessageText(error.message);
    }
  }

  useEffect(() => {
    startGame();
  }, []);

  return (
    <>
      <MessageBox message={messageText}/>
      <Grid
        currentGuess={currentGuess}
        currentTurnNumber={currentTurnNumber}
        gameStatus={gameStatus}
        guessHistory={guessHistory}
      />
      <GuessButton
        submitGuess={handleSubmitGuess}
        disabled={currentGuess.length != WORD_LENGTH || gameStatus != 'in_progress'}
      />
      <ResetButton 
        reset={startGame}
      />
    </>
  )
}

export default App
