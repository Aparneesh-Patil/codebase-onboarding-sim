import { useState, useRef, useEffect } from 'react'
import '../styles/ChatPanel.css'
import { sendChatMessage } from '../service/api'

function ChatPanel( {repoId}) {
    const [input, setInput] = useState('')
    const [messages, setMessages] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef(null)

    useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
        behavior: 'smooth'
    })
    }, [messages, isLoading])

    // functiont to make chatbot's texts feel more user friendly
    function typeAssistantMessage(answer) {
    const assistantMessage = {
        role: 'assistant',
        content: ''
    }

    setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage
    ])

    let characterIndex = 0

    const typingInterval = setInterval(() => {
        characterIndex += 1

        setMessages((previousMessages) => {
        const updatedMessages = [...previousMessages]
        const lastMessageIndex = updatedMessages.length - 1

        updatedMessages[lastMessageIndex] = {
            ...updatedMessages[lastMessageIndex],
            content: answer.slice(0, characterIndex)
        }

        return updatedMessages
        })

        if (characterIndex >= answer.length) {
        clearInterval(typingInterval)
        }
    }, 20)
    }

    // sends message to chatbot
    async function sendMessage(question) {
        const trimmedQuestion = question.trim()

        if (!trimmedQuestion || isLoading) {
            return
        }

        const userMessage = {
            role: 'user',
            content: trimmedQuestion
        }

        setMessages((previousMessages) => [
        ...previousMessages,
        userMessage
        ])

        setInput('')
        setIsLoading(true)

        // regardless of whether we run into an error or not, our loading animation stops (using the finally button)
        try {
            const data = await sendChatMessage(trimmedQuestion, repoId)
            
            typeAssistantMessage(data.response)
        } catch (error) {
            console.error(error)

            setMessages((previousMessages) => [
                ...previousMessages,
                {
                    role: 'assistant',
                    content: 'Something went wrong while getting a response.'
                }
            ])
        } finally {
            setIsLoading(false)
        }

    }

    // user's chat bubble
    function handleSubmit(event) {
        event.preventDefault()
        sendMessage(input)
    }

    return (
        <main className="chat-panel">
        <header className="chat-header">
            <h2>Repository Assistant</h2>
            <p>Ask questions about the uploaded codebase.</p>
        </header>

        <section className="chat-content">
            {messages.length === 0 ? (
            <div className="welcome-message">
                <h3>Where would you like to start?</h3>

                <div className="starter-questions">
                <button
                    type="button"
                    onClick={() => sendMessage('Explain this project')}
                >
                    Explain this project
                </button>

                <button
                    type="button"
                    onClick={() => sendMessage('Where should I start reading?')}
                >
                    Where should I start reading?
                </button>

                <button
                    type="button"
                    onClick={() => sendMessage('What are the important files?')}
                >
                    What are the important files?
                </button>
                </div>
            </div>
            ) : (
            <div className="messages">
                {messages.map((message, index) => (
                    <div
                    key={index}
                    className={`message ${message.role}`}
                    >
                    {message.content}
                    </div>
                ))}

                {isLoading && (
                    <div className="message assistant loading-message">
                    <span></span>
                    <span></span>
                    <span></span>
                    </div>
                )}

                <div ref={messagesEndRef}></div>
            </div>
            )}
        </section>

        <form className="chat-form" onSubmit={handleSubmit}>
            <input
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about this repository..."
            disabled={isLoading}
            />

            <button type="submit" disabled={isLoading}> {isLoading ? 'Waiting...' : 'Send'} </button>
        </form>
        </main>
    )
}

export default ChatPanel