import { useEffect, useState } from 'react'
import { instance } from './api/axios'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {
  const [data, setData] = useState([]);
  const [error, setError] = useState('');

  const fetchPing = async () => {
    const res = await instance.get('/api/hello');
    setData(res.data);
  }

  useEffect(() => {
    fetchPing();
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
