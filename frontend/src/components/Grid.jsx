import Row from "./Row";

const Grid = ({ currentGuess, currentTurnNumber, gameStatus, guessHistory }) => {

    return (
        <div className="flex flex-col gap-1">
            {guessHistory.map((g, i) => (
                <Row guess={i === currentTurnNumber && gameStatus === 'in_progress' ? currentGuess : Object.keys(g)[0]} colors={Object.values(g)[0]} key={i}/>
            ))}
        </div>
    )
}

export default Grid;