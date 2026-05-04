const COLOR_CLASSES = {
    green:  'bg-green-600 text-white border-green-600',
    yellow: 'bg-yellow-400 text-white border-yellow-400',
    gray:   'bg-gray-400 text-white border-gray-400',
    none:   'bg-white text-black border-gray-300',
};

const Tile = ({ letter, color }) => {
    const colorClass = COLOR_CLASSES[color] ?? COLOR_CLASSES.none;

    return (
        <div className={`w-14 h-14 border-2 flex items-center justify-center text-xl font-bold uppercase select-none ${colorClass}`}>
            {letter}
        </div>
    )
}

export default Tile;