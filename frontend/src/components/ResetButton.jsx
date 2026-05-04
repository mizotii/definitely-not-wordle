const ResetButton = ({ reset }) => {

    return (
        <button
            className='reset-button'
            onClick={reset}
        >
            reset
        </button>
    )
}

export default ResetButton;