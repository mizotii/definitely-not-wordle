import Tile from "./Tile";

const Row = ({ guess, colors, wordLength }) => {
    function paddedGuessArray(str) {
        return Array.from(str.padEnd(wordLength, '\u00A0'));
    }

    return (
        <div className='row'>
            {paddedGuessArray(guess).map((c, i) =>
                <Tile letter={c} color={colors[i] ?? 'none'} key={i} />
            )}
        </div>
    )
}

export default Row;