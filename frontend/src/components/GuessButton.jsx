const GuessButton = ({ submitGuess, disabled }) => {


    return (
        <button
            id='guess'
            onClick={submitGuess}
            disabled={disabled}
            className="px-5 py-2 text-sm uppercase tracking-widest border border-black text-black hover:bg-black hover:text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
        >
            guess
        </button>
    )
}

export default GuessButton;