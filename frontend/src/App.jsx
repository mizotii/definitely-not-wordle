import { useEffect, useState } from 'react'
import { instance } from './api/axios'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {
  const [currentGuess, setCurrentGuess] = useState('')
  const [messageText, setMessageText] = useState('')

  const [currentTurnNumber, setCurrentTurnNumber] = useState(0)
  const [gameStatus, setGameStatus] = useState('in_progress')
  const [guessHistory, setGuessHistory] = useState([])



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

  useEffect(() => {
    startGame();
  }, []);

  return (
    <>
    </>
  )
}

export default App
