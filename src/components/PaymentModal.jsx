import React, { useState } from 'react';
import QRCode from 'react-qr-code';
import { FaCreditCard, FaQrcode, FaTimes, FaCheckCircle } from 'react-icons/fa';

const PaymentModal = ({ total, onClose, onPaymentSuccess, merchantVpa, currency }) => {
    const [activeTab, setActiveTab] = useState('upi');
    const [isProcessing, setIsProcessing] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);

    // UPI ID - In a real app, this would be the merchant's VPA
    const upiId = merchantVpa || 'merchant@upi';
    // UPI always uses INR, so we pass the INR total (which is 'total' prop)
    const upiLink = `upi://pay?pa=${upiId}&pn=SouthIndianDelights&am=${total}&cu=INR`;

    const handleCardPayment = (e) => {
        e.preventDefault();
        setIsProcessing(true);
        // Simulate API call
        setTimeout(() => {
            setIsProcessing(false);
            setIsSuccess(true);
            setTimeout(() => {
                onPaymentSuccess();
            }, 2000);
        }, 1500);
    };

    if (isSuccess) {
        return (
            <div className="modal-overlay">
                <div className="modal-content success-modal">
                    <FaCheckCircle className="success-icon" />
                    <h2>Payment Successful!</h2>
                    <p>Thank you for your order.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <button onClick={onClose} className="close-modal"><FaTimes /></button>
                <h2>Payment Gateway</h2>
                <p className="payment-total">Amount to Pay: {currency.symbol} {(total / currency.rate).toFixed(2)}</p>

                <div className="payment-tabs">
                    <button
                        className={`tab-btn ${activeTab === 'upi' ? 'active' : ''}`}
                        onClick={() => setActiveTab('upi')}
                    >
                        <FaQrcode /> UPI QR
                    </button>
                    <button
                        className={`tab-btn ${activeTab === 'card' ? 'active' : ''}`}
                        onClick={() => setActiveTab('card')}
                    >
                        <FaCreditCard /> Card
                    </button>
                </div>

                <div className="payment-body">
                    {activeTab === 'upi' ? (
                        <div className="upi-section">
                            <div className="qr-wrapper">
                                <QRCode value={upiLink} size={200} />
                            </div>
                            <p className="scan-text">Scan with any UPI App</p>
                            <div className="supported-apps">
                                <span>GPay</span> • <span>PhonePe</span> • <span>Paytm</span>
                            </div>
                        </div>
                    ) : (
                        <form onSubmit={handleCardPayment} className="card-form">
                            <div className="form-group">
                                <label>Card Number</label>
                                <input type="text" placeholder="0000 0000 0000 0000" required maxLength="19" />
                            </div>
                            <div className="form-row">
                                <div className="form-group">
                                    <label>Expiry</label>
                                    <input type="text" placeholder="MM/YY" required maxLength="5" />
                                </div>
                                <div className="form-group">
                                    <label>CVV</label>
                                    <input type="password" placeholder="123" required maxLength="3" />
                                </div>
                            </div>

                            <button type="submit" className="pay-btn" disabled={isProcessing}>
                                {isProcessing ? 'Processing...' : `Pay ${currency.symbol}${(total / currency.rate).toFixed(2)}`}
                            </button>
                        </form>
                    )}
                </div>
            </div>

        </div>
    );
};

export default PaymentModal;
