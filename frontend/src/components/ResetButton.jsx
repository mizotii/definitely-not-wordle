const ResetButton = ({ reset }) => {

    return (
        <button
            onClick={reset}
            className="px-5 py-2 text-sm uppercase tracking-widest border border-gray-400 text-gray-500 hover:border-black hover:text-black transition-colors"
        >
            reset
        </button>
    )
}

export default ResetButton;