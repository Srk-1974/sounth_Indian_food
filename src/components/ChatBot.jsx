import React, { useState, useRef, useEffect } from 'react';
import { FaTimes, FaShoppingBag, FaUtensils, FaTrash, FaCheck } from 'react-icons/fa';

const ChatBot = ({ items, onAddToCart, currency, cart, onRemoveFromCart, onCheckout }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [view, setView] = useState('menu'); // 'menu' or 'cart'
    const [messages, setMessages] = useState([
        { text: "Hello! 👋 I'm your food assistant. What would you like to eat today?", sender: 'bot' }
    ]);
    const messagesEndRef = useRef(null);

    // Dragging state
    const [position, setPosition] = useState({ x: window.innerWidth - 80, y: window.innerHeight - 80 });
    const [isDragging, setIsDragging] = useState(false);
    const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
    const [hasMoved, setHasMoved] = useState(false);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen, view]);

    // Handle window resize to keep bot on screen
    useEffect(() => {
        const handleResize = () => {
            setPosition(prev => ({
                x: Math.min(prev.x, window.innerWidth - 80),
                y: Math.min(prev.y, window.innerHeight - 80)
            }));
        };
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    const handleMouseDown = (e) => {
        setIsDragging(true);
        setDragStart({ x: e.clientX - position.x, y: e.clientY - position.y });
        setHasMoved(false);
    };

    const handleMouseMove = (e) => {
        if (isDragging) {
            const newX = e.clientX - dragStart.x;
            const newY = e.clientY - dragStart.y;
            setPosition({ x: newX, y: newY });
            setHasMoved(true);
        }
    };

    const handleMouseUp = () => {
        setIsDragging(false);
    };

    // Attach global mouse listeners when dragging
    useEffect(() => {
        if (isDragging) {
            window.addEventListener('mousemove', handleMouseMove);
            window.addEventListener('mouseup', handleMouseUp);
        } else {
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseup', handleMouseUp);
        }
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseup', handleMouseUp);
        };
    }, [isDragging]);

    const toggleChat = () => {
        if (!hasMoved) {
            setIsOpen(!isOpen);
        }
    };

    const handleAddItem = (item) => {
        onAddToCart(item);
        setMessages(prev => [
            ...prev,
            { text: `Added ${item.name} to cart!`, sender: 'bot' }
        ]);
    };

    const handleRemoveItem = (id, name) => {
        onRemoveFromCart(id);
        setMessages(prev => [
            ...prev,
            { text: `Removed ${name} from cart.`, sender: 'bot' }
        ]);
    };

    const handleCheckoutClick = () => {
        setIsOpen(false);
        onCheckout();
    };

    return (
        <div
            className="chatbot-container"
            style={{
                left: position.x,
                top: position.y,
                cursor: isDragging ? 'grabbing' : 'grab',
                bottom: 'auto',
                right: 'auto'
            }}
            onMouseDown={handleMouseDown}
        >
            {isOpen && (
                <div className="chatbot-window" onMouseDown={(e) => e.stopPropagation()}>
                    <div className="chatbot-header">
                        <div className="chatbot-title">
                            <img src="/assets/chatbot-icon.png" alt="Bot" className="bot-avatar-small" />
                            <span>Foodie Bot</span>
                        </div>
                        <button onClick={() => setIsOpen(false)} className="close-chat"><FaTimes /></button>
                    </div>

                    <div className="chatbot-messages">
                        {messages.map((msg, index) => (
                            <div key={index} className={`chat-message ${msg.sender}`}>
                                {msg.text}
                            </div>
                        ))}

                        {view === 'menu' && (
                            <div className="chat-menu-list">
                                <p className="list-title">Menu</p>
                                {items.map(item => (
                                    <div key={item.id} className="chat-menu-item">
                                        <div className="chat-item-info">
                                            <span className="chat-item-name">{item.name}</span>
                                            <span className="chat-item-price">{currency.symbol}{Math.round(item.price / currency.rate)}</span>
                                        </div>
                                        <button onClick={() => handleAddItem(item)} className="chat-add-btn">Add</button>
                                    </div>
                                ))}
                            </div>
                        )}

                        {view === 'cart' && (
                            <div className="chat-menu-list">
                                <p className="list-title">Your Cart</p>
                                {cart.length === 0 ? (
                                    <p className="empty-cart-msg">Your cart is empty.</p>
                                ) : (
                                    cart.map(item => (
                                        <div key={item.id} className="chat-menu-item">
                                            <div className="chat-item-info">
                                                <span className="chat-item-name">{item.name} (x{item.quantity})</span>
                                                <span className="chat-item-price">{currency.symbol}{Math.round(item.price * item.quantity / currency.rate)}</span>
                                            </div>
                                            <button onClick={() => handleRemoveItem(item.id, item.name)} className="chat-remove-btn"><FaTrash /></button>
                                        </div>
                                    ))
                                )}
                                {cart.length > 0 && (
                                    <button onClick={handleCheckoutClick} className="chat-checkout-btn">
                                        Checkout Now <FaCheck />
                                    </button>
                                )}
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="chatbot-actions">
                        <button
                            className={`action-btn ${view === 'menu' ? 'active' : ''}`}
                            onClick={() => setView('menu')}
                        >
                            <FaUtensils /> Menu
                        </button>
                        <button
                            className={`action-btn ${view === 'cart' ? 'active' : ''}`}
                            onClick={() => setView('cart')}
                        >
                            <FaShoppingBag /> Cart ({cart.length})
                        </button>
                    </div>
                </div>
            )}
            <button className="chatbot-toggle" onClick={toggleChat}>
                <img src="/assets/chatbot-icon.png" alt="Chat" className="bot-icon-large animated-bot" />
                {cart.length > 0 && <span className="chat-badge">{cart.length}</span>}
            </button>
            {!isOpen && (
                <div className="chatbot-tooltip">
                    Hello! 👋 I'm your food assistant. What would you like to eat today?
                    <div className="tooltip-arrow"></div>
                </div>
            )}
        </div>
    );
};

export default ChatBot;
