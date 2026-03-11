import React from 'react';
import { FaTrash, FaShoppingCart, FaWhatsapp } from 'react-icons/fa';

const Cart = ({ cartItems, onRemove, onCheckout, currency, whatsappNumber, allItems }) => {
    const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

    const handleWhatsAppOrder = () => {
        // Format order message
        let message = "🍽️ *New Order from Food App*\n\n";
        message += "*Items:*\n";

        cartItems.forEach(item => {
            message += `• ${item.name} x${item.quantity} - ${currency.symbol}${((item.price * item.quantity) / currency.rate).toFixed(2)}\n`;
        });

        message += `\n*Total: ${currency.symbol}${(total / currency.rate).toFixed(2)}*\n\n`;
        message += "Please confirm my order. Thank you! 😊";

        // Encode message for URL
        const encodedMessage = encodeURIComponent(message);

        // WhatsApp number (remove + and spaces)
        const phoneNumber = whatsappNumber.replace(/[^0-9]/g, '');

        // Open WhatsApp
        const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
        window.open(whatsappUrl, '_blank');
    };

    const handleBrowseMenu = () => {
        // Group items by category
        const categories = {};
        allItems.forEach(item => {
            if (!categories[item.category]) {
                categories[item.category] = [];
            }
            categories[item.category].push(item);
        });

        // Format complete menu message
        let message = "🍽️ *South Indian Delights - Complete Menu*\n\n";

        // Add each category
        Object.keys(categories).sort().forEach(category => {
            const emoji = {
                'Breakfast': '🌅',
                'Lunch': '🍛',
                'Snacks': '🍪',
                'Beverages': '☕'
            }[category] || '📋';

            message += `${emoji} *${category.toUpperCase()}*\n`;
            categories[category].forEach(item => {
                message += `• ${item.name} - ${currency.symbol}${Math.round(item.price / currency.rate)}\n`;
            });
            message += "\n";
        });

        message += "---\n";
        message += "*To order, reply with:*\n";
        message += "Item name x Quantity\n\n";
        message += "*Example:*\n";
        message += "Idly x2\n";
        message += "Dosa x1\n";
        message += "Tea x1\n\n";
        message += "We'll confirm your order! 😊";

        // Encode and open WhatsApp
        const encodedMessage = encodeURIComponent(message);
        const phoneNumber = whatsappNumber.replace(/[^0-9]/g, '');
        const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
        window.open(whatsappUrl, '_blank');
    };

    if (cartItems.length === 0) {
        return null;
    }

    return (
        <div className="cart-container">
            <div className="cart-header">
                <h2><FaShoppingCart /> Your Cart</h2>
            </div>
            <div className="cart-items">
                {cartItems.map((item) => (
                    <div key={item.id} className="cart-item">
                        <div className="cart-item-info">
                            <span className="cart-item-name">{item.name}</span>
                            <span className="cart-item-qty">x{item.quantity}</span>
                        </div>
                        <div className="cart-item-price">
                            {currency.symbol} {((item.price * item.quantity) / currency.rate).toFixed(2)}
                        </div>
                        <button onClick={() => onRemove(item.id)} className="remove-btn">
                            <FaTrash />
                        </button>
                    </div>
                ))}
            </div>
            <div className="cart-footer">
                <div className="total-amount">
                    Total: {currency.symbol} {(total / currency.rate).toFixed(2)}
                </div>
                <button onClick={handleBrowseMenu} className="whatsapp-btn whatsapp-menu-btn">
                    <FaWhatsapp /> Browse Menu via WhatsApp
                </button>
                <button onClick={handleWhatsAppOrder} className="whatsapp-btn">
                    <FaWhatsapp /> Order via WhatsApp
                </button>
                <button onClick={onCheckout} className="checkout-btn">Checkout</button>
            </div>
        </div>
    );
};

export default Cart;
