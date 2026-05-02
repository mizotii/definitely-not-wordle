import { useEffect, useState } from 'react'
import axios from 'axios';
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/api/hello')
      .then((res) => {
        console.log(res)
        setData(res.data);
      })
      .catch((err) => {
        setError(err.message);
      })
  }, []);

  return (
    <>
      <h1>
        {data ? data.message : error.message}
      </h1>
    </>
  )
}

export default App
