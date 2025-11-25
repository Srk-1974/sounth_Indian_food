import React from 'react';
import { FaTrash, FaShoppingCart } from 'react-icons/fa';

const Cart = ({ cartItems, onRemove, onCheckout, currency }) => {
    const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

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
                <button onClick={onCheckout} className="checkout-btn">Checkout</button>
            </div>
        </div>
    );
};

export default Cart;
