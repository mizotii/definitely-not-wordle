const ROWS = [
  ['Q','W','E','R','T','Y','U','I','O','P'],
  ['A','S','D','F','G','H','J','K','L'],
  ['ENTER','Z','X','C','V','B','N','M','⌫'],
];

export default function Keyboard({ onKey }) {
  return (
    <div className="flex flex-col items-center gap-1">
      {ROWS.map((row, i) => (
        <div key={i} className="flex gap-1">
          {row.map((key) => (
            <button
              key={key}
              onClick={() => onKey(key === '⌫' ? 'Backspace' : key)}
              className="h-14 min-w-8 px-1 sm:min-w-11 rounded bg-gray-200 text-sm font-bold uppercase active:bg-gray-400"
            >
              {key}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
}
