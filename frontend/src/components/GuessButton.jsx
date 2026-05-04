const GuessButton = ({ submitGuess, disabled }) => {


    return (
        <button
            id='guess'
            className='guess-button'
            onClick={submitGuess}
            disabled={disabled}
        >
            guess
        </button>
    )
}

export default GuessButton;