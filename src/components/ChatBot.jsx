import React, { useState, useRef, useEffect } from 'react';
import { FaTimes, FaShoppingBag, FaUtensils, FaTrash, FaCheck, FaPaperPlane } from 'react-icons/fa';

const ChatBot = ({ items, onAddToCart, currency, cart, onRemoveFromCart, onCheckout }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [view, setView] = useState('chat'); // 'chat', 'menu' or 'cart'
    const getGreeting = () => {
        const hour = new Date().getHours();
        if (hour < 12) return "Good Morning";
        if (hour < 18) return "Good Afternoon";
        return "Good Evening";
    };

    const [messages, setMessages] = useState([
        { text: `${getGreeting()}! 👋 I'm your food assistant. What would you like to eat today?`, sender: 'bot' }
    ]);
    const [userInput, setUserInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    // Dragging state
    const [position, setPosition] = useState({ x: window.innerWidth - 80, y: window.innerHeight - 80 });
    const [isDragging, setIsDragging] = useState(false);
    const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
    const [hasMoved, setHasMoved] = useState(false);

    // Detect if device is mobile/touch
    const isMobile = 'ontouchstart' in window;

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

    const handleTouchStart = (e) => {
        setIsDragging(true);
        setDragStart({ x: e.touches[0].clientX - position.x, y: e.touches[0].clientY - position.y });
        setHasMoved(false);
    };

    const handleTouchMove = (e) => {
        if (isDragging) {
            const newX = e.touches[0].clientX - dragStart.x;
            const newY = e.touches[0].clientY - dragStart.y;
            setPosition({ x: newX, y: newY });
            setHasMoved(true);
        }
    };

    const handleTouchEnd = () => {
        setIsDragging(false);
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
            if (!isOpen) {
                setView('chat');
            }
        }
    };

    // AI-like intelligence functions
    const containsKeyword = (text, keywords) => {
        return keywords.some(keyword => text.includes(keyword));
    };

    const getSmartResponse = (userMessage) => {
        const msg = userMessage.toLowerCase();

        if (containsKeyword(msg, ['hi', 'hello', 'hey'])) {
            return "Hello! 😊 I'm here to help you order delicious South Indian food. What are you craving?";
        }

        if (containsKeyword(msg, ['breakfast', 'morning'])) {
            const breakfastItems = items.filter(item => item.category === 'Breakfast');
            if (breakfastItems.length > 0) {
                const itemsList = breakfastItems.map(item => `• ${item.name} - ${currency.symbol}${Math.round(item.price / currency.rate)}`).join('\n');
                return `🌅 Good morning! Here are our delicious breakfast items:\n\n${itemsList}\n\nPerfect way to start your day! 😊`;
            }
        }

        if (containsKeyword(msg, ['spicy', 'hot', 'chili'])) {
            return "🌶️ Looking for something spicy? **Bajji** is available and it's perfectly spiced! You can find it in our Snacks section. Want to try it? 🔥";
        }

        if (containsKeyword(msg, ['sweet', 'dessert'])) {
            return "For something sweet, our beverages are perfect! Try Coffee or Tea. ☕";
        }

        if (containsKeyword(msg, ['hungry', 'starving', 'eat'])) {
            return "I can help with that! 🍽️ Our most popular items are Idly and Dosa. Both are delicious and filling!";
        }

        if (containsKeyword(msg, ['cheap', 'budget', 'affordable', 'price'])) {
            const cheapest = items.reduce((min, item) => item.price < min.price ? item : min, items[0]);
            return `Our most affordable option is ${cheapest.name} at ${currency.symbol}${Math.round(cheapest.price / currency.rate)}. Great value! 💰`;
        }

        if (containsKeyword(msg, ['popular', 'best', 'recommend', 'delicious', 'good'])) {
            return "😋 All our items are absolutely delicious! But if I had to pick favorites:\n\n🌟 **IDLY** - Soft, fluffy, healthy!\n🌟 **DOSA** - Crispy golden perfection!\n🌟 **VADA** - Crunchy outside, soft inside!\n\nYou really can't go wrong with anything on our menu! 💯";
        }

        if (containsKeyword(msg, ['drink', 'beverage', 'tea', 'coffee'])) {
            const beverages = items.filter(item => item.category === 'Beverages');
            return `We have ${beverages.map(i => i.name).join(' and ')}. Perfect to go with your meal! ☕`;
        }

        if (containsKeyword(msg, ['snack', 'light'])) {
            const snacks = items.filter(item => item.category === 'Snacks');
            if (snacks.length > 0) {
                const itemsList = snacks.map(item => `• ${item.name} - ${currency.symbol}${Math.round(item.price / currency.rate)}`).join('\n');
                return `🍪 Perfect for snack time! Here are our crispy delights:\n\n${itemsList}\n\nCrunchy and delicious! 😋`;
            }
        }

        if (containsKeyword(msg, ['help', 'menu', 'show'])) {
            return "I can help you find the perfect meal! Try asking me about breakfast, snacks, or beverages. Or just tell me what you're craving! 😊";
        }

        return "I'm not sure about that, but I can show you our menu! Click the Menu tab below to browse all items. 📋";
    };

    const handleSendMessage = () => {
        if (!userInput.trim()) return;

        const userMsg = { text: userInput, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        setUserInput('');
        setIsTyping(true);

        setTimeout(() => {
            setIsTyping(false);
            const botResponse = getSmartResponse(userInput);
            setMessages(prev => [...prev, { text: botResponse, sender: 'bot' }]);
        }, 800);
    };

    const handleQuickReply = (message) => {
        setUserInput(message);
        setTimeout(() => handleSendMessage(), 100);
    };

    const handleAddItem = (item) => {
        onAddToCart(item);
        setMessages(prev => [
            ...prev,
            { text: `Added ${item.name} to cart! Anything else? 😋`, sender: 'bot' }
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

    const quickReplies = [
        "Show breakfast items",
        "Show snacks",
        "What's spicy?",
        "What's most delicious?"
    ];

    return (
        <div
            className="chatbot-container"
            style={{
                left: position.x,
                top: position.y,
                cursor: isMobile ? 'pointer' : (isDragging ? 'grabbing' : 'grab'),
                bottom: 'auto',
                right: 'auto'
            }}
            onMouseDown={handleMouseDown}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
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

                        {isTyping && (
                            <div className="chat-message bot typing-indicator">
                                <span></span><span></span><span></span>
                            </div>
                        )}

                        {view === 'chat' && (
                            <div className="quick-replies">
                                {quickReplies.map((reply, idx) => (
                                    <button
                                        key={idx}
                                        className="quick-reply-btn"
                                        onClick={() => handleQuickReply(reply)}
                                    >
                                        {reply}
                                    </button>
                                ))}
                            </div>
                        )}

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

                    {view === 'chat' && (
                        <div className="chat-input-container">
                            <input
                                type="text"
                                className="chat-input"
                                placeholder="Ask me anything..."
                                value={userInput}
                                onChange={(e) => setUserInput(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                            />
                            <button className="chat-send-btn" onClick={handleSendMessage}>
                                <FaPaperPlane />
                            </button>
                        </div>
                    )}

                    <div className="chatbot-actions">
                        <button
                            className={`action-btn ${view === 'chat' ? 'active' : ''}`}
                            onClick={() => setView('chat')}
                        >
                            💬 Chat
                        </button>
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
            {
                !isOpen && (
                    <div className="chatbot-tooltip">
                        {getGreeting()}! 👋 I'm your food assistant. What would you like to eat today?
                        <div className="tooltip-arrow"></div>
                    </div>
                )
            }
        </div >
    );
};

export default ChatBot;
