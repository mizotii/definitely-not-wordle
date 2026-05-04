import Tile from "./Tile";
import { WORD_LENGTH } from "../constants";

const Row = ({ guess, colors }) => {
    function paddedGuessArray(str) {
        return Array.from(str.padEnd(WORD_LENGTH, '\u00A0'));
    }

    return (
        <div className="flex gap-1">
            {paddedGuessArray(guess).map((c, i) =>
                <Tile letter={c} color={colors[i] ?? 'none'} key={i} />
            )}
        </div>
    )
}

export default Row;