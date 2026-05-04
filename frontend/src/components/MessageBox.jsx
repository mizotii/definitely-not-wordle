const MessageBox = ({ message }) => {

    if (!message) return null;

    return (
        <p className="text-sm tracking-wide text-gray-600">{message}</p>
    )
}

export default MessageBox;